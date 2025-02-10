import difflib
import bs4
import re

def read_html_content(filename):
    """读取HTML文件并提取可见文本"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup.get_text().splitlines(keepends=True)  # 按行拆分，保持换行
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def generate_diff_html(file1, file2, output_file='diff.html'):
    """对比HTML的可见文本内容，并生成更直观的差异报告"""
    text1 = read_html_content(file1)
    text2 = read_html_content(file2)

    differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=80)
    diff_content = differ.make_file(text1, text2, file1, file2, context=True)

    # 自定义CSS样式，增强可视化
    styled_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>HTML 可视化差异对比</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                background-color: white;
                box-shadow: 0px 0px 10px #ddd;
            }}
            th, td {{
                padding: 8px;
                border: 1px solid #ddd;
                font-size: 14px;
            }}
            .diff_add {{
                background-color: #d4fcbc;  /* 绿色 - 添加的文本 */
            }}
            .diff_sub {{
                background-color: #ffb6ba;  /* 红色 - 删除的文本 */
            }}
            .diff_chg {{
                background-color: #ffff99;  /* 黄色 - 修改的文本 */
            }}
        </style>
    </head>
    <body>
        <h2>HTML 可视化差异对比</h2>
        {diff_content}
    </body>
    </html>
    """

    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)

    print(f"可视化差异报告已生成：{output_file}")

if __name__ == "__main__":
    # 直接在代码中指定文件路径
    file1 = r"C:\path\to\your\file1.html"  # 修改为你的文件路径
    file2 = r"C:\path\to\your\file2.html"  # 修改为你的文件路径
    output_file = r"C:\path\to\your\diff.html"  # 输出文件路径

    generate_diff_html(file1, file2, output_file)
