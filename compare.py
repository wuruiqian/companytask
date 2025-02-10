import difflib
from bs4 import BeautifulSoup, NavigableString

def read_html(filename):
    """读取 HTML 文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def normalize_text(text):
    """
    归一化文本：将文本中的所有空白字符（包括换行、制表符、多个空格等）
    合并为一个空格，避免因格式差异产生不必要的对比差异
    """
    return " ".join(text.split())

def highlight_text_diff(old_text, new_text):
    """
    对比归一化后的文本，返回 file1 中不相同的部分（替换和删除部分）用高亮标记包裹的字符串。
    file2 中新增的部分（insert）不显示。
    """
    differ = difflib.SequenceMatcher(None, old_text, new_text)
    result = []
    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag == 'equal':
            result.append(old_text[i1:i2])
        elif tag in ('replace', 'delete'):
            result.append(f'<span class="diff_sub">{old_text[i1:i2]}</span>')
        elif tag == 'insert':
            # file2 中新增的部分，不显示
            continue
    return ''.join(result)

def mark_differences(file1, file2, output_file='diff.html'):
    """
    对比两个 HTML 文件：
      1. 先对文件内容去除空行和归一化空白字符（不会改变 HTML 结构）。
      2. 使用 BeautifulSoup 解析 HTML，得到所有标签。
      3. 对于两个文件中对应的标签（按解析顺序），如果其文本归一化后不同，
         则在 file1 中将不同部分用 <span class="diff_sub"> 高亮显示（只显示 file1 部分）。
      4. 若两个 HTML 文件标签数不同，则仅对比较少部分，并发出提示。
    """
    html1 = read_html(file1)
    html2 = read_html(file2)

    # 删除多余的空行（每行 strip 后不为空才保留）
    html1 = "\n".join(line.strip() for line in html1.splitlines() if line.strip() != "")
    html2 = "\n".join(line.strip() for line in html2.splitlines() if line.strip() != "")

    soup1 = BeautifulSoup(html1, "html.parser")
    soup2 = BeautifulSoup(html2, "html.parser")

    tags1 = soup1.find_all()
    tags2 = soup2.find_all()
    min_len = min(len(tags1), len(tags2))
    if len(tags1) != len(tags2):
        print(f"警告：两个文件标签数量不同（file1: {len(tags1)}，file2: {len(tags2)}）。仅对比前 {min_len} 个标签。")

    for i in range(min_len):
        tag1 = tags1[i]
        tag2 = tags2[i]
        # 只对比含有纯文本（string）且不为 None 的标签
        if tag1.string and tag2.string:
            norm_text1 = normalize_text(tag1.string)
            norm_text2 = normalize_text(tag2.string)
            if norm_text1 != norm_text2:
                diff_html = highlight_text_diff(norm_text1, norm_text2)
                # 清空原有文本，再插入经过高亮处理的文本
                tag1.string.replace_with(NavigableString(""))
                tag1.append(BeautifulSoup(diff_html, "html.parser"))

    # 自定义 CSS 样式，只定义 file1 中差异部分的显示效果
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
                background-color: #ffb6ba;  /* 红色背景表示 file1 中与 file2 不同的部分 */
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
    # 请根据实际情况修改下面文件路径
    file1 = r"C:\path\to\your\file1.html"
    file2 = r"C:\path\to\your\file2.html"
    output_file = r"C:\path\to\your\diff.html"
    mark_differences(file1, file2, output_file)
