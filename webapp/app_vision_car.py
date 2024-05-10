from flask import Flask, render_template, Response, request, jsonify, stream_with_context
import RPi.GPIO as GPIO
import cv2
from components.drv8833 import Motor
from components.dual_axis_servos import Dual_Axis
from components.camera import CameraStream
import threading
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

motor = Motor(5,6,27,17)
dual_axis=Dual_Axis(18,90,19,90)
cap = CameraStream().start()

def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route('/car_action', methods=['GET'])
def car_action():
    m_action = int(request.args.get('action'))
    motor.action(m_action)
    return jsonify({'motor status':m_action})


@app.route('/dual_axis_action', methods=['GET'])
def dual_axis_action():
    dual_axis_action = int(request.args.get('action'))
    dual_axis.action(dual_axis_action)
    return jsonify({'dual_axis servo status':dual_axis_action})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
    cv2.destroyAllWindows()
    GPIO.cleanup()
