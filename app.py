import streamlit as st, pandas as pd, matplotlib.pyplot as plt
from db import init_db, metrics, list_queries, get_user, add_user
from auth import hash_password, verify_password

st.set_page_config(page_title="Client Query Management System", page_icon="🧾", layout="wide")
init_db()
if "user" not in st.session_state:
    st.session_state.user = None

# -------- Sidebar (auth) --------
with st.sidebar:
    mode = st.radio("Mode", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Client","Support"])
    if mode == "Register":
        if st.button("Create Account", use_container_width=True):
            if username and password:
                try:
                    add_user(username, hash_password(password), role)
                    st.success("Account created. Switch to Login.")
                except:
                    st.error("Username already exists")
            else:
                st.error("Enter credentials")
    else:
        if st.button("Login", use_container_width=True):
            u = get_user(username)
            if not u:
                st.error("User not found")
            else:
                if verify_password(password, u[2]):
                    st.session_state.user = {"id":u[0],"username":u[1],"role":u[3]}
                    st.success("Logged in")
                else:
                    st.error("Invalid credentials")
    if st.session_state.user:
        st.info("Logged in as " + st.session_state.user["username"] + " (" + st.session_state.user["role"] + ")")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None

# -------- Data & metrics --------
t, o, c, a = metrics()
df = list_queries(status="All")
for col in ["query_created_time","query_closed_time"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

today = pd.Timestamp.now().normalize()
today_new = int((df["query_created_time"].dt.normalize() == today).sum())

closed_df = df[df["status"] == "Closed"].dropna(subset=["query_closed_time"])
if not closed_df.empty:
    closed_df = closed_df.assign(
        rt_hrs=(closed_df["query_closed_time"] - closed_df["query_created_time"]).dt.total_seconds()/3600
    )
    on_time_rate = round((closed_df["rt_hrs"] <= 24).mean()*100, 1)
else:
    on_time_rate = 0.0

open_df = df[df["status"] == "Open"]
if not open_df.empty:
    oldest_open_age = int((today - open_df["query_created_time"].dt.normalize().min()).days)
else:
    oldest_open_age = 0

days = pd.date_range(end=today, periods=14)
created = df["query_created_time"].dt.normalize().value_counts().reindex(days, fill_value=0).sort_index()
closed = df[df["status"]=="Closed"]["query_closed_time"].dt.normalize().value_counts().reindex(days, fill_value=0).sort_index()

# -------- Styles --------
st.markdown(
    """
    <style>
    .main .block-container{padding:6px 10px 12px}
    body{background:#f5f7ff}
    .accent{height:54px;border-radius:12px;background:
      radial-gradient(260px 80px at -10% -10%, #22c55e33, transparent 60%),
      radial-gradient(220px 70px at 110% 20%, #60a5fa33, transparent 60%),
      linear-gradient(135deg,#0ea5e9,#2563eb 40%,#1d4ed8);
      position:relative;overflow:hidden;margin-bottom:8px}
    .accent:after{content:"";position:absolute;inset:-40% -40% auto auto;height:200%;width:200%;
      background:conic-gradient(from 180deg at 50% 50%,#22c55e22,#60a5fa22,#f9731622,#22c55e22);
      animation:spin 24s linear infinite}
    @keyframes spin{to{transform:rotate(360deg)}}
    .headline{display:flex;align-items:center;gap:10px;margin:0 2px 6px 2px}
    .headline h1{font-size:22px;color:#0f172a;margin:0;font-weight:900}
    .ticker{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:8px}
    .tick{background:#0e1f3a;color:#e5edff;border:1px solid #c7d2fe33;border-radius:10px;padding:8px 10px;font-weight:700;text-align:center}
    .flash{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:8px}
    .card{background:#ffffff;border:1px solid rgba(2,6,23,.06);border-radius:12px;padding:10px}
    .knum{font-size:20px;font-weight:900;color:#0f172a;margin-top:6px}
    .klabel{font-size:12px;color:#334155}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .head{font-weight:800;color:#0f172a;margin-bottom:6px}
    .progress{height:10px;background:#e2e8f0;border-radius:999px;overflow:hidden}
    .bar{height:100%;background:linear-gradient(90deg,#22c55e,#60a5fa)}
    .tips{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .tip{background:#ecfeff;border:1px solid #67e8f9;border-radius:10px;padding:8px;font-size:13px}
    .bottom{margin-top:10px}
    .bottom-grid{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:10px}
    .small{font-size:13px;color:#334155}
    </style>
    """,
    unsafe_allow_html=True
)

# -------- Accent + headline --------
st.markdown('<div class="accent"></div>', unsafe_allow_html=True)
st.markdown('<div class="headline"><h1>Client Query Management System</h1></div>', unsafe_allow_html=True)

# -------- Live ticker --------
st.markdown('<div class="ticker">', unsafe_allow_html=True)
st.markdown('<div class="tick">Open '+str(o)+'</div>', unsafe_allow_html=True)
st.markdown('<div class="tick">Closed '+str(c)+'</div>', unsafe_allow_html=True)
st.markdown('<div class="tick">Avg '+str(a)+' hrs</div>', unsafe_allow_html=True)
st.markdown('<div class="tick">New today '+str(today_new)+'</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------- Flash cards --------
st.markdown('<div class="flash">', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown('<div class="card"><div>On-time close ≤ 24h</div><div class="knum">'+str(on_time_rate)+'%</div><div class="progress"><div class="bar" style="width:'+str(on_time_rate)+'%"></div></div></div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="card"><div>Oldest open age</div><div class="knum">'+str(oldest_open_age)+' days</div><div class="klabel">Reduce backlog</div></div>', unsafe_allow_html=True)
with f3:
    st.markdown('<div class="card"><div>Avg resolution</div><div class="knum">'+str(a)+' hrs</div><div class="klabel">Across closed tickets</div></div>', unsafe_allow_html=True)
with f4:
    st.markdown('<div class="card"><div>Total queries</div><div class="knum">'+str(t)+'</div><div class="klabel">Project to date</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------- Recent + donut --------
st.markdown('<div class="row">', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    st.markdown('<div class="card"><div class="head" id="go">Recent Activity</div>', unsafe_allow_html=True)
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><div class="head">Status Overview</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        sizes = [o, c]
        labels = ["Open","Closed"]
        fig = plt.figure(figsize=(1.9,1.9))
        wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            autopct="%1.0f%%",
            startangle=120,
            colors=["#2563eb","#22c55e"],
            pctdistance=0.78,
            textprops={"color":"#0f172a","weight":"bold"}
        )
        centre = plt.Circle((0,0),0.56,fc="#ffffff")
        fig.gca().add_artist(centre)
        plt.axis("equal")
        fig.patch.set_alpha(0)
        st.pyplot(fig, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------- Trend + quick access --------
st.markdown('<div class="row">', unsafe_allow_html=True)
l2, r2 = st.columns(2)

with l2:
    st.markdown('<div class="card"><div class="head">14-day Created vs Closed</div>', unsafe_allow_html=True)
    fig2, ax = plt.subplots(figsize=(7.5, 3.2))
    ax.plot(days, created, label="Created", linewidth=2.8, marker="o", markersize=4)
    ax.fill_between(days, 0, created, alpha=0.25)
    ax.plot(days, closed,  label="Closed",  linewidth=2.8, marker="o", markersize=4)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Tickets / day", fontsize=9)
    ax.set_xlabel("")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", frameon=False)
    ax.set_xticks(days[::3])
    ax.set_xticklabels([d.strftime("%d %b") for d in days[::3]], fontsize=9)
    st.pyplot(fig2, use_container_width=True)

    last7 = pd.date_range(end=today, periods=7)
    created7 = int(created.reindex(last7, fill_value=0).sum())
    closed7  = int(closed.reindex(last7,  fill_value=0).sum())
    delta7   = created7 - closed7
    if delta7 > 0:
        trend_word = "↑ backlog grew by " + str(delta7)
    elif delta7 < 0:
        trend_word = "↓ backlog shrank by " + str(-delta7)
    else:
        trend_word = "— backlog unchanged"
    st.caption("Daily counts of Created (blue) vs Closed (orange) tickets for the last 14 days. Past 7 days → Created: "
               + str(created7) + ", Closed: " + str(closed7) + ", " + trend_word + ".")
    st.markdown('</div>', unsafe_allow_html=True)

with r2:
    st.markdown('<div class="card"><div class="head">Quick Access</div>', unsafe_allow_html=True)
    if st.session_state.user and st.session_state.user["role"] == "Client":
        st.page_link("pages/1_Client_Submission.py", label="Open Client Submission", use_container_width=True)
    elif st.session_state.user and st.session_state.user["role"] == "Support":
        st.page_link("pages/2_Support_Dashboard.py", label="Open Support Dashboard", use_container_width=True)
    else:
        st.info("Login from the left sidebar to continue")
    st.markdown('<div class="head" style="margin-top:8px">Tips</div>', unsafe_allow_html=True)
    st.markdown('<div class="tips"><div class="tip">Attach a screenshot for faster triage</div>'
                '<div class="tip">Use search to filter by email or heading</div>'
                '<div class="tip">Download CSV from Support Dashboard</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------- Bottom utilities (replaces footer chip) --------
st.markdown('<div class="bottom">', unsafe_allow_html=True)
st.markdown('<div class="bottom-grid">', unsafe_allow_html=True)

# Export all data
colA, colB, colC = st.columns([1.1, 1, 1])
with colA:
    st.markdown('<div class="card"><div class="head">Export</div>', unsafe_allow_html=True)
    st.download_button(
        "Download all queries (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="queries_all.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# How to use
with colB:
    st.markdown('<div class="card"><div class="head">How to use</div>', unsafe_allow_html=True)
    st.markdown('<div class="small">Client → submit query with screenshot. '
                'Support → filter/search, mark closed, export CSV. '
                'Use the trend to watch backlog and the donut to see current status.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Support info (replace with your real details)
with colC:
    st.markdown('<div class="card"><div class="head">Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="small">Email: support@example.com<br/>SLA target: close within 24 hours<br/>DB: local SQLite (project scope)</div>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
