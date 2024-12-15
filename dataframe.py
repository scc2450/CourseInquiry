########################
# Data frame setup
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
import pandas as pd

# column_config = {
#     'xh': '序号',
#     'kch': '课程号',
#     'kcmc': '课程名称',
#     'kctxm': '课程体系名',
#     'kkxsmc': '开课系所名称',
#     'sksj': '上课时间',
#     'teacher': '教师',
#     'zxjhbh': '教学计划编号',
#     'jxbh': '教学班号',
#     'qzz': '起止周',
#     'xf': '学分',
#     'bz': '备注'
# }

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