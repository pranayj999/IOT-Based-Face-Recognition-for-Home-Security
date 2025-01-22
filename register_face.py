import cv2
import os

# Create directory for storing registered faces
face_dir = "registered_faces"
os.makedirs(face_dir, exist_ok=True)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture
cap = cv2.VideoCapture(0)
user_name = input("Enter the name of the person: ")
save_path = os.path.join(face_dir, user_name)
os.makedirs(save_path, exist_ok=True)

print("Press 'c' to capture images. Press 'q' to quit.")

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face = gray_frame[y:y+h, x:x+w]
        if cv2.waitKey(1) & 0xFF == ord('c'):
            count += 1
            cv2.imwrite(f"{save_path}/{user_name}_{count}.jpg", face)
            print(f"Captured {count} images")

    cv2.imshow("Register Face", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()
print(f"Face registration completed for {user_name}. Images saved in {save_path}.")
