
import streamlit as st

from . import online, offline

def run():
    st.set_page_config(page_title='PKU Course Search', layout='wide')
    st.header('White Whale Univ. Course Search')
    options = ['在线查询', '离线查询（支持研究生课程）']
    selection = st.segmented_control(
        " ", options, selection_mode="single", default='离线查询（支持研究生课程）'
    )
    index_sidebar = st.sidebar.empty()
    if selection == '在线查询':
        online.run(index_sidebar)
    else:
        offline.run(index_sidebar)
