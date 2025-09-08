## 模型文件下载

由于空间和 GitHub 限制，`model.onnx` 和 `mdra` 等大文件未包含在仓库中。请用户自行下载并放置到指定目录。

模型下载链接（请后续补充）：

- [model.onnx 下载地址](https://drive.google.com/file/d/12Jbja3L8KJzI0mHAt0QxV48MNP11RuyN/view?usp=sharing)
  - 下载后请将 `model.onnx` 文件放置于项目根目录下的 `model/` 文件夹：
    ```
    chat_win/
    └── model/
          └── model.onnx
    ```
- [mdra 下载地址](https://drive.google.com/file/d/17Py03Z55WAk7MSWEOVWTtIyUZvFytixG/view?usp=sharing)
  - 下载后请将 `mdra` 相关文件放置于项目根目录下的 `mdraModel/` 文件夹：
    ```
    chat_win/
    └── mdraModel/
          └── <mdra 文件>
    ```

# chat_win

## 项目简介

chat_win 是一个基于 Flask 的多模态数据处理与分析平台，支持 EEG（脑电）、音频、文本等多种数据的上传、预处理和可视化。平台集成了深度学习模型，可用于抑郁症等心理健康检测，适用于科研、医疗和心理健康数据分析场景。

## 主要功能

- 支持 EEG、音频、文本数据的上传与格式校验
- 文本词云自动生成与可视化
- EEG/音频/文本特征提取与分析
- 综合检测报告自动生成
- 友好的前端页面

## 安装与运行

1. 克隆仓库：
   ```sh
   git clone https://github.com/SuXiaoLong1/chat_win.git
   ```
2. 安装依赖：
   ```sh
   pip install -r requirements.txt
   ```
3. 启动服务：
   ```sh
   python main.py
   ```

## 目录结构

```
chat_win/
├── main.py                # 主程序入口
├── Get_data.py            # 数据上传与处理接口
├── process_data/          # 数据处理模块
├── deepseek_api/          # 深度学习/AI相关接口
├── mdraModel/             # 抑郁症检测模型
├── static/                # 前端静态资源
├── templates/             # 前端页面模板
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

## 适用场景

- 科研数据分析
- 医疗辅助诊断
- 心理健康评估

# chat_win

This project  supports uploading, preprocessing, and visualization of EEG, audio, and text data. Users can upload files or input text directly on the frontend, and the backend provides automatic word cloud generation and comprehensive depression analysis using deep learning models.

# 安装依赖：

conda create python==3.9 -n name

conda activate name

conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1 -c pytorch -c nvidia

conda install flask requests jieba numpy openai

conda install librosa tensorflow==2.12.0 resampy tf_slim six onnx onnxruntime

pip install elmoformanylangs
