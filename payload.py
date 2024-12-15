########################
# Payload class
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
import pandas as pd
from const import init_payload, College, Course

class Payload:
    def __init__(self):
        self.coursename = init_payload['coursename']
        self.teachername = init_payload['teachername']
        self.yearandseme = init_payload['yearandseme']
        self.coursetypecode = init_payload['coursetype']
        self.yuanxicode = init_payload['yuanxi']
        self.coursetype = 'unset'
        self.yuanxi = 'unset'
        self.startrow = init_payload['startrow']
        self.col1, self.col2 = st.columns(2)
    
    def setcoursename(self):
        self.coursename = self.col1.text_input('课程名称/课程号/关键字')

    def setteachername(self):
        self.teachername = self.col2.text_input('教师名称/关键字')

    def setyearandseme(self):
        year_now = pd.Timestamp.now().year
        year = self.col1.number_input('年份', min_value=2010, max_value=year_now+1, value=year_now, help='可查询的时间范围为2012秋季至今')
        semester_now = '春季' if pd.Timestamp.now().month < 7 or year == year_now+1 else '秋季' if pd.Timestamp.now().month > 8 else '暑校'
        semester = self.col2.selectbox('学期', ['春季', '秋季', '暑校'], index=0 if semester_now == '春季' else 1 if semester_now == '秋季' else 2)
        year = year if semester == '秋季' else year - 1
        self.yearandseme = f'{year-2000}-{year-1999}-{1 if semester == "秋季" else 2 if semester == "春季" else 3}'

    def setcoursetype(self):
        self.coursetype = st.selectbox('课程类型', Course.type_list)
        format_coursetype = lambda x: Course.type_code_dict[x]
        self.coursetypecode = format_coursetype(self.coursetype)

    def setyuanxi(self):
        self.yuanxi = st.selectbox('开课系所', College.name_list)
        format_yuanxi = lambda x: College.name_code_dict[x]
        self.yuanxicode = format_yuanxi(self.yuanxi)

    def setstartrow(self, startrow):
        self.startrow = startrow
    
    def set(self):
        self.setcoursename()
        self.setteachername()
        self.setyearandseme()
        self.setcoursetype()
        self.setyuanxi()

    def get(self):
        return {
            'coursename': self.coursename,
            'teachername': self.teachername,
            'yearandseme': self.yearandseme,
            'coursetype': self.coursetypecode,
            'yuanxi': self.yuanxicode,
            'startrow': self.startrow
        }
    