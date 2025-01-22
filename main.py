import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import serial

# Load trained model and label map
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_recognizer.yml")
label_map = np.load("label_map.npy", allow_pickle=True).item()

# Setup GPIO for relay (door lock) and buzzer (alarm)
RELAY_PIN = 18
BUZZER_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize serial connection for GSM module
GSM_PORT = "/dev/ttyUSB0"  # Adjust based on your Raspberry Pi setup
gsm = serial.Serial(GSM_PORT, baudrate=9600, timeout=1)

# Initialize video capture
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("Press 'q' to quit.")

def send_sms(message):
    """Send SMS alert via GSM module."""
    gsm.write(b'AT+CMGF=1\r')  # Set SMS text mode
    time.sleep(1)
    gsm.write(b'AT+CMGS="+1234567890"\r')  # Replace with the recipient's phone number
    time.sleep(1)
    gsm.write(f"{message}\r".encode())
    gsm.write(bytes([26]))  # ASCII code for Ctrl+Z to send the SMS
    time.sleep(3)
    print("SMS sent.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            face = gray_frame[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))
            label, confidence = recognizer.predict(face)

            if confidence < 50:  # Adjust threshold based on testing
                name = [key for key, value in label_map.items() if value == label][0]
                print(f"Access Granted: {name}")
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # Unlock door
                time.sleep(5)  # Keep door unlocked for 5 seconds
                GPIO.output(RELAY_PIN, GPIO.LOW)   # Lock door
            else:
                print("Access Denied. Intruder Alert!")
                GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Activate buzzer
                send_sms("Intruder Alert! Unauthorized person detected at the door.")
                time.sleep(3)  # Sound the buzzer for 3 seconds
                GPIO.output(BUZZER_PIN, GPIO.LOW)  # Deactivate buzzer

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    gsm.close()

