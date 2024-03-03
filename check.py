import gradio as gr
import preprocessing as pre # 预处理函数

def ngrams(input, n): #集合处理
    input = input.split(' ')
    output = set()
    for i in range(len(input) - n + 1):
        output.add(' '.join(input[i:i+n]))
    return output

def process_text(text1, text2, method, n):
    pre_obj = pre.preprocessing()
    result1 = result2 = None  # Default assignment
    # 根据method处理两个文本输入
    if method == 'Chinese':
        result1 = pre_obj.pre_set_chinese(text1)
        result2 = pre_obj.pre_set_chinese(text2)
    elif method == 'English':
        result1 = pre_obj.pre_set_english(text1)
        result2 = pre_obj.pre_set_english(text2)
    elif method == 'Code':
        result1 = pre_obj.pre_set_code(text1)
        result2 = pre_obj.pre_set_code(text2)
    # 根据n的值把result1 和result2的值放进两个hash表中
    ngrams1 = ngrams(result1, n)
    ngrams2 = ngrams(result2, n)
    # 如果集合的大小小于n，返回错误消息和0的重复率

    #调试用
    print(ngrams1)
    print(ngrams2)

    if len(ngrams1) < n or len(ngrams2) < n:
        return "n太大了或文本值太小了", "n太大了或文本值太小了", 0
    if len(ngrams1) == 0 or len(ngrams2) == 0:
        return "文本为空", "文本为空", 0

    # 计算重复率
    intersection = ngrams1.intersection(ngrams2)
    # 两个集合的并集
    union = ngrams1.union(ngrams2)
    # 重复率
    similarity = len(intersection) / len(union) if len(union) != 0 else 0

    # 创建HighlightedText对象
    result1 = ' '.join(word if word in intersection else word for word in result1.split())
    result2 = ' '.join(word if word in intersection else word for word in result2.split())
    
    # 返回两个结果和重复率
    return result1, result2, similarity


if __name__ == "__main__":
    iface = gr.Interface(fn=process_text, 
                         inputs=[gr.Textbox(lines=5, placeholder='Input 1 here...'), 
                                 gr.Textbox(lines=5, placeholder='Input 2 here...'), 
                                 gr.Radio(['Chinese', 'English', 'Code']),
                                 gr.Slider(minimum=1, maximum=20, step=1)],
                         outputs=[gr.Textbox(), gr.Textbox(),gr.Textbox()])
    iface.launch()