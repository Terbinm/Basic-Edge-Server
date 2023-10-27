# server.py
from flask import Flask, request, jsonify, render_template
import logging, os

app = Flask(__name__)

# 設定日誌
logging.basicConfig(filename='app.log', level=logging.INFO)

# 儲存裝置狀態的字典
device_status = {}

# 定義裝置類別
class Device:
    def __init__(self, device_id, device_type):
        # 初始化裝置屬性
        self.device_id = device_id
        self.device_type = device_type
        self.status = None
        self.streamingdata = None
        self.outdir = ''
        self.timestamp = None
        self.streaming_file = ''

    # 更新裝置狀態的方法
    def update_status(self, status, timestamp, streaming_file, streamingdata=None):
        self.status = status
        self.timestamp = timestamp
        if streamingdata is not None:
            self.streamingdata = streamingdata
            self.streaming_file = streaming_file

@app.route('/status', methods=['POST'])
def status():
    data = request.get_json()
    device_id = data['device_id']
    if device_id not in device_status:
        # 如果裝置不存在，則創建新的裝置物件並添加到字典中
        device_status[device_id] = Device(device_id, data['device_type'])
    # 獲取音樂檔案列表並更新裝置狀態
    music_files = [f for f in os.listdir('static/music') if f.endswith('.wav')]
    device_status[device_id].update_status(data['status'], data['streamingdata'], data['timestamp'], music_files)
    app.logger.info(f"Received status from device {device_id}: {data['status']} at {data['timestamp']}")
    return jsonify({'message': 'Status received'}), 200

@app.route('/status_return/', methods=['GET'])
def status_return():
    # 返回所有裝置的狀態，將每個 Device 物件轉換為字典以便轉換為 JSON
    return jsonify({device_id: vars(device) for device_id, device in device_status.items()}), 200

# 其他的程式碼...

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9997)
