import datetime
from flask import Flask, render_template, request
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
            line_json = {"title": line[0],
                         "video_id": line[1],
                         "score": line[2],
                         'uploader': line[3],
                         'uploader_url': line[4],
                         'duration': line[5],
                         'view_count': line[6],
                         'like_count': line[7],
                         'thumbnail': line[8]
                         }
            videos.append(line_json)

    # if time.time_ns() - last_update > (720*3600*1e9):
    #   run_backend.update_db()

    predictions = []
    for video in videos:
        predictions.append((video['video_id'],
                            video['title'],
                            float(video['score']),
                            video['uploader'],
                            video['uploader_url'],
                            video['duration'],
                            video['view_count'],
                            video['like_count'],
                            video['thumbnail']
                            ))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

    return predictions


@app.route('/')
def main_page():
    preds = get_predictions()

    return render_template("index.html", len=len(preds), predictions=preds)


@app.route('/predict')
def predict_api():
    yt_video_id = request.args.get("id", default='')

    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})
    video_json_data = ydl.extract_info("https://www.youtube.com/watch?v={}".format(yt_video_id), download=False)

    if video_json_data is None:
        return "not found"

    p = ml_utils.compute_prediction(video_json_data)

    video_id_ = video_json_data['webpage_url']
    watch_uploader_ = video_json_data['uploader'].replace("'", "")
    watch_uploader_url_ = video_json_data['uploader_url'].replace("'", "")
    watch_thumbnail_ = video_json_data['thumbnail'].replace("'", "")
    watch_title_ = video_json_data['title'].replace("'", "")

    try:
        watch_view_count_ = video_json_data['view_count']
    except KeyError:
        watch_view_count_ = 0

    try:
        watch_like_count_ = video_json_data['like_count']
    except KeyError:
        watch_like_count_ = 0

    duration_ = str(datetime.timedelta(seconds=video_json_data['duration']))

    output = [[video_id_, watch_title_, p, watch_uploader_, watch_uploader_url_,
               duration_, watch_view_count_, watch_like_count_, watch_thumbnail_]]

    return render_template("index.html", len=len(output), predictions=output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
