import cv2
import os
import numpy as np

# Paths
face_dir = "registered_faces"
model_path = "face_recognizer.yml"

# Initialize LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Prepare training data
faces = []
labels = []
label_map = {}
label_id = 0

for root, dirs, files in os.walk(face_dir):
    for file in files:
        if file.endswith(".jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root)

            if label not in label_map:
                label_map[label] = label_id
                label_id += 1

            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(label_map[label])

# Train the recognizer
faces = np.array(faces)
labels = np.array(labels)
recognizer.train(faces, labels)

# Save the trained model and label map
recognizer.write(model_path)
np.save("label_map.npy", label_map)
print("Training completed. Model saved.")
