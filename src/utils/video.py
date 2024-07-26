import mediapipe as mp
import os
import numpy as np
import cv2
import subprocess


def generate_preview(video_path, img_output_path):
    return subprocess.run(['ffmpeg', '-i', video_path, '-ss',
                    '00:00:00.000', '-vframes', '1', img_output_path])


def get_duration(video_path):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration_str = result.stdout.strip()
        duration = float(duration_str)
        return duration
    except Exception as e:
        print(f"Error al obtener la duración del video: {str(e)}")
        return None


mp_holistic = mp.solutions.holistic


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten(
    ) if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten(
    ) if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten(
    ) if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten(
    ) if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


def extract_points_of_video(video):
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print(f"Error al abrir el archivo {os.getcwd()}/{video}")
        return None

    points = []

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        for _ in range(30):
            _, frame = cap.read()

            if frame is None:
                break

            _, results = mediapipe_detection(frame, holistic)

            keypoints = extract_keypoints(results)
            points.append(keypoints)

        cap.release()

    return points
