import difflib
from bs4 import BeautifulSoup, NavigableString

def read_html(filename):
    """读取 HTML 文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def normalize_text(text):
    """去除多余空白符（包括换行、制表符等），归一化文本"""
    if not text:
        return ""  # 处理 None 值
    return " ".join(text.split())

def highlight_text_diff(old_text, new_text):
    """
    仅在 file1（旧文件）中高亮不同部分，file2（新文件）新增部分不显示
    """
    differ = difflib.SequenceMatcher(None, old_text, new_text)
    result = []
    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag == 'equal':
            result.append(old_text[i1:i2])  # 相同部分
        elif tag in ('replace', 'delete'):
            result.append(f'<span class="diff_sub">{old_text[i1:i2]}</span>')  # 仅高亮 file1 中不同部分
        elif tag == 'insert':
            continue  # file2（新文件）新增部分不显示
    return ''.join(result)

def mark_differences(file1, file2, output_file='diff.html'):
    """对比 HTML 文件，仅高亮 file1 中的差异部分"""
    html1 = read_html(file1)
    html2 = read_html(file2)

    # 解析 HTML 并删除空行
    soup1 = BeautifulSoup("\n".join([line.strip() for line in html1.splitlines() if line.strip()]), "html.parser")
    soup2 = BeautifulSoup("\n".join([line.strip() for line in html2.splitlines() if line.strip()]), "html.parser")

    tags1 = soup1.find_all()
    tags2 = soup2.find_all()

    # 确保两个文件的标签数量一致，取最小值
    min_len = min(len(tags1), len(tags2))
    if len(tags1) != len(tags2):
        print(f"⚠️ 警告：HTML 结构不同！仅对比前 {min_len} 个标签")

    for i in range(min_len):
        tag1 = tags1[i]
        tag2 = tags2[i]

        # 确保标签名称匹配
        if tag1.name != tag2.name:
            print(f"⚠️ 标签不匹配: {tag1.name} ↔ {tag2.name}，跳过该对比")
            continue

        # 确保文本非空
        if tag1.string and tag2.string:
            norm_text1 = normalize_text(tag1.string)
            norm_text2 = normalize_text(tag2.string)

            if norm_text1 != norm_text2:
                diff_html = highlight_text_diff(norm_text1, norm_text2)
                tag1.string.replace_with(NavigableString(""))  # 清空原文本
                tag1.append(BeautifulSoup(diff_html, "html.parser"))  # 替换为带高亮的文本

    # CSS 样式
    styled_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>HTML 差异标注</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            .diff_sub {{
                background-color: #ffb6ba;  /* file1 不同的部分高亮 */
                color: red;
                text-decoration: line-through;
            }}
        </style>
    </head>
    <body>
        {str(soup1)}
    </body>
    </html>
    """

    # 生成输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)
    print(f"✅ 差异标注报告已生成：{output_file}")

if __name__ == "__main__":
    file1 = r"C:\path\to\your\file1.html"  # 你的 HTML 文件路径
    file2 = r"C:\path\to\your\file2.html"  # 你的 HTML 文件路径
    output_file = r"C:\path\to\your\diff.html"  # 结果文件路径
    mark_differences(file1, file2, output_file)
