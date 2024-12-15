########################
# Course Inquiry
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from const import Server
from payload import Payload
from dataframe import column_config
from dataframe import soup_parser
from client import CourseSearchClient
st.set_page_config(page_title='PKU Course Search', layout='wide')
st.header('White Whale Univ. Course Search')
st.image(Server.Head_img, use_column_width=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

payload = {
    'coursename': '',
    'teachername': '',
    'yearandseme': '12-13-1',
    'coursetype': '0',
    'yuanxi': '0',
    'startrow': '0'
}

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

# 尝试下载全部
all_course_data = []
with st.sidebar.expander('下载全部课程信息'):
    st.write('点击按钮下载全部课程信息至本地')
    if st.button('抓取全部'):
        st.spinner('正在下载全部课程信息...')
        response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload, headers=headers)
        response_data = response.json()
        all_course_data = response_data['courselist']
        loop_count = int(response_data['count']) // 100 + 1 if int(response_data['count']) % 100 != 0 else int(response_data['count']) // 100
        for i in range(1, loop_count) if loop_count > 1 else range(0):
            payload['startrow'] = str(i * 100)
            response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload, headers=headers)
            response_data = response.json()
            course_data = response_data['courselist']
            all_course_data.extend(course_data)
        soup_parser(all_course_data)
        # 转存为csv文件
        df = pd.DataFrame(all_course_data)
        df.to_csv('course_data.csv', index=False, encoding='utf-8-sig')
        st.success('已下载全部课程信息至本地，文件名为course_data.csv')