from flask import Blueprint, render_template, request, jsonify, url_for, Flask
import os
from werkzeug.utils import secure_filename
from mdraModel import create_sample_config as create_text_audio_config
from mdraModel import mdraModel
from model.onnxmodel import net
from read_data.read_eeg_file import get_data as upload_data
# from read_data.get_data import get_data as hardware_data 
import pyedflib
# 导入独立的词云生成工具
from process_data.text_cloud import WordCloudGenerator
path = os.path.dirname(os.path.abspath(__file__))
text="mdraModel/sample/neutral.txt"
audio="mdraModel/sample/neutral_out.wav"
ONNX_MODEL_PATH = os.path.join(path, "model/model.onnx")  # ONNX模型路径


create_text_audio_config(text=os.path.join(path, text), audio=os.path.join(path, audio))

net1=net(ONNX_MODEL_PATH,4)
# 创建蓝图（子页面模块）
getdata_bp = Blueprint('getdata', __name__, url_prefix='/get-data', 
                       template_folder='templates',
                       static_folder='static')

# 配置：上传路径和允许的文件类型
UPLOAD_CONFIG = {
    'eeg': os.path.join(os.path.dirname(__file__), 'raw_data', 'eeg'),
    'audio': os.path.join(os.path.dirname(__file__),'raw_data', 'audio'),
    'text': os.path.join(os.path.dirname(__file__), 'raw_data', 'text')
}

# 词云图保存路径
WORDCLOUD_PATH = os.path.join(os.path.dirname(__file__), 'static', 'users_body_datas', 'wordclouds')

ALLOWED_EXTENSIONS = {
    'eeg': {'edf','bdf'},
    'audio': {'wav'},
    'text': {'txt'}
}

# 初始化词云生成器（全局实例，避免重复创建）
# 注意：根据系统字体路径调整 font_path
wordcloud_generator = WordCloudGenerator(
    output_dir=WORDCLOUD_PATH
    
)

# 确保所有必要目录存在
for path in UPLOAD_CONFIG.values():
    os.makedirs(path, exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'users_body_datas'), exist_ok=True)

def allowed_file(filename, data_type):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(data_type, set())


@getdata_bp.route('/')
def index():
    """子页面入口"""
    return render_template('get-data.html')

