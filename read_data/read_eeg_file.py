import numpy as np
import pyedflib
import os
path=os.path.dirname(__file__)

def read_eeg(filename, target_samples=500):
    """
    自动识别 EDF/BDF 并读取，返回 (n_channels, target_samples) numpy array
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".edf", ".bdf"]:
        raise ValueError("文件扩展名必须是 .edf 或 .bdf")
    
    reader = pyedflib.EdfReader(filename)
    n_channels = reader.signals_in_file
    n_samples = reader.getNSamples()[0]
    
    data = np.zeros((n_channels, min(n_samples, target_samples)))
    for i in range(n_channels):
        signal = reader.readSignal(i)
        data[i, :] = signal[:target_samples]
    reader.close()
    
    return data
def get_data(filename=None):
    if filename is None:
        filename = os.path.join("raw_data/eeg", "eeg.bdf")

    eeg_data = read_eeg(filename)
    eeg_data = eeg_data.reshape(1, 1, eeg_data.shape[0], eeg_data.shape[1]).astype(np.float32)/50   #归一化
    return eeg_data

if __name__ == "__main__":


    # 自动读取 BDF
    bdf_data = read_eeg("random_auto.bdf")
    print("BDF 数据形状:", bdf_data.shape)

    # 自动读取 EDF
    edf_data = read_eeg("random_auto.edf")
    print("EDF 数据形状:", edf_data.shape)
