########################
# Download all course data
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
from .client import CourseSearchClient
from .dataframe import soup_parser, column_config_download
import pandas as pd
from io import StringIO, BytesIO
import time

def download_all(payload):
    all_course_data = []
    client = CourseSearchClient()
    client.search(payload=payload, mode='download')
    all_course_data = client.course_data
    loop_count = client.max_page_index
    status_bar = st.progress(1/loop_count)
    for i in range(1, loop_count) if loop_count >= 1 else range(0):
        payload['startrow'] = str(i * 100)
        client.search(payload=payload, mode='download')
        course_data = client.course_data
        all_course_data.extend(course_data)
        status_bar.progress((i+1) / loop_count)
    time.sleep(1)
    status_bar.progress(1)
    st.success(f"共抓取{len(all_course_data)}条课程信息")
    soup_parser(all_course_data, mode='download')
    # 转存为csv文件
    df = pd.DataFrame(all_course_data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_data = csv_buffer.getvalue()
    st.download_button(
        label="下载为csv",
        data=csv_data,
        file_name=f"{payload['coursename']}_{payload['teachername']}_{payload['yearandseme']}_{payload['coursetype']}_{payload['yuanxi']}.csv",
        mime="text/csv",
    )
    # 转存为excel文件
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Courses")
    excel_buffer.seek(0)  # 将文件指针移到开头
    st.download_button(
        label="下载为Excel(xlsx)",
        data=excel_buffer,
        file_name=f"{payload['coursename']}_{payload['teachername']}_{payload['yearandseme']}_{payload['coursetype']}_{payload['yuanxi']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )