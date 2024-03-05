import preprocessing as pre
import os

# 读取文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 保存文件
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
"""
词法分析

关键字标识符 1
变量名 2
数值 3
运算符 4 
其他 5
比如for(int i=0;i<10;i++){

}
翻译成
for -> 10
( -> 11
int -> 12
i -> 20
= -> 40
0 -> 30
; -> 50
i -> 20
< -> 41
10 -> 31
; -> 50
i -> 20
++ -> 42
) -> 13
{ -> 14
} -> 15

"""
def