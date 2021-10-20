import run_backend
import sqlite3 as sql

if __name__ == "__main__":
    with sql.connect(run_backend.db_name) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE VIDEOS
                        (title text,
                         uploader text,
                         uploader_url text,
                         duration text,
                         view_count text,
                         like_count text,
                         thumbnail text,
                         video_id text, 
                         score real
                         )""")
        conn.commit()

    run_backend.update_db()
