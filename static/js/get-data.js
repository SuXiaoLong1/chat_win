// 等待DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 跟踪数据处理状态
    const dataStatus = {
        eeg: { uploaded: false, processed: false },
        audio: { uploaded: false, processed: false },
        text: { uploaded: false, processed: false }
    };
    
    // 上传数据到后端
    window.uploadData = function(dataType) {
        const fileInput = document.getElementById(`${dataType}-upload`);
        const file = fileInput.files[0];
        const statusElement = document.getElementById(`${dataType}-status`);
        
        if (!file) {
            showStatus(statusElement, `请先选择${getDataTypeName(dataType)}文件`, 'error');
            return;
        }
        
        // 显示上传中状态
        showStatus(statusElement, `正在上传 ${file.name}...`, 'processing');
        
        // 创建FormData对象
        const formData = new FormData();
        formData.append('file', file);
        formData.append('data_type', dataType);
        
        // 发送请求到后端 - 修复路径，添加蓝图前缀
        fetch('/get-data/api/upload-data', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                showStatus(statusElement, `文件 "${file.name}" 上传成功`, 'success');
                dataStatus[dataType].uploaded = true;
                
                // 显示上传的文件预览
                const imgContainer = document.getElementById(`${dataType}-image`);
                const imgSrc = document.getElementById(`${dataType}-img-src`);
                console.log('预览URL:', result.preview_url);
                // 文本文件特殊处理：显示生成的词云图
                if (dataType === 'text' && result.wordcloud_url) {
                    imgSrc.src = result.wordcloud_url;
                    // 同时更新词云图显示区域
                    const wordcloudImg = document.getElementById('wordcloud-img-src');
                    if (wordcloudImg) {
                        wordcloudImg.src = result.wordcloud_url;
                        document.getElementById('wordcloud-image').style.display = 'block';
                    }
                } else {
                    imgSrc.src = result.preview_url || `/static/users_body_datas/${dataType}.svg`;
                }
                imgContainer.style.display = 'block';
            } else {
                showStatus(statusElement, `上传失败: ${result.msg}`, 'error');
            }
        })
        .catch(error => {
            showStatus(statusElement, `上传出错: 请重试`, 'error');
            console.error('上传错误:', error);
        });
    }
    // 从硬件获取数据（适配后端 /api/eeg_from_hardware 接口）
    window.get_hardware_data = function(dataType) {
        // 仅支持 EEG 类型（后端接口仅处理 EEG，如需扩展需后端同步支持）
        if (dataType !== 'eeg') {
            const statusElement = document.getElementById(`${dataType}-status`);
            showStatus(statusElement, `暂不支持从硬件获取${getDataTypeName(dataType)}数据`, 'error');
            return;
        }

        const statusElement = document.getElementById(`${dataType}-status`);
        const imgContainer = document.getElementById(`${dataType}-image`); // EEG 预览容器
        const imgSrc = document.getElementById(`${dataType}-img-src`);     // EEG 预览图片

        // 1. 显示“获取中”状态
        showStatus(statusElement, `正在从硬件获取${getDataTypeName(dataType)}数据...`, 'processing');
        imgSrc.src = '/static/users_body_datas/processing.svg'; // 加载中动画
        imgContainer.style.display = 'block'; // 显示预览区域

        // 2. 调用后端硬件数据接口（GET 方法，与后端路由一致）
        fetch('/get-data/api/eeg_from_hardware', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // 若需用户认证，可添加 Token（如 JWT）
                // 'Authorization': `Bearer ${sessionStorage.getItem('token')}`
            }
        })
        .then(response => {
            // 处理 HTTP 状态码（如 404、500）
            if (!response.ok) {
                throw new Error(`接口请求失败（状态码：${response.status}）`);
            }
            return response.json(); // 解析后端返回的 JSON 数据
        })
        .then(result => {
            // 3. 处理接口成功响应
            if (result.success) {
                // 更新状态：标记 EEG 已上传（可后续处理）
                dataStatus[dataType].uploaded = true;
                
                // 显示成功提示
                showStatus(statusElement, `${getDataTypeName(dataType)}数据从硬件获取完成`, 'success');
                
                // 4. 预览处理：后端若返回 BDF 文件访问链接，可展示（需前端支持 BDF 预览）
                // （注：BDF 是二进制脑电文件，前端直接预览需第三方库，如 `bdfjs`）
                if (result.bdf_preview_url) {
                    imgSrc.src = result.bdf_preview_url; // 后端生成的预览图（如波形图）
                } else {
                    // 若无预览图，显示默认 EEG 图标
                    imgSrc.src = `/static/users_body_datas/${dataType}.svg`;
                }
            } else {
                // 5. 处理接口业务失败（如硬件连接失败）
                showStatus(statusElement, `获取失败：${result.msg}`, 'error');
                imgSrc.src = `/static/users_body_datas/${dataType}_error.svg`; // 错误图标
            }
        })
        .catch(error => {
            // 6. 处理网络异常（如断网、跨域错误）
            console.error('硬件数据获取错误：', error);
            showStatus(statusElement, `获取出错：${error.message}`, 'error');
            imgSrc.src = `/static/users_body_datas/${dataType}_error.svg`;
        });
    }

    // 使用示例数据
    window.useSampleData = function(dataType) {
        const statusElement = document.getElementById(`${dataType}-status`);
        const imgContainer = document.getElementById(`${dataType}-image`);
        const imgSrc = document.getElementById(`${dataType}-img-src`);
        
        showStatus(statusElement, `正在加载示例${getDataTypeName(dataType)}数据...`, 'processing');
        if (dataType === 'audio') {
            // 模拟加载示例数据
            setTimeout(() => {
                imgSrc.src = `/static/users_body_datas/${dataType}.gif`;
                imgContainer.style.display = 'block';
                showStatus(statusElement, `示例${getDataTypeName(dataType)}数据加载完成`, 'success');
                dataStatus[dataType].uploaded = true;
            }, 800);
        } else if (dataType === 'eeg') {
            // 模拟加载示例数据
            setTimeout(() => {
                imgSrc.src = `/static/users_body_datas/${dataType}.svg`;
                imgContainer.style.display = 'block';
                showStatus(statusElement, `示例${getDataTypeName(dataType)}数据加载完成`, 'success');
                dataStatus[dataType].uploaded = true;
            }, 800);
        } else {
            showStatus(statusElement, `不支持的示例数据类型: ${dataType}`, 'error');
        }
    }
    
    // 处理数据
    window.preprocessData = function(dataType) {
        if (!dataStatus[dataType].uploaded) {
            alert(`请先上传或加载${getDataTypeName(dataType)}数据`);
            return;
        }
        
        const statusElement = document.getElementById(`${dataType}-status`);
        const imgSrc = document.getElementById(`${dataType}-img-src`);
        
        showStatus(statusElement, `正在处理${getDataTypeName(dataType)}数据...`, 'processing');
        imgSrc.src = '/static/users_body_datas/processing.svg';

        // 模拟数据处理过程
        setTimeout(() => {
            imgSrc.src = `/static/users_body_datas/${dataType}_preprocessed.svg`;
            showStatus(statusElement, `${getDataTypeName(dataType)}数据处理完成`, 'success');
            dataStatus[dataType].processed = true;
            
            // 检查是否所有数据都已处理
            checkAllProcessed();
        }, 1500);
    }
    
    // 生成词云 - 支持直接从文本框输入生成
    window.generateWordCloud = function() {
        const textInput = document.getElementById('patient-text');
        const text = textInput.value.trim();
        const statusElement = document.getElementById('text-status');
        const imgContainer = document.getElementById('text-image');
        const imgSrc = document.getElementById('text-img-src');
        
        // 检查是否有文本输入
        if (!text) {
            alert('请先在文本框中输入患者自述内容');
            return;
        }
        
        showStatus(statusElement, '正在生成词云分析...', 'processing');
        
        // 创建FormData对象发送文本内容
        const formData = new FormData();
        formData.append('text_content', text);
        formData.append('data_type', 'text');
        
        // 发送请求生成词云
        fetch('/get-data/api/generate-wordcloud', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                console.log('词云生成成功:', result);
                imgSrc.src = result.wordcloud_url;
                imgContainer.style.display = 'block';
                showStatus(statusElement, '词云分析生成完成', 'success');
                dataStatus.text.uploaded = true;
                dataStatus.text.processed = true;
                checkAllProcessed();
            } else {
                showStatus(statusElement, `词云生成失败: ${result.msg}`, 'error');
            }
        })
        .catch(error => {
            showStatus(statusElement, '词云生成出错，请重试', 'error');
            console.error('词云生成错误:', error);
        });
    }
    
    // 运行检测
    window.runDetection = function() {
        // 检查是否所有必要数据都已处理
        if (!dataStatus.eeg.processed || !dataStatus.audio.processed) {
            alert('请先上传并处理EEG和音频数据');
            return;
        }
        
        const resultDiv = document.getElementById('result');
        resultDiv.className = 'processing';
        
        // 调用后端 /api/predict 接口
        fetch('/get-data/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: sessionStorage.getItem('user_id'),
                eeg_processed: dataStatus.eeg.processed,
                audio_processed: dataStatus.audio.processed
            })
        })
        .then(response => response.json())
        .then(res => {
            if (res.success) {
                const result = res.result;
                resultDiv.className = 'success';
                resultDiv.innerHTML = res.result;
            } else {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `<p>检测失败：${res.msg}</p>`;
            }
        })
        .catch(error => {
            resultDiv.className = 'error';
            resultDiv.innerHTML = `<p>网络异常：检测请求发送失败，请重试</p>`;
            console.error('检测接口错误：', error);
        });      
    }
    
    // 辅助函数：显示状态信息
    function showStatus(element, message, type) {
        element.textContent = message;
        element.className = `status-message ${type}`;
    }
    
    // 辅助函数：获取数据类型名称
    function getDataTypeName(dataType) {
        const names = {
            eeg: 'EEG信号',
            audio: '音频',
            text: '文本'
        };
        return names[dataType] || dataType;
    }
    
    // 检查是否所有数据都已处理
    function checkAllProcessed() {
        const allProcessed = dataStatus.eeg.processed && 
                            dataStatus.audio.processed && 
                            dataStatus.text.processed;
                            
        if (allProcessed) {
            const resultDiv = document.getElementById('result');
            resultDiv.className = 'success';
            resultDiv.textContent = '所有数据已处理完成，可以开始综合检测分析';
        }
    }
});
