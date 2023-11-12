from flask import Blueprint, request
from models.response import Response
import numpy as np
import cv2
import mediapipe as mp

translateRoutes = Blueprint('translate', __name__, url_prefix="/translate")
mp_holistic = mp.solutions.holistic


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    return results


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]
                    ).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]
                    ).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]
                  ).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]
                  ).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


@translateRoutes.post('/')
def translate():
    photos = request.data
    print("photos: ", photos)
    print("json: ", request.json)
    print("files: ", request.files)

    # if photos is None:
    #     return Response.new("Failed", success=False), 400
    #
    # points = []
    #
    # with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    #     for f in photos:
    #         frame = np.frombuffer(f, dtype=np.uint8)
    #         frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    #         results = mediapipe_detection(frame, holistic)
    #         points.append(extract_keypoints(results))
    #
    #     print(len(points))

    return Response.new("Success")
