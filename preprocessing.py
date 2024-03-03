import jieba
import string
import re

class preprocessing:
    @staticmethod
    def pre_set_chinese(s):
        # 删除英文和中文标点符号
        en_punct = string.punctuation
        cn_punct = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
        all_punct = en_punct + cn_punct
        translator = str.maketrans('', '', all_punct)
        s = s.translate(translator).replace('\n', '')
        # 分词
        seg_list = jieba.cut(s, cut_all=False)
        # 连接成一个字符串并返回
        return ' '.join(seg_list)

    @staticmethod
    def pre_set_english(s):
        # 删除标点符号
        translator = str.maketrans('', '', string.punctuation)
        s = s.translate(translator).replace('\n', '')
        # 分词
        words = s.split()
        # 连接成一个字符串并返回
        return ' '.join(words)

    @staticmethod
    def pre_set_code(code):
        # 删除注释
        code = re.sub(r'#.*', '', code)
        # 删除空白行和额外的空格
        code = '\n'.join(line.strip() for line in code.split('\n') if line.strip())
        return code