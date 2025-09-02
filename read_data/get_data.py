from neuracle_api import DataServerThread
import time
import numpy as np
import parameters

sample_rate = parameters.sample_rate
t_buffer = parameters.t_buffer
thread_data_server = DataServerThread(sample_rate, t_buffer)
# 建立TCP/IP连接
notconnect = thread_data_server.connect(hostname='127.0.0.1', port=8712)
if notconnect:
    raise TypeError("Can't connect JellyFish, Please open the hostport ")
else:
    # meta包还没解析好就等待
    while not thread_data_server.isReady():
        time.sleep(1)
        continue
    # 启动线程
    thread_data_server.start()
    print('Data server start')

def get_data():
    data =  thread_data_server.GetBufferData()
    thread_data_server.ResetDataLenCount()
    return data