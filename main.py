from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

# === Initialize MediaPipe ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# === Gesture Classification Rules ===
def classify_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    wrist = landmarks[0]

    fingers_up = [
        index_tip.y < wrist.y,
        middle_tip.y < wrist.y,
        ring_tip.y < wrist.y,
        pinky_tip.y < wrist.y,
        thumb_tip.x > wrist.x  # right hand rule
    ]

    if all(fingers_up[:4]) and not fingers_up[4]:
        return "Palm"
    elif not any(fingers_up):
        return "Fist"
    elif fingers_up[0] and not any(fingers_up[1:]):
        return "Pointing"
    elif fingers_up[0] and fingers_up[1] and not any(fingers_up[2:]):
        return "Peace"
    elif fingers_up[4] and not any(fingers_up[:4]):
        return "Thumbs Up"
    else:
        return "Unknown"

# === Video Frame Generator ===
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark
                gesture = classify_gesture(landmarks)

                x = int(landmarks[0].x * frame.shape[1])
                y = int(landmarks[0].y * frame.shape[0])
                cv2.putText(frame, gesture, (x, y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
