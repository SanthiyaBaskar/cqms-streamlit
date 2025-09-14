import sqlite3, os, pandas as pd, datetime
DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
SEED_CSV = os.path.join(os.path.dirname(__file__), "data", "seed_queries.csv")
def conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
def init_db():
    c = conn()
    cur = c.cursor()
    cur.execute("create table if not exists users(id integer primary key autoincrement, username text unique, hashed_password text, role text)")
    cur.execute("create table if not exists queries(id integer primary key autoincrement, mail_id text, mobile_number text, query_heading text, query_description text, status text, query_created_time text, query_closed_time text, image blob)")
    c.commit()
    if os.path.exists(SEED_CSV):
        n = pd.read_sql_query("select count(*) as n from queries", c).iloc[0]["n"]
        if n == 0:
            seed = pd.read_csv(SEED_CSV)
            for _, r in seed.iterrows():
                cur.execute("insert into queries(id, mail_id, mobile_number, query_heading, query_description, status, query_created_time, query_closed_time) values(?,?,?,?,?,?,?,?)",
                            (int(r["query_id"]), r["mail_id"], r["mobile_number"], r["query_heading"], r["query_description"], r["status"], r["query_created_time"], r["query_closed_time"] if str(r["query_closed_time"])!='nan' else None))
            c.commit()
    c.close()
def add_user(username, hashed_password, role):
    c = conn(); cur = c.cursor()
    cur.execute("insert into users(username, hashed_password, role) values(?,?,?)", (username, hashed_password, role))
    c.commit(); c.close()
def get_user(username):
    c = conn(); cur = c.cursor()
    cur.execute("select id, username, hashed_password, role from users where username=?", (username,))
    row = cur.fetchone(); c.close(); return row
def insert_query(mail_id, mobile_number, heading, description, image_bytes):
    c = conn(); cur = c.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("insert into queries(mail_id, mobile_number, query_heading, query_description, status, query_created_time, image) values(?,?,?,?,?,?,?)",
                (mail_id, mobile_number, heading, description, "Open", now, image_bytes))
    c.commit(); c.close()
def close_query(qid):
    c = conn(); cur = c.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("update queries set status='Closed', query_closed_time=? where id=?", (now, qid))
    c.commit(); c.close()
def list_queries(status=None, search=None):
    c = conn()
    q = "select id, mail_id, mobile_number, query_heading, query_description, status, query_created_time, query_closed_time from queries"
    params = []; conds = []
    if status and status != "All":
        conds.append("status=?"); params.append(status)
    if search:
        conds.append("(query_heading like ? or query_description like ? or mail_id like ?)")
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if conds: q += " where " + " and ".join(conds)
    q += " order by datetime(coalesce(query_closed_time, query_created_time)) desc"
    df = pd.read_sql_query(q, c, params=params); c.close(); return df
def get_image(qid):
    c = conn(); cur = c.cursor()
    cur.execute("select image from queries where id=?", (qid,))
    r = cur.fetchone(); c.close(); return r[0] if r else None
def metrics():
    c = conn(); cur = c.cursor()
    cur.execute("select count(*) from queries"); total = cur.fetchone()[0]
    cur.execute("select count(*) from queries where status='Open'"); open_n = cur.fetchone()[0]
    cur.execute("select count(*) from queries where status='Closed'"); closed_n = cur.fetchone()[0]
    cur.execute("select avg(strftime('%s', query_closed_time) - strftime('%s', query_created_time)) from queries where status='Closed' and query_closed_time is not null")
    avg = cur.fetchone()[0]; avg_hours = round(avg/3600,2) if avg else 0; c.close(); return total, open_n, closed_n, avg_hours