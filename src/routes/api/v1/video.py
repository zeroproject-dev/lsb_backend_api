from flask import Blueprint, jsonify, request
from sqlalchemy.util.deprecations import os

from models.video import TVIDEO


videosRoutes = Blueprint('videos', __name__, url_prefix='/videos')


@videosRoutes.get('/')
def get_videos():

    videos = TVIDEO.query.all()
    return jsonify([video.to_json() for video in videos])


BASE_PATH = os.path.split(__file__)[0]
VIDEOS_FOLDER = os.path.join(BASE_PATH, 'static', 'assets', 'videos')


@ videosRoutes.post('/')
def create_video():
    if 'video' not in request.files:
        return jsonify({'message': 'Falta el video'}), 400

    video = request.files['video']

    return jsonify({'name': 'video001.mp4'})


@ videosRoutes.get('/:id')
def get_video(id: int):
    return jsonify({'name': 'video001.mp4'})


@ videosRoutes.delete('/:id')
def delete_video(id: int):
    return jsonify({'name': 'video001.mp4'})
