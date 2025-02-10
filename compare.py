import difflib
import bs4

def read_html(filename):
    """读取 HTML 文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def highlight_diff_in_html(file1, file2, output_file='diff.html'):
    """在原 HTML 文件中标注差异部分，保留原 HTML 结构"""
    html1 = read_html(file1)
    html2 = read_html(file2)

    # 使用 BeautifulSoup 解析 HTML 文件，保留 HTML 结构
    soup1 = bs4.BeautifulSoup(html1, "html.parser")
    soup2 = bs4.BeautifulSoup(html2, "html.parser")

    # 获取原 HTML 文件的文本内容
    text1 = soup1.get_text()
    text2 = soup2.get_text()

    # 使用 difflib 进行文本对比
    differ = difflib.Differ()
    diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

    # 将差异部分添加 CSS 样式进行高亮
    def mark_diff(diff_list):
        """给差异部分添加标注"""
        highlighted_text = []
        for line in diff_list:
            if line.startswith('+'):
                highlighted_text.append(f'<span class="diff_add">{line[2:]}</span>')  # 新增的内容
            elif line.startswith('-'):
                highlighted_text.append(f'<span class="diff_sub">{line[2:]}</span>')  # 删除的内容
            elif line.startswith('?'):
                continue  # 跳过问号行（这些是 diff 的提示行，不需要显示）
            else:
                highlighted_text.append(line)  # 保留不变的内容
        return '\n'.join(highlighted_text)

    # 标注文本差异
    marked_diff = mark_diff(diff)

    # 将差异部分插入原 HTML 文件
    soup1.body.insert(0, marked_diff)

    # 自定义 CSS 样式，突出差异
    styled_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>HTML 差异标注</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .diff_add {{
                background-color: #d4fcbc;  /* 绿色 - 新增内容 */
                color: green;
                font-weight: bold;
            }}
            .diff_sub {{
                background-color: #ffb6ba;  /* 红色 - 删除内容 */
                color: red;
                text-decoration: line-through;
            }}
            span {{
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <h2>HTML 差异标注</h2>
        {str(soup1)}
    </body>
    </html>
    """

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)

    print(f"差异标注报告已生成：{output_file}")

if __name__ == "__main__":
    # 直接在代码中指定文件路径
    file1 = r"C:\path\to\your\file1.html"  # 替换为你的文件路径
    file2 = r"C:\path\to\your\file2.html"  # 替换为你的文件路径
    output_file = r"C:\path\to\your\diff.html"  # 输出文件路径

    highlight_diff_in_html(file1, file2, output_file)
