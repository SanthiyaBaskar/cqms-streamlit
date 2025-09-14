import streamlit as st, pandas as pd, matplotlib.pyplot as plt
from db import list_queries, close_query, get_image
st.set_page_config(page_title="Support Dashboard", layout="wide")
if "user" not in st.session_state or st.session_state.user is None or st.session_state.user["role"] != "Support":
    st.error("Login as Support to access this page")
else:
    st.title("Support Dashboard")
    f1, f2 = st.columns([1,2])
    with f1:
        status = st.selectbox("Filter by Status", ["All","Open","Closed"])
    with f2:
        search = st.text_input("Search")
    df = list_queries(status=status, search=search)
    st.dataframe(df, use_container_width=True, hide_index=True)
    c1, c2 = st.columns([1,1])
    with c1:
        st.subheader("Close Query")
        qid = st.number_input("Enter Query ID", min_value=1, step=1)
        if st.button("Mark Closed", use_container_width=True):
            try:
                close_query(int(qid))
                st.success("Updated")
            except:
                st.error("Invalid ID")
    with c2:
        st.subheader("View Screenshot")
        qid_view = st.number_input("Query ID for Image", min_value=1, step=1, key="viewid")
        if st.button("Show Image", use_container_width=True):
            img = get_image(int(qid_view))
            if img:
                st.image(img)
            else:
                st.info("No image attached")
    st.subheader("Status Distribution")
    counts = df["status"].value_counts().reindex(["Open","Closed"]).fillna(0)
    fig = plt.figure(figsize=(2.8,2.8))
    wedges, texts, autotexts = plt.pie(counts.values, labels=counts.index, autopct="%1.0f%%", startangle=90, colors=["#2563eb","#22c55e"], pctdistance=0.8, textprops={"color":"#0f172a","weight":"bold"})
    centre_circle = plt.Circle((0,0),0.58,fc="#ffffff")
    fig.gca().add_artist(centre_circle)
    plt.axis("equal")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=False)
    st.subheader("Download")
    st.download_button("Download CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="queries.csv", mime="text/csv")