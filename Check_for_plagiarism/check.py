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

    """
    print(ngrams1)
    print(ngrams2)
    """

    # 如果集合的大小小于n，返回错误消息和0的重复率
    if len(ngrams1) < n or len(ngrams2) < n:
        return [{"text": "n太大了或文本值太小了", "class": None}], [{"text": "n太大了或文本值太小了", "class": None}], 0
    # 计算重复率
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    similarity = len(intersection) / len(union) if len(union) != 0 else 0

    # 打印集合
    print(intersection)
    print(union)

    print(result1)
    print(result2)
    
    # 创建输出字符串
    result1 = ' '.join([f'{{{ngram}, red}}' if ngram in intersection else f'{{{ngram}, none}}' for ngram in ngrams(result1, n)])
    result2 = ' '.join([f'{{{ngram}, red}}' if ngram in intersection else f'{{{ngram}, none}}' for ngram in ngrams(result2, n)])
    # 返回两个结果和重复率
    return result1, result2, similarity

if __name__ == "__main__":
    iface = gr.Interface(fn=process_text, 
                         inputs=[gr.Textbox(lines=5, placeholder='Input 1 here...'), 
                                 gr.Textbox(lines=5, placeholder='Input 2 here...'), 
                                 gr.Radio(['Chinese', 'English', 'Code']),
                                 gr.Slider(minimum=1, maximum=20, step=1)],
                         outputs=[gr.Textbox(), gr.Textbox(), gr.Textbox()])
    iface.launch()