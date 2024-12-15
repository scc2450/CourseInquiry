########################
# Page Configuration
# version 1.0
# author: Erik
# date: 12/15/2024
########################


import streamlit as st
from const import Server
from payload import Payload
from client import CourseSearchClient
from dataframe import column_config, soup_parser
from download import download_all

def run():
    st.set_page_config(page_title='PKU Course Search', layout='wide')
    st.header('White Whale Univ. Course Search')
    st.image(Server.Head_img, use_container_width=True)

    st.sidebar.title('欢迎使用课程信息查询镜像')
    st.sidebar.markdown('**当前搜索条件**')

    my_payload = Payload()
    my_payload.set()
    st.sidebar.write(f"课程名称/课程号: {my_payload.coursename}")
    st.sidebar.write(f"教师名称: {my_payload.teachername}")
    st.sidebar.write(f"年份与学期: {my_payload.yearandseme}")
    st.sidebar.write(f"课程类型: {my_payload.coursetype}")
    st.sidebar.write(f"开课系所: {my_payload.yuanxi}")

    if 'show_form' not in st.session_state:
        st.session_state.show_form = False
        st.session_state.startrow = '0'
    if st.button('查询'):
        st.session_state.show_form = True
        my_payload.setstartrow(st.session_state.startrow)
    if st.session_state.show_form:
        client = CourseSearchClient()
        client.search(payload=my_payload.get())
        course_data = soup_parser(client.course_data)
        st.dataframe(course_data, column_config =column_config, use_container_width=True)
        max_page_index = client.max_page_index
        page_index = st.number_input('页码(修改页码后请再次单击‘查询’)', min_value=1, step=1, max_value=max_page_index, value=1)
        st.session_state.startrow = str((page_index - 1) * 100)

    with st.sidebar:
        if st.button('抓取全部'):
            download_all(my_payload.get())