@getdata_bp.route('/api/upload-data', methods=['POST'])
def upload_data():
    """处理文件上传请求，文本文件自动生成词云"""
    try:
        file = request.files.get('file')
        data_type = request.form.get('data_type')
        # print(f"接收上传请求，文件：{file}, 数据类型：{data_type}")
        # 基础校验
        if not file or not data_type:
            return jsonify({'success': False, 'msg': '缺少文件或数据类型参数'})
        
        if data_type not in UPLOAD_CONFIG:
            return jsonify({'success': False, 'msg': f'不支持的数据类型：{data_type}'})
        
        if file.filename == '':
            return jsonify({'success': False, 'msg': '未选择文件'})
        
        if not allowed_file(file.filename, data_type):
            allowed_ext = ','.join(ALLOWED_EXTENSIONS[data_type])
            return jsonify({'success': False, 'msg': f'仅支持以下格式：{allowed_ext}'})
        
        # 安全保存文件
        # filename = secure_filename(file.filename)

        # print(f"上传文件：{file.filename}，保存路径：{save_path}")
        # 文本文件特殊处理：调用独立词云工具生成词云
        wordcloud_url = None
        if data_type == 'text':
            try:
                filename="text.txt"
                save_path = os.path.join(UPLOAD_CONFIG[data_type], filename)
                file.save(save_path)
                print(f"生成词云图，输入文件：{save_path}")
                # 调用词云生成器（从文件生成）
                wordcloud_filename = wordcloud_generator.generate_from_file(save_path)
                # 生成词云图URL
                wordcloud_url = url_for('static', 
                                      filename=f'users_body_datas/wordclouds/{wordcloud_filename}')
            except Exception as e:
                print(f"词云生成失败：{str(e)}")
                return jsonify({'success': False, 'msg': f'词云生成失败：{str(e)}'})
        elif data_type =='eeg':
            try:
                filename=file.filename.split('.')[-1]
                filename=f"eeg.{filename}"
                save_path = os.path.join(UPLOAD_CONFIG[data_type], filename)
                file.save(save_path)
                # print(f"生成EEG预览图，输入文件：{save_path}")
                # 调用EEG预处理函数
                # preview_url = 'static/users_body_datas/eeg.svg'
            except Exception as e:
                print(f"EEG预处理失败：{str(e)}")
                return jsonify({'success': False, 'msg': f'EEG预处理失败：{str(e)}'})
        elif data_type =='audio':
            try:
                filename=file.filename.split('.')[-1]
                filename=f"audio.{filename}"
                save_path = os.path.join(UPLOAD_CONFIG[data_type], filename)
                file.save(save_path)
                # print(f"生成音频预览图，输入文件：{save_path}")
                # 调用音频预处理函数
                # preview_url = 'static/users_body_datas/audio.gif'
            except Exception as e:
                print(f"音频预处理失败：{str(e)}")
                return jsonify({'success': False, 'msg': f'音频预处理失败：{str(e)}'})
        # 生成预览图URL
        if data_type == 'text' and wordcloud_url:
            preview_url = wordcloud_url  # 文本文件预览图使用新词云
        elif data_type == 'audio':
            preview_url = url_for('getdata.static', 
                                filename=f'users_body_datas/{data_type}.gif')
        elif data_type == 'eeg':
            preview_url = url_for('getdata.static', 
                                filename=f'users_body_datas/{data_type}.svg')
        print({
            'success': True,
            'msg': f'文件 "{filename}" 上传成功',
            'preview_url': preview_url,
            'save_path': save_path,
            'wordcloud_url': wordcloud_url
        })
        return jsonify({
            'success': True,
            'msg': f'文件 "{filename}" 上传成功',
            'preview_url': preview_url,
            'save_path': save_path,
            'wordcloud_url': wordcloud_url
        })

    except Exception as e:
        
        return jsonify({'success': False, 'msg': f'上传失败：{str(e)}'})

@getdata_bp.route('/api/generate-wordcloud', methods=['POST'])
def preprocess_data():
    """处理上传的数据"""
    try:
    # if True:
        # 获取文本内容和数据类型
        text = request.form.get('text_content')
        data_type = request.form.get('data_type')
        if not text or not data_type:
            return jsonify({'success': False, 'msg': '缺少文本内容或数据类型'})
        # 只支持 text 类型
        if data_type != 'text':
            return jsonify({'success': False, 'msg': '仅支持文本词云生成'})
        # 生成词云图片
        wordcloud_filename = wordcloud_generator.generate_from_text(text, 'input_text')
        wordcloud_url = url_for('static', filename=f'users_body_datas/wordclouds/{wordcloud_filename}')
        return jsonify({'success': True, 'msg': '词云生成完成', 'wordcloud_url': wordcloud_url})
    except Exception as e:
        return jsonify({'success': False, 'msg': f'处理失败：{str(e)}'})

