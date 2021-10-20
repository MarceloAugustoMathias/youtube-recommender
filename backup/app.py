import time
import requests
from flask import Flask
import run_backend
import ml_utils
import youtube_dl
import sqlite3 as sql

from ml_utils import *

app = Flask(__name__)


def get_predictions():

    videos = []

    with sql.connect(run_backend.db_name) as conn:
        c = conn.cursor()

        for line in c.execute("SELECT * FROM videos"):
            line_json = {"title": line[0], "video_id": line[1], "score": line[2], "update_time": line[3]}
            videos.append(line_json)

    # if time.time_ns() - last_update > (720*3600*1e9):
    #   run_backend.update_db()

    predictions = []
    for video in videos:
        predictions.append((video['video_id'], video['title'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

    predictions_formatted = []
    for e in predictions:
        predictions_formatted.append(
            "<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=e[2])
        )

    return '\n'.join(predictions_formatted)


@app.route('/')
def main_page():
    preds = get_predictions()

    return """<head><h1>Recomendador de Vídeos do Youtube</h1></head>
    <body>\
    <table>\
                {}\
    </table>\
    </body>""".format(preds)


@app.route('/predict')
def predict_api():
    yt_video_id = requests.args.get("yt_video_id", default='')

    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})
    video_json_data = ydl.extract_info("https://www.youtube.com/watch?v={}".format(yt_video_id), download=False)

    if video_json_data is None:
        return "not found"

    p = ml_utils.compute_prediction(video_json_data)
    output = {"title": video_json_data['title'], "score": p}

    return json.dumps(output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
