import sqlite3 as sql
import youtube_dl
import datetime
from ml_utils import *

queries = ['machine+learning', 'data+science', 'kaggle']
db_name = 'videos.db'


def update_db():
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})

    with sql.connect(db_name) as conn:
        for query in queries:
            r = ydl.extract_info("ytsearchdate400:{}".format(query), download=False)
            video_list = r['entries']

            for video in video_list:
                if video is None:
                    continue

                p = compute_prediction(video)
                video_id = video['webpage_url']
                watch_uploader = video['uploader'].replace("'", "")
                watch_uploader_url = video['uploader_url'].replace("'", "")
                watch_thumbnail = video['thumbnail'].replace("'", "")
                watch_title = video['title'].replace("'", "")

                try:
                    watch_view_count = video['view_count']
                except KeyError:
                    watch_view_count = 0

                try:
                    watch_like_count = video['like_count']
                except KeyError:
                    watch_like_count = 0

                duration = str(datetime.timedelta(seconds=video['duration']))
                data_front = {'title': watch_title,
                              'score': float(p),
                              'video_id': video_id,
                              'uploader': watch_uploader,
                              'uploader_url': watch_uploader_url,
                              'duration': duration,
                              'view_count': watch_view_count,
                              'like_count': watch_like_count,
                              'thumbnail': watch_thumbnail}

                print(video_id, json.dumps(data_front))
                c = conn.cursor()
                c.execute("INSERT INTO videos VALUES ('{title}', '{video_id}', {score}, '{uploader}', '{uploader_url}', '{duration}', '{view_count}', '{like_count}','{thumbnail}')".format(**data_front))
                conn.commit()
    return True
