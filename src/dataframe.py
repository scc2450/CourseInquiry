########################
# Data frame setup
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

def soup_parser(course_data, mode='inquiry'):
    for course in course_data:
        sksj_soup = BeautifulSoup(course['sksj'], 'html.parser')
        sksj_list = [p.text for p in sksj_soup.find_all('p')]
        sksj = "，".join(sksj_list) if sksj_list else "时间单独分配"
        course['sksj'] = sksj
        teacher_soup = BeautifulSoup(course['teacher'], 'html.parser')
        teacher_list = [p.text for p in teacher_soup.find_all('p')]
        teacher = "/".join(teacher_list) if teacher_list else "未指定"
        course['teacher'] = teacher
        if mode == 'inquiry':
            course['kch'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kch']
            course['kcmc'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kcmc']
    return course_data

column_config_download = {
    'xh': '序号',
    'kch': '课程号',
    'kcmc': '课程名称',
    'kctxm': '课程体系名',
    'kkxsmc': '开课系所名称',
    'sksj': '上课时间',
    'teacher': '教师',
    'zxjhbh': '教学计划编号',
    'jxbh': '教学班号',
    'qzz': '起止周',
    'xf': '学分',
    'bz': '备注'
}

column_config = {
    'xh': None,
    'kch': st.column_config.LinkColumn(
        "课程号",
        help="点击查看课程详情",
        display_text=r"https:.*#(.*?)$",
        width='small'
    ),
    'kcmc': st.column_config.LinkColumn(
        "课程名称",
        help="点击查看课程详情",
        display_text=r"https:.*#(.*?)$",
    ),
    'kctxm': None,
    'kkxsmc': '开课系所名称',
    'sksj': '上课时间',
    'teacher': '教师',
    'zxjhbh': None,
    'jxbh': None,
    'qzz': '起止周',
    'xf': st.column_config.NumberColumn(
        "学分",
        format="%.1f",
        width='small',
    ),  
    'bz': '备注',
}