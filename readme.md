# ✅Project Name: Eye Blink Reminder
## 💡Goal:
        Detect if the eyes have not closed/blinked for a certain duration (say, 10 seconds), and if so, beep an alert to remind you to blink.

## 🛠️Libraries You’ll Need:
        pip install opencv-python mediapipe playsound

        Or, if you want to use dlib, it’s more complex to install (we’ll start with MediaPipe, which is easier).



## ✅Approach Using MediaPipe:
        MediaPipe provides reliable eye landmark detection with real-time performance.
##### 🔍Step-by-step logic:
        Capture webcam video.
        Detect facial landmarks.
        Calculate eye aspect ratio (EAR) to detect blinks.
        Start a timer whenever the eyes are open.
        If no blink is detected for N seconds (e.g., 10s), play a sound reminder.



##### 🧠Key Concepts:
        Eye Aspect Ratio (EAR): Used to estimate if eyes are open or closed.
        Timer: To track eye-open duration.
        Sound Beep: To alert user if no blink is detected in time.