#Python code to print and draw all 468 points on your face in real time and see them:
#Face is outlined with numbers all over (each number = a point like the corner of an eye, nose tip, lips, etc.)

import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame to detect face landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for i, landmark in enumerate(face_landmarks.landmark):
                x, y = int(landmark.x * width), int(landmark.y * height)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    cv2.imshow("Face Mesh Landmarks", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()


#This draws numbers on your face in real time, so you can see which point is where.