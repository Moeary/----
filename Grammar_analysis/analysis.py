import pandas as pd

def addtwodimdict(thedict, key_a, key_b, val): 
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})
# 读取CSV文件
table = pd.read_csv('table1.csv', skiprows=0)

# 初始化字典
action = dict()
goto = dict()

# 遍历每一行和每一列
for i, row in table.iterrows():
    for j, cell in enumerate(row):
        if pd.notnull(cell):  # 如果单元格非空
            # 获取状态和符号
            state = i
            symbol = table.columns[j]

            # 根据单元格的值决定是添加到action字典还是goto字典
            if cell.startswith('s') or cell.startswith('r') or cell == 'acc':
                addtwodimdict(action, state, symbol, cell)
            else:
                addtwodimdict(goto, state, symbol, cell)
# 遍历并打印action字典
print("Action Dictionary:")
for state, transitions in action.items():
    for symbol, action in transitions.items():
        print(f"addtwodimdict(action, {state}, '{symbol}', '{action}')")

# 遍历并打印goto字典
print("\nGoto Dictionary:")
for state, transitions in goto.items():
    for symbol, goto_state in transitions.items():
        print(f"addtwodimdict(goto, {state}, '{symbol}', {goto_state})")

sen='i*i+i$'
ip=0#sen的指针
stack=['$',0]
a=sen[ip]
while True:
    print(stack)
    print(action)
    s=stack[len(stack)-1] #s为栈顶状态
    s_str = str(s)  # Convert s to string
    if s_str not in action:
        print(f"Error: No actions for state {s}")
        break
    if a not in action[s_str]:
        print(f"Error: No action for symbol {a} in state {s}")
        break
    elif  a in action[s]:#存在action[s][a]
        if action[s][a]=='acc': #若为acc 则成功，并结束
            print('ana succeess')
            break
        elif action[s][a][0]=='s':#若为 si 则把a和i依次入栈 a指向下一个
            print('移进'+action[s][a])
            t=int(action[s][a][1])
            stack.append(a)
            stack.append(t)
            ip+=1
            a=sen[ip]
        elif action[s][a][0]=='r':#若为ri i为第i个文法（gramma[i-1]） 则栈回退2*gramma[i-1]表达式表达式右端的长度
            print('规约'+gramma[int(action[s][a][1])-1][0:1]+'->'+gramma[int(action[s][a][1])-1][1:])
            size=len(gramma[int(action[s][a][1])-1])-1 #rj 对应的第j个产生式右端的长度
            j=0
            while j<2*size:
                stack.pop()
                j+=1
            t=stack[len(stack)-1]#t为现在栈的状态
            stack.append(gramma[int(action[s][a][1])-1][0])#表达式左端入栈
            stack.append(goto[t][gramma[int(action[s][a][1])-1][0]])#goto[t,表达式左端]入栈
            print(gramma[int(action[s][a][1])-1])#输出产生式
        else:
            #调用错误恢复例程
            print('error')