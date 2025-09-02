import numpy as np
import onnx
import onnxruntime as ort


# --------------------- 1. 检查ONNX模型 ---------------------
def check_onnx_model(model_path):
    """验证ONNX模型格式是否正确"""
    try:
        model = onnx.load(model_path)
        onnx.checker.check_model(model)
        print("✅ ONNX 模型检查通过")

        # 打印模型输入/输出信息
        print("\n📌 模型输入输出信息:")
        for input in model.graph.input:
            print(f"  输入名称: {input.name}, 形状: {input.type.tensor_type.shape}")
        for output in model.graph.output:
            print(f"  输出名称: {output.name}, 形状: {output.type.tensor_type.shape}")

        return model
    except Exception as e:
        print(f"❌ ONNX 模型检查失败: {e}")
        raise


# --------------------- 2. 数据预处理 ---------------------



# --------------------- 3. ONNX推理 ---------------------
def run_onnx_inference(model_path, input_data):
    """执行ONNX推理"""
    try:
        # 创建推理会话（可选GPU/CPU）
        providers = ["CPUExecutionProvider"]  # 优先使用GPU
        sess = ort.InferenceSession(model_path, providers=providers)

        # 获取输入名称
        input_name = sess.get_inputs()[0].name
        # 打印 ONNX 模型的输入信息
        for input in sess.get_inputs():
            print(f"Input name: {input.name}, Shape: {input.shape}, Type: {input.type}")
        # 对每一层执行推理并打印输出
        for layer in sess.get_outputs():
            layer_output = sess.run([layer.name], {input_name: input_data})
            print(f"Output name: {layer.name}, Output shape: {layer_output[0].shape}")
        # 运行推理
        outputs = sess.run(None, {input_name: input_data})

        print(f"🎯 推理完成，输出形状: {outputs[0].shape}")
        return outputs
    except Exception as e:
        print(f"❌ 推理失败: {e}")
        raise


# --------------------- 4. 结果后处理 ---------------------
def postprocess_output(output):
    """后处理输出结果（示例：分类任务取Top-5）"""
    probs = np.squeeze(output)  # 去除batch维度
    top_indices = np.argsort(probs)[-5:][::-1]  # 取概率最高的5个类别

    # 示例：假设是ImageNet类别（实际需替换为你的类别标签）
    imagenet_labels = [...]  # 这里应替换为实际的类别标签列表
    print("\n🏆 推理结果:")
    for i, idx in enumerate(top_indices):
        print(f"  {i + 1}. {imagenet_labels[idx]} (概率: {probs[idx]:.4f})")

    return top_indices

class net:
    def __init__(self,model_path,feature_num):
        self.net=check_onnx_model(model_path)
        self.model_path=model_path
        if feature_num==4:
            self.label=['健康','轻度抑郁','中度抑郁','重度抑郁']
        else:
            self.label=['健康','抑郁']
        # providers=["CUDAExecutionProvider"]
        self.sess = ort.InferenceSession(model_path)
        self.input_name = self.sess.get_inputs()[0].name
    def predict(self,x):
        try:
            x = np.reshape(x,(1,1,64,500))
        except Exception as e:
            print(f"❌ 数据预处理失败: {e}")

            return np.array([0.5,0.5])
        y = self.sess.run(None, {self.input_name: x})
        # y=run_onnx_inference(self.model_path, x)
        y = y[0][0]
        EEG_doctor = {}
        for i in range(len(y)):
            EEG_doctor[self.label[i]] = y[i]
        return EEG_doctor
# --------------------- 主程序 ---------------------
if __name__ == "__main__":
    # 配置路径和参数

    net1=net('model_cuda.onnx',4)

    x=np.random.randn(1,1,64,500).astype(np.float32)
    print(net1.predict(x))
    exit()

    ONNX_MODEL_PATH = "model_cuda.onnx"  # 替换为你的ONNX模型路径
    IMAGE_PATH = "test.jpg"  # 替换为测试图像路径
    INPUT_SHAPE = [1,1, 64, 500]  # 模型输入形状 [batch, channel, height, width]

    try:
        # 1. 检查模型
        model = check_onnx_model(ONNX_MODEL_PATH)

        # 2. 数据预处理
        input_data = np.random.randn(3, 1,64,500).astype(np.float32)

        # 3. 执行推理
        outputs = run_onnx_inference(ONNX_MODEL_PATH, input_data)

        # 4. 后处理结果
        postprocess_output(outputs[0])

    except Exception as e:
        print(f"🔴 主程序出错: {e}")