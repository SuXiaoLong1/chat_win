import os
import jieba
from wordcloud import WordCloud

import numpy as np
path=os.path.dirname(__file__)
class WordCloudGenerator:
    """词云图生成工具类"""

    def __init__(self, output_dir, font_path="C:/Windows/Fonts/simhei.ttf"):
        """
        初始化词云生成器
        :param output_dir: 词云图保存目录
        :param font_path: 中文字体路径（确保存在）
        """
        self.output_dir = output_dir
        self.font_path = font_path
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_from_text(self, text, base_filename):
        """
        从文本内容生成词云图
        :param text: 文本内容
        :param base_filename: 基础文件名（用于生成词云文件名）
        :return: 词云图文件名（含路径）
        """
        if not text.strip():
            raise ValueError("文本内容不能为空")
        
        # 中文分词
        seg_list = jieba.cut(text, cut_all=False)
        processed_text = " ".join(seg_list)
        
        # 创建词云对象
        wc = WordCloud(
            font_path=self.font_path,
            background_color="white",
            max_words=200,
            width=800,
            height=600,
            contour_width=1,
            contour_color='steelblue'
        )
        
        # 生成词云
        wc.generate(processed_text)
        
        # 保存词云图
        wordcloud_filename = f"{os.path.splitext(base_filename)[0]}_cloud.png"
        wordcloud_path = os.path.join(self.output_dir, wordcloud_filename)
        wc.to_file(wordcloud_path)
        
        return wordcloud_filename
    
    def generate_from_file(self, file_path, base_filename=None):
        """
        从文本文件生成词云图
        :param file_path: 文本文件路径
        :param base_filename: 基础文件名（默认使用原文件名）
        :return: 词云图文件名（含路径）
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 读取文本内容
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 若未指定基础文件名，则使用原文件名
        if not base_filename:
            base_filename = os.path.basename(file_path)
            
        return self.generate_from_text(text, base_filename)
if __name__ == '__main__':
    # 示例用法
    output_directory = os.path.join(path, "test_output")  # 词云图保存目录
    text_cloud_generator = WordCloudGenerator(output_directory)

    # 从文本生成词云图
    sample_text = "这是一个用于生成词云图的示例文本"
    text_cloud_generator.generate_from_text(sample_text, "sample_text")

    # 从文件生成词云图
    text_cloud_generator.generate_from_file("f:/python/visualization/chat_win/raw_data/text/text.txt")