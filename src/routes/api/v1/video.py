from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy.util.deprecations import os
from werkzeug.utils import secure_filename

from models.video import TVIDEO
from utils.video import generate_preview, get_duration
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


@videosRoutes.post('/')
def create_video():
    if 'video' not in request.files:
        return jsonify({'message': 'Falta el video'}), 400

    video = request.files['video']

    if video is None or video.filename is None:
        return jsonify({'message': 'Falta el video'}), 400

    file_path = os.path.join(VIDEOS_FOLDER, secure_filename(video.filename))

    video.save(file_path)

    thumbnail = generate_preview(file_path)
    duration = get_duration(file_path)

    if duration is None:
        return jsonify({'message': 'Error al verificar el video'}), 400

    new_video = TVIDEO()
    new_video.path = file_path
    new_video.preview = thumbnail
    new_video.duration = duration
    new_video.uploaded_by = 1
    new_video.uploaded_date = datetime.now()
    new_video.state = 'active'

    db.session.add(new_video)
    db.session.commit()

    return jsonify({'message': 'success'})


@videosRoutes.get('/:id')
def get_video(id: int):
    return jsonify({'name': 'video001.mp4'})


@videosRoutes.delete('/:id')
def delete_video(id: int):
    return jsonify({'name': 'video001.mp4'})
