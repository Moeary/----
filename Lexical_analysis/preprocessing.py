import re
import string
#去除注释和无效行等
def code(string_s):
    # 删除注释
    string_s = re.sub(r'#.*', '', string_s)
    # 删除空白行和额外的空格
    string_s = '\n'.join(line.strip() for line in string_s.split('\n') if line.strip())
    return string_s

def 