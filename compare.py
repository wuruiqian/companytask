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
    """
    归一化文本：删除多余空白（包括换行、空行、制表符等），
    使得 'abc\n   def' 归一化为 'abc def'
    """
    return " ".join(text.split())

def highlight_text_diff(old_text, new_text):
    """
    对比两个归一化后的文本，返回 file1 部分的文本，
    对于 file1 中与 file2 不同的部分，用 <span class="diff_sub">包裹。
    对于 file2 中新增的内容，不显示。
    """
    differ = difflib.SequenceMatcher(None, old_text, new_text)
    result = []
    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag == 'equal':
            result.append(old_text[i1:i2])
        elif tag in ('replace', 'delete'):
            # 对于 file1 中有而 file2 中不同或缺失的部分，做高亮处理
            result.append(f'<span class="diff_sub">{old_text[i1:i2]}</span>')
        elif tag == 'insert':
            # file2 中新增的部分，不显示
            continue
    return ''.join(result)

def mark_differences(file1, file2, output_file='diff.html'):
    """
    对比两个 HTML 文件：
      - 对于每个标签，如果归一化后的文本不一致，则
        用 difflib 计算差异，仅在 file1 中对差异部分高亮显示，
        输出结果仍保持原 HTML 结构
    """
    html1 = read_html(file1)
    html2 = read_html(file2)

    # 解析 HTML 文件
    soup1 = BeautifulSoup(html1, "html.parser")
    soup2 = BeautifulSoup(html2, "html.parser")

    # 遍历 file1 与 file2 中所有标签（假设两文件标签顺序基本相同）
    for tag1, tag2 in zip(soup1.find_all(), soup2.find_all()):
        # 如果两个标签都有文本内容，则进行归一化后对比
        if tag1.string and tag2.string:
            norm_text1 = normalize_text(tag1.string)
            norm_text2 = normalize_text(tag2.string)
            if norm_text1 != norm_text2:
                # 计算 file1 的差异高亮（仅显示 file1 文本，但不显示 file2 新增内容）
                diff_html = highlight_text_diff(norm_text1, norm_text2)
                # 替换标签中的原文本，注意这里用归一化后的文本替换原文本
                tag1.string.replace_with(NavigableString(""))
                tag1.append(BeautifulSoup(diff_html, "html.parser"))
    # 自定义 CSS 样式
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
                background-color: #ffb6ba;  /* 红色 - 表示 file1 中与 file2 不同的部分 */
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

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)
    print(f"差异标注报告已生成：{output_file}")

if __name__ == "__main__":
    # 修改为你的 HTML 文件路径
    file1 = r"C:\path\to\your\file1.html"
    file2 = r"C:\path\to\your\file2.html"
    output_file = r"C:\path\to\your\diff.html"
    mark_differences(file1, file2, output_file)
