import threading
from datetime import datetime

from flask import Flask, render_template, request, jsonify

from matrix.main import Matrix
from matrix.modules.alarm import AlarmModule, ScrollTextModule

matrix = Matrix()
matrix_thread = threading.Thread(target=matrix.run_update_loop, daemon=True)
matrix_thread.start()

app = Flask(__name__)

@app.route('/')
def render_index():
  return render_template('alarm.html')

@app.route('/alarms')
def render_alarm():
  return render_template('alarm.html')

@app.route('/api/alarms', methods=['POST'])
def save_alarm():
  for alarm in request.json:
    set_alarm(matrix, alarm)
  return jsonify({"message": "Alarm saved successfully"})

def set_alarm(matrix, data):
  time = datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')
  alarm_module = AlarmModule(data['label'], time)
  matrix.register(alarm_module, 0, 8, 2)

@app.route('/api/alarms/<id>', methods=['PATCH'])
def update_alarm(id):
  alarm_module = matrix.get_module(id)
  if alarm_module is None:
    return jsonify({"message": "Alarm not found"})

  data = request.json
  alarm_module.date = datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')
  alarm_module.set_text(data['label'])
  return jsonify({"message": "Alarm updated successfully"})
#
@app.route('/api/alarms/<id>/enable', methods=['POST'])
def enable_alarm(id):
  alarm_module = matrix.get_module(id)
  if alarm_module is None:
    return jsonify({"message": "Alarm not found"})

  data = request.json
  alarm_module.enabled = data['enabled']
  return jsonify({"message": "Alarm updated successfully"})


@app.route('/api/alarms', methods=['GET'])
def get_alarms():
  alarms = matrix.get_modules_by_class(AlarmModule.__name__)
  json_alarms = []
  for alarm in alarms:
    json_alarms.append({
      "id": alarm.id,
      "date": alarm.date.strftime("%Y-%m-%d"),
      "time": alarm.date.strftime("%H:%M"),
      "label": alarm.text,
      "enabled": alarm.enabled
    })
  return jsonify({"alarms": json_alarms})

@app.route('/api/alarms/<id>', methods=['DELETE'])
def delete_alarm(id):
  if matrix.remove_module(id):
    return jsonify({"message": "Success"}), 200
  else:
    return jsonify({"message": "Alarm not found"}), 404