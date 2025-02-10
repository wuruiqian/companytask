import difflib
import argparse

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines(keepends=True)
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
        exit(1)

def compare_html(file1, file2, output_file='diff.html'):
    # 读取文件内容
    text1 = read_file(file1)
    text2 = read_file(file2)

    # 创建差异比较器
    differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=80)

    # 生成差异报告
    diff_content = differ.make_file(text1, text2, file1, file2, context=True)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(diff_content)

    print(f"差异报告已生成：{output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='比较两个HTML文件的差异')
    parser.add_argument('file1', help='第一个HTML文件路径')
    parser.add_argument('file2', help='第二个HTML文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认：diff.html）', default='diff.html')
    
    args = parser.parse_args()
    
    compare_html(args.file1, args.file2, args.output)