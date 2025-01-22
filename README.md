# IoT-Based Facial Recognition for Home Security

An IoT-powered system for secure door access using facial recognition. This project integrates **OpenCV**, **Raspberry Pi**, a **GSM module**, and **relay circuits** to provide enhanced home security. It features real-time face recognition, alarm activation, and SMS alerts for unauthorized access.

---

## Features

1. **Face Registration**: Capture and save images to register new faces.
2. **Training the Model**: Train the Local Binary Patterns Histogram (LBPH) recognizer using registered faces.
3. **Real-Time Face Recognition**:
   - Unlocks the door for authorized faces.
   - Activates a buzzer alarm and sends SMS alerts for unauthorized access.
4. **SMS Notifications**: Uses AT commands and a GSM module for SMS alerts.
5. **Modular and Scalable**: Easily extendable for additional features like cloud-based monitoring or remote access.

---

## Hardware Requirements

- Raspberry Pi 3 Model B (or later)
- USB Camera or Pi Camera
- SPDT Relay Module
- GSM Module (e.g., SIM800)
- Buzzer
- 5V Power Supply
- Door Lock Mechanism

---

## Software Requirements

- Python 3.x
- Libraries: `opencv-python`, `opencv-contrib-python`, `numpy`, `RPi.GPIO`
- Thonny Python IDE (optional)
- Raspbian OS (recommended)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/iot-facial-recognition.git
   cd iot-facial-recognition
   Install dependencies:
2. Install dependencies:
pip install opencv-python opencv-contrib-python numpy

#Connect and configure hardware components:
Relay to GPIO 18
Buzzer to GPIO 23
GSM module to a USB port

#Train the model:
Run register_face.py to capture face images.
Run train_faces.py to train the recognizer.

Start the recognition system:
python main.py

#Usage

Register Faces: Capture faces and save them to the dataset.
Train Model: Generate a trained model using LBPH.
Run System: Recognize faces and control the door lock, alarm, and SMS notifications.

#Project Structure:

.
├── register_face.py         # Script for capturing and saving face images
├── train_faces.py           # Script for training the LBPH recognizer
├── main.py                  # Main script for real-time face recognition
├── face_recognizer.yml      # Trained model file (generated after training)
├── label_map.npy            # Label map for face recognition
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation


#Example AT Commands

Set SMS Mode: AT+CMGF=1
Send SMS: AT+CMGS="+1234567890"
Check SIM Status: AT+CPIN?
Check Network Registration: AT+CREG?

#Future Enhancements:

Cloud-based face data storage.
Integration with smart home ecosystems.
Enhanced face detection using deep learning models.
