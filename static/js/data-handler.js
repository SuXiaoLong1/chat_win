// data-handler.js
// 跟踪数据处理状态
const dataStatus = {
  eeg: { uploaded: false, processed: false },
  audio: { uploaded: false, processed: false },
  text: { uploaded: false, processed: false }
};

// 上传数据到后端
function uploadData(dataType) {
  const fileInput = document.getElementById(`${dataType}-upload`);
  const file = fileInput.files[0];
  const statusElement = document.getElementById(`${dataType}-status`);
  if (!file) {
    showStatus(statusElement, `请先选择${getDataTypeName(dataType)}文件`, 'error');
    return;
  }
  showStatus(statusElement, `正在上传 ${file.name}...`, 'processing');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('data_type', dataType);
  fetch('/get-data/api/upload-data', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      showStatus(statusElement, `文件 "${file.name}" 上传成功`, 'success');
      dataStatus[dataType].uploaded = true;
      const imgContainer = document.getElementById(`${dataType}-image`);
      const imgSrc = document.getElementById(`${dataType}-img-src`);
      console.log('预览URL:', result.preview_url);
      if (dataType === 'text' && result.wordcloud_url) {
        imgSrc.src = result.wordcloud_url;
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

// 使用示例数据
function useSampleData(dataType) {
  const statusElement = document.getElementById(`${dataType}-status`);
  const imgContainer = document.getElementById(`${dataType}-image`);
  const imgSrc = document.getElementById(`${dataType}-img-src`);
  showStatus(statusElement, `正在加载示例${getDataTypeName(dataType)}数据...`, 'processing');
  if (dataType === 'audio') {
    setTimeout(() => {
      imgSrc.src = `/static/users_body_datas/${dataType}.gif`;
      imgContainer.style.display = 'block';
      showStatus(statusElement, `示例${getDataTypeName(dataType)}数据加载完成`, 'success');
      dataStatus[dataType].uploaded = true;
    }, 800);
  } else if (dataType === 'eeg') {
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
function preprocessData(dataType) {
  if (!dataStatus[dataType].uploaded) {
    alert(`请先上传或加载${getDataTypeName(dataType)}数据`);
    return;
  }
  const statusElement = document.getElementById(`${dataType}-status`);
  const imgSrc = document.getElementById(`${dataType}-img-src`);
  showStatus(statusElement, `正在处理${getDataTypeName(dataType)}数据...`, 'processing');
  imgSrc.src = '/static/users_body_datas/processing.svg';
  setTimeout(() => {
    imgSrc.src = `/static/users_body_datas/${dataType}_preprocessed.svg`;
    showStatus(statusElement, `${getDataTypeName(dataType)}数据处理完成`, 'success');
    dataStatus[dataType].processed = true;
    checkAllProcessed();
  }, 1500);
}

// 生成词云
function generateWordCloud() {
  const textInput = document.getElementById('patient-text');
  const text = textInput.value.trim();
  const statusElement = document.getElementById('text-status');
  const imgContainer = document.getElementById('text-image');
  const imgSrc = document.getElementById('text-img-src');
  if (!text) {
    alert('请先在文本框中输入患者自述内容');
    return;
  }
  showStatus(statusElement, '正在生成词云分析...', 'processing');
  const formData = new FormData();
  formData.append('text_content', text);
  formData.append('data_type', 'text');
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
function runDetection() {
  if (!dataStatus.eeg.processed || !dataStatus.audio.processed) {
    alert('请先上传并处理EEG和音频数据');
    return;
  }
  const resultDiv = document.getElementById('result');
  resultDiv.className = 'processing';
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

// 辅助函数
function showStatus(element, message, type) {
  element.textContent = message;
  element.className = `status-message ${type}`;
}

function getDataTypeName(dataType) {
  const names = {
    eeg: 'EEG信号',
    audio: '音频',
    text: '文本'
  };
  return names[dataType] || dataType;
}

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
