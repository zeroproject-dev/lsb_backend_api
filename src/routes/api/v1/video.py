from typing import List, Tuple
from datetime import datetime
from flask import Blueprint,  request
import uuid
import os
from werkzeug.utils import secure_filename
import numpy as np

from models.video import TVIDEO
from models.wordvideo import TWORDVIDEO
from models.user import TUSER
from models.response import Response
from utils.video import extract_points_of_video, generate_preview, get_duration
from database.db import db


videosRoutes = Blueprint("videos", __name__, url_prefix="/videos")


@videosRoutes.get("/")
def get_videos():
  videos = (
      db.session.query(TVIDEO, TUSER)
      .join(TUSER, TVIDEO.uploaded_by == TUSER.id)
      .all()
  )
  return Response.success("Lista de videos", [video.to_json() for video in videos])


@videosRoutes.get("/<int:word_id>")
def get_video_word(word_id):
  videos_with_users: List[Tuple[TVIDEO, TUSER]] = db.session.query(TVIDEO, TUSER).join(TWORDVIDEO, TVIDEO.id == TWORDVIDEO.video_id).join(
      TUSER, TVIDEO.uploaded_by == TUSER.id).filter(TWORDVIDEO.word_id == word_id).all()

  videos = []
  for video, user in videos_with_users:
    video_json = video.to_json()
    video_json["uploaded_by"] = user.to_json()
    videos.append(video_json)

  return Response.success("Lista de videos", videos)


# BASE_PATH = os.path.split(__file__)[0]
BASE_PATH = os.getcwd()
VIDEOS_FOLDER = os.path.join(BASE_PATH, "static", "videos")
IMAGES_FOLDER = os.path.join(BASE_PATH, "static", "images")
POINTS_FOLDER = os.path.join(BASE_PATH, "static", "points")

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


@videosRoutes.post("/<word>/<word_id>")
def create_video(word: str, word_id: int):
  if "video" not in request.files:
    return Response.fail("Falta el video"), 400

  video = request.files["video"]

  if video is None or video.filename is None:
    return Response.fail("Falta el video"), 400

  video_name = str(uuid.uuid4())
  video_extension = video.filename.split(".")[-1]

  file_path = os.path.join(VIDEOS_FOLDER, video_name + "." + video_extension)
  img_path = os.path.join(IMAGES_FOLDER, video_name + ".jpg")

  video.save(file_path)

  generate_preview(file_path, img_path)

  duration = get_duration(file_path)

  points = extract_points_of_video(file_path)

  if duration is None or points is None:
    return Response.fail("Error al verificar el video"), 400

  try:
    if not os.path.exists(os.path.join(POINTS_FOLDER, word)):
      os.makedirs(os.path.join(POINTS_FOLDER, word))
    path_word = os.path.join(POINTS_FOLDER, word)

    path_points = os.path.join(path_word, video_name)
    os.makedirs(path_points)
  except:
    return Response.fail("Error al verificar el video"), 400

  for i, point in enumerate(points):
    points_path = os.path.join(path_points, str(i))
    np.save(points_path, point)

  new_video = TVIDEO()
  new_video.path = os.path.join("static", "videos", video_name + "." + video_extension)
  new_video.preview = os.path.join(
      "static", "images", video_name + ".jpg"
  )
  new_video.points = os.path.join("static", "points", word, video_name)
  new_video.duration = duration
  new_video.bucket = "words"
  new_video.region = "us"
  new_video.uploaded_by = 1
  new_video.uploaded_date = datetime.now()
  new_video.state = "active"

  db.session.add(new_video)
  db.session.commit()

  new_word_video = TWORDVIDEO()
  new_word_video.word_id = word_id
  new_word_video.video_id = new_video.id
  db.session.add(new_word_video)
  db.session.commit()

  return Response.success("Video agregado correctamente", new_video.to_json())


@videosRoutes.delete("/<id>")
def delete_video(id: int):
  twordvideo = db.session.query(TWORDVIDEO).filter(TWORDVIDEO.video_id == id).first()

  if twordvideo is None:
    return Response.fail("Video no encontrado"), 404

  db.session.delete(twordvideo)
  db.session.commit()

  video = db.session.query(TVIDEO).filter(TVIDEO.id == id).first()

  if video is None:
    return Response.fail("Video no encontrado"), 404

  db.session.delete(video)
  db.session.commit()

  delete_video_path = os.path.join(BASE_PATH, video.path)

  os.remove(delete_video_path)

  delete_preview_path = os.path.join(BASE_PATH, video.preview)

  os.remove(delete_preview_path)

  delete_points_path = os.path.join(BASE_PATH, video.points)

  os.system('rm -rf "{}"'.format(delete_points_path))

  return Response.success("Video eliminado correctamente", {})
