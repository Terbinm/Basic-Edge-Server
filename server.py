# server.py
from flask import Flask, request, jsonify, render_template
import logging,os,glob

app = Flask(__name__)

os.chdir("/home/led/project/Basic-edge-server")
# 設定日誌
logging.basicConfig(filename='app.log', level=logging.INFO)

# 儲存裝置狀態的字典
device_status = {}

@app.route('/input/<client_id>/<session_id>/', methods=['POST'])
def receive_file(client_id,session_id):
    print("received")
    file = request.files['file']
    current_path = os.getcwd()
    directoryID = os.path.join(current_path, "static/input", client_id)
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
    device_status[data['device_id']] = {'status': data['status'],
                                        'device_id': data['device_id'],
                                        'device_type': data['device_type'],
                                        'timestamp': data['timestamp']}
    print(device_status)
    app.logger.info(f"Received status from device {data['device_id']}: {data['status']} at {data['timestamp']}")
    return jsonify({'message': 'Status received'}), 200


@app.route('/status_return/', methods=['GET'])
def status_return():
    return jsonify(device_status), 200

@app.route('/music/<client_id>/')
def client_id_music(client_id):
    music_files = glob.glob(f'static/input/{client_id}/*/*.wav')
    music_files = [f.replace(os.sep, '/').replace('static/', '', 1) for f in music_files]
    print(music_files)
    return render_template('music.html', music_files=music_files)

@app.route('/main/', methods=['GET'])
def home():
    return render_template('home.html', device_status=device_status)

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('伺服器錯誤: %s', error)
    return jsonify({'message': '內部伺服器錯誤'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9997)
