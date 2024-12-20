########################
# Postgraduate Configuration
# version 1.0
# author: Erik
# date: 12/20/2024
########################

import streamlit as st
import pandas as pd
import os
from .const import Server, DataFrame
from .payload import OfflinePayload
from .dataframe import column_config, soup_parser
from .download import download_all

def run(index_sidebar):
    st.image(Server.Head_img, use_container_width=True)
    my_payload = OfflinePayload()
    my_payload.set()
    with index_sidebar.container():
        st.title('欢迎使用课程信息查询镜像')
        st.markdown('数据源：[信息门户](https://portal.pku.edu.cn/publicQuery/#/courseSchedule)')
        st.divider()
        st.markdown(f'**{my_payload.courseScheduleTypeName}-当前搜索条件**')
        st.sidebar.write(f"课程名称/关键字: {my_payload.courseName}") if my_payload.courseName else None
        st.sidebar.write(f"年份与学期: {my_payload.year}-{my_payload.term}")
        st.sidebar.write(f"课程类型: {my_payload.courseTypeName}")
        st.sidebar.write(f"开课系所: {my_payload.deptName}")
    file_path = f'file/{my_payload.courseScheduleType}/{my_payload.year}-{my_payload.term}_{my_payload.courseScheduleType}_all_courses.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if my_payload.deptId != 'all':
            df = df[df['开课系所'] == int(my_payload.deptId)]
        if my_payload.courseName:
            df = df[df['courseName'].str.contains(my_payload.courseName, case=False, na=False)]
        if my_payload.courseType != '':
            df = df[df['courseType'] == my_payload.courseTypeName]
        st.success(f"共查询到{df.shape[0]}条{'' if my_payload.deptId=='all' else my_payload.deptName}于{my_payload.year}-{my_payload.term}开设的{my_payload.courseScheduleTypeName[:3]}课程({my_payload.courseTypeName})")
        if df.shape[0] > 0:
            st.dataframe(df, column_config = DataFrame.column_config, column_order=DataFrame.column_config, use_container_width=True, hide_index=True)
        else:
            st.warning("无符合搜索条件的数据")
    else:
        df = pd.DataFrame()
        st.warning("该搜索条件无可查询数据")
