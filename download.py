########################
# Download all course data
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
from client import CourseSearchClient
from dataframe import soup_parser
from dataframe import column_config_download
import pandas as pd
from io import StringIO

def download_all(payload):
    all_course_data = []
    client = CourseSearchClient()
    client.search(payload=payload, mode='download')
    all_course_data = client.course_data
    loop_count = client.max_page_index
    for i in range(1, loop_count) if loop_count >= 1 else range(0):
        payload['startrow'] = str(i * 100)
        client.search(payload=payload, mode='download')
        course_data = client.course_data
        all_course_data.extend(course_data)
    soup_parser(all_course_data, mode='download')
    # 转存为csv文件
    df = pd.DataFrame(all_course_data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_data = csv_buffer.getvalue()
    st.download_button(
        label="下载全部",
        data=csv_data,
        file_name=f"{payload['coursename']}_{payload['teachername']}_{payload['yearandseme']}_{payload['coursetype']}_{payload['yuanxi']}.csv",
        mime="text/csv",
    )