import streamlit as st
from db import insert_query
st.set_page_config(page_title="Client Submission")
if "user" not in st.session_state or st.session_state.user is None or st.session_state.user["role"] != "Client":
    st.error("Login as Client to access this page")
else:
    st.title("Submit a Query")
    with st.form("client_form"):
        mail = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        head = st.text_input("Query Heading")
        desc = st.text_area("Query Description", height=160)
        img = st.file_uploader("Attach Screenshot (optional)", type=["png","jpg","jpeg"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            img_bytes = img.read() if img else None
            if mail and mobile and head and desc:
                insert_query(mail, mobile, head, desc, img_bytes)
                st.success("Query submitted")
            else:
                st.error("Fill all required fields")