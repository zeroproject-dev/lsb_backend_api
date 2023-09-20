import subprocess


def generate_preview(video_path, img_output_path):
    subprocess.call(['ffmpeg', '-i', video_path, '-ss',
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
