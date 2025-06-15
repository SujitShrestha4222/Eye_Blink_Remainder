import cv2
import mediapipe as mp
import time
import threading
import os
import sys


# Initialize MediaPipe face mesh(i.e bringing the face mesh from the mediapipe library )
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


# Eye landmarks (by index from MediaPipe face mesh model)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Function to calculate EAR (Eye Aspect Ratio)
def eye_aspect_ratio(eye):
    A = ((eye[1][0] - eye[5][0]) ** 2 + (eye[1][1] - eye[5][1]) ** 2) ** 0.5
    B = ((eye[2][0] - eye[4][0]) ** 2 + (eye[2][1] - eye[4][1]) ** 2) ** 0.5
    C = ((eye[0][0] - eye[3][0]) ** 2 + (eye[0][1] - eye[3][1]) ** 2) ** 0.5
    return (A + B) / (2.0 * C)

def system_beep():
    if sys.platform == "win32":
        import winsound
        winsound.Beep(1000, 500)
    else:
        print('\a', end='', flush=True)

# New: Repeating beep thread control
beep_thread = None
stop_beep_flag = False

def repeat_beep():
    global stop_beep_flag
    while not stop_beep_flag:
        print("Beep triggered!")
        system_beep()
        time.sleep(1.5) #if you don't blink ,the beep sound comes again and again within 1.5 sec

cap = cv2.VideoCapture(0)
BLINK_THRESHOLD = 0.20 #if this threshold is high(your little blink also can triggered)
                       #if this threshold is lower(it ignores your partial blink)
                       #this means in real time our ear would be around 27-30 and when we go towards closing our eye,the ear decrease and when it meets lower than our set blink threshold,it triggers our blinked print. it means when threshold is 0.25 ,our little blink also can make the ear go below the 0.25 which is considered triggered(blinked)

NO_BLINK_LIMIT = 5  # you must blink under 10seconds time to reduce the eye strain hai!!!

last_blink_time = time.time()
is_blinking = False
beep_played = False  # To avoid multiple beep threads

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        left_eye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in LEFT_EYE]
        right_eye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in RIGHT_EYE]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0

        print(f"EAR: {avg_ear:.2f}")

        if avg_ear < BLINK_THRESHOLD:
            if not is_blinking:
                is_blinking = True
                last_blink_time = time.time()
                beep_played = False
                stop_beep_flag = True  # Stop ongoing beep thread
            blink_status = "BLINKING"
            color = (0, 0, 255)
            timer_display = "0.00"
        else:
            if is_blinking:
                is_blinking = False

            blink_status = "NOT BLINKING"
            color = (0, 255, 0)

            elapsed = time.time() - last_blink_time
            timer_display = f"{elapsed:.2f}"

            if elapsed > NO_BLINK_LIMIT and not beep_played:
                stop_beep_flag = False
                beep_thread = threading.Thread(target=repeat_beep)
                beep_thread.daemon = True
                beep_thread.start()
                beep_played = True

        # Stop the beep thread once the user blinks
        if avg_ear < BLINK_THRESHOLD and beep_played:
            stop_beep_flag = True
            beep_played = False

        # Draw eye landmarks
        for p in left_eye + right_eye:
            cv2.circle(frame, p, 2, color, -1)

        # Display EAR, blink status, and timer
        cv2.putText(frame, f'EAR: {avg_ear:.2f} - {blink_status}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f'Time since last blink: {timer_display} s', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Eye Blink Reminder", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stop_beep_flag = True  # Ensure beep thread ends if still running
cap.release()
cv2.destroyAllWindows()
