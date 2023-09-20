from datetime import datetime
from sys import exception
from flask import Blueprint, jsonify, request
from sqlalchemy.util.deprecations import os
from werkzeug.utils import secure_filename
import numpy as np

from models.video import TVIDEO
from utils.video import extract_points_of_video, generate_preview, get_duration
from database.db import db


videosRoutes = Blueprint('videos', __name__, url_prefix='/videos')


@videosRoutes.get('/')
def get_videos():

    videos = TVIDEO.query.all()
    return jsonify([video.to_json() for video in videos])


# BASE_PATH = os.path.split(__file__)[0]
BASE_PATH = os.getcwd()
VIDEOS_FOLDER = os.path.join(
    BASE_PATH, 'static', 'videos')
IMAGES_FOLDER = os.path.join(
    BASE_PATH, 'static', 'images')
POINTS_FOLDER = os.path.join(
    BASE_PATH, 'static', 'points')

try:
    os.makedirs(VIDEOS_FOLDER)
except:
    pass
try:
    os.makedirs(IMAGES_FOLDER)
except:
    pass
try:
    os.makedirs(POINTS_FOLDER)
except:
    pass


@videosRoutes.post('/')
def create_video():
    if 'video' not in request.files:
        return jsonify({'message': 'Falta el video'}), 400

    video = request.files['video']

    if video is None or video.filename is None:
        return jsonify({'message': 'Falta el video'}), 400

    filename = secure_filename(video.filename)
    name_without_extension = filename.rsplit('.')[0]

    file_path = os.path.join(VIDEOS_FOLDER, filename)
    img_path = os.path.join(IMAGES_FOLDER,  name_without_extension + '.jpg')

    video.save(file_path)

    generate_preview(file_path, img_path)

    duration = get_duration(file_path)

    points = extract_points_of_video(file_path)

    if duration is None or points is None:
        return jsonify({'message': 'Error al verificar el video'}), 400

    try:
        os.makedirs(os.path.join(
            POINTS_FOLDER,  name_without_extension))
    except:
        return jsonify({'message': 'Error al verificar el video'}), 400

    for i, point in enumerate(points):
        points_path = os.path.join(
            POINTS_FOLDER,  name_without_extension, str(i))
        np.save(points_path, point)

    new_video = TVIDEO()
    new_video.path = file_path
    new_video.preview = img_path
    new_video.duration = duration
    new_video.bucket = 'words'
    new_video.region = 'us'
    new_video.uploaded_by = 1
    new_video.uploaded_date = datetime.now()
    new_video.state = 'active'

    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_json())


@videosRoutes.get('/:id')
def get_video(id: int):
    return jsonify({'name': 'video001.mp4'})


@videosRoutes.delete('/:id')
def delete_video(id: int):
    return jsonify({'name': 'video001.mp4'})
