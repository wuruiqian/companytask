import difflib

def read_file(filename):
    """读取文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines(keepends=True)
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def compare_html(file1, file2, output_file='diff.html'):
    """比较两个HTML文件，并生成带高亮的差异报告"""
    # 读取文件内容
    text1 = read_file(file1)
    text2 = read_file(file2)

    # 创建HTML差异比较器
    differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=80)

    # 生成HTML差异报告
    diff_content = differ.make_file(text1, text2, file1, file2, context=True)

    # 定义CSS样式，增强高亮效果
    styled_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>HTML 文件差异对比</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                padding: 8px;
                border: 1px solid #ddd;
                font-size: 14px;
            }}
            .diff_add {{
                background-color: #d4fcbc;  /* 绿色 - 添加的内容 */
            }}
            .diff_sub {{
                background-color: #ffb6ba;  /* 红色 - 删除的内容 */
            }}
            .diff_chg {{
                background-color: #ffff99;  /* 黄色 - 变化的内容 */
            }}
        </style>
    </head>
    <body>
        <h2>HTML 文件差异对比</h2>
        {diff_content}
    </body>
    </html>
    """

    # 将结果写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)

    print(f"差异报告已生成：{output_file}")

if __name__ == "__main__":
    # 指定HTML文件路径
    file1 = "C:/path/to/your/file1.html"  # 替换成你的HTML文件路径
    file2 = "C:/path/to/your/file2.html"  # 替换成你的HTML文件路径
    output_file = "C:/path/to/your/diff.html"  # 结果文件路径

    compare_html(file1, file2, output_file)