@getdata_bp.route('/api/predict', methods=['POST'])
def predict():
    """进行抑郁症检测预测"""
    try:
        text="raw_data/text/text.txt"
        audio="raw_data/audio/audio.wav"
        path = os.path.dirname(os.path.abspath(__file__))


        create_text_audio_config(text=os.path.join(path, text), audio=os.path.join(path, audio))
        # 获取上传的EEG、音频和文本数据
        
        EEG_doctor = net1.predict(upload_data())
        text_audio_doctor = mdraModel()


        result_data = "<p><strong>抑郁症检测分析报告</strong></p>" \
        f"<p>1. EEG信号分析：患者抑郁症可能性为 <strong>{1-EEG_doctor['健康']:.2f}</strong></p>" \
        f"<p>2. 音频特征分析：语音语调平缓，可能性为 <strong>{1-text_audio_doctor['healthy_probability']:.2f}</strong></p>" \
        f"<p>3. 文本语义分析：自述内容，可能性为 <strong>{1-text_audio_doctor['healthy_probability']:.2f}</strong></p>"

        r1="这是我的抑郁症检测分析报告\n"\
        f"1. EEG信号分析：患者抑郁症可能性为{1-EEG_doctor['健康']:.2f}\n"\
        f"2. 音频特征分析：语音语调平缓，可能性为{1-text_audio_doctor['healthy_probability']:.2f}\n"\
        f"3. 文本语义分析：自述内容，可能性为{1-text_audio_doctor['healthy_probability']:.2f}\n"
        if EEG_doctor['健康'] < 0.2 or text_audio_doctor['healthy_probability'] < 0.2:
            result_data += "<p><strong>综合评估：</strong>患者存在明显抑郁倾向，建议尽快就医。</p>"
            r1+="患者存在明显抑郁倾向，建议尽快就医。"
        elif EEG_doctor['健康'] < 0.3 or text_audio_doctor['healthy_probability'] < 0.3:
            result_data += "<p><strong>综合评估：</strong>患者存在一定的抑郁倾向，建议进行心理咨询。</p>"
            r1+="患者存在一定的抑郁倾向，建议进行心理咨询。"
        elif EEG_doctor['健康'] < 0.5 or text_audio_doctor['healthy_probability'] < 0.5:
            result_data += "<p><strong>综合评估：</strong>患者存在轻度抑郁倾向，建议进一步临床诊断确认。</p>"
            r1+="患者存在轻度抑郁倾向，建议进一步临床诊断确认。"
        else:
            result_data += "<p><strong>综合评估：</strong>患者没有明显抑郁倾向，建议继续保持健康 lifestyle。</p>"
            r1+="患者没有明显抑郁倾向，建议继续保持健康 lifestyle。"
        # TODO: 调用模型进行预测
        # 假设你的字符串

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(r1)

        print("保存完成: result.txt")



        return jsonify({
            'success': True,
            'msg': '预测完成',
            'result': result_data  # 核心预测结果，供前端解析
        })
    except Exception as e:
        return jsonify({'success': False, 'msg': f'预测失败：{str(e)}'})
@getdata_bp.route('/api/eeg_from_hardware', methods=['GET'])
def get_eeg_from_hardware():
    """从硬件获取EEG数据"""
    try:
        # TODO: 实现从硬件获取EEG数据的逻辑
        eeg_data = hardware_data()
        # BDF 文件保存路径
        bdf_path = 'raw_data/eeg/eeg.bdf'

        # 创建 BDF 文件
        f = pyedflib.EdfWriter(
            bdf_path,
            n_channels=64,
            file_type=pyedflib.FILETYPE_BDF
        )

        # 通道信息（可根据实际情况调整）
        channel_info = []
        for i in range(64):
            ch_dict = {
                'label': f'Ch{i+1}',
                'dimension': 'uV',
                'sample_rate': 250,
                'physical_min': -1000,
                'physical_max': 1000,
                'digital_min': -8388608,
                'digital_max': 8388607,
                'transducer': '',
                'prefilter': ''
            }
            channel_info.append(ch_dict)

        f.setSignalHeaders(channel_info)
        f.writeSamples(eeg_data)
        f.close()
        return jsonify({'success': True, 'eeg_data': eeg_data})
    except Exception as e:
        return jsonify({'success': False, 'msg': f'获取EEG数据失败：{str(e)}'})

def init_app(app):
    """在主应用中注册蓝图"""
    app.register_blueprint(getdata_bp)

if __name__ == "__main__":
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    test_app.config['DEBUG'] = True
    init_app(test_app)
    
    print("="*50)
    print("Getdata子页面测试模式启动")
    print(f"访问地址: http://127.0.0.1:5000/get-data")
    print(f"文件上传接口: http://127.0.0.1:5000/get-data/api/upload-data")
    print(f"上传文件将保存至: {UPLOAD_CONFIG}")
    print(f"词云图将保存至: {WORDCLOUD_PATH}")
    print("="*50)
    
    test_app.run(host='0.0.0.0', port=5000)
