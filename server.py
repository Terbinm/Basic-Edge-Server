# server.py
from flask import Flask, request, jsonify, render_template
import logging,os

app = Flask(__name__)

# 設定日誌
logging.basicConfig(filename='app.log', level=logging.INFO)

# 儲存裝置狀態的字典
device_status = {}

@app.route('/input/<client_id>/<session_id>/', methods=['POST'])
def receive_file(client_id,session_id):
    print("received")
    file = request.files['file']
    current_path = os.getcwd()
    directoryID = os.path.join(current_path, "input", client_id)
    print(directoryID)
    if not os.path.exists(directoryID):
        os.makedirs(directoryID)
        print("New clientID, created")

    finaldir = os.path.join(directoryID,session_id)
    if not os.path.exists(finaldir):
        os.makedirs(finaldir)
        print("New session, created")
    save_path = os.path.join(finaldir, file.filename)
    file.save(save_path)
    return "File received!", 200

@app.route('/status', methods=['POST'])
def status():
    data = request.get_json()
    device_status[data['device_id']] = {'status': data['status'], 'timestamp': data['timestamp']}
    print(device_status)
    app.logger.info(f"Received status from device {data['device_id']}: {data['status']} at {data['timestamp']}")
    return jsonify({'message': 'Status received'}), 200

@app.route('/status_return/', methods=['GET'])
def status_return():
    return jsonify(device_status), 200

@app.route('/main/', methods=['GET'])
def home():
    return render_template('home.html', device_status=device_status)

# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9999)
