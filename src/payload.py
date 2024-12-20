########################
# Payload class
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st
import pandas as pd
from .const import *

class OnlinePayload:
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
        self.startrow = str(startrow)
    
    def set(self):
        self.setcoursename()
        self.setteachername()
        self.setyearandseme()
        self.setcoursetype()
        self.setyuanxi()

    def get(self):
        self.startrow = st.session_state.startrow
        return {
            'coursename': self.coursename,
            'teachername': self.teachername,
            'yearandseme': self.yearandseme,
            'coursetype': self.coursetypecode,
            'yuanxi': self.yuanxicode,
            'startrow': self.startrow
        }
    
class OfflinePayload:
    def __init__(self):
        self.courseName = 'unset'
        self.year = CourseScheduleList.init_payload['year']
        self.term = CourseScheduleList.init_payload['term']
        self.courseScheduleType = CourseScheduleList.init_payload['courseScheduleType']
        self.courseScheduleTypeName = 'unset'
        self.deptId = CourseScheduleList.init_payload['deptId']
        self.deptName = 'unset'
        self.courseType = 'unset'
        self.courseTypeName = 'unset'
        self.col1, self.col2 = st.columns(2)
        self.deptId_list = get_list(Colleges.list, 'id')
    
    def setcoursename(self):
        self.courseName = self.col1.text_input('课程名称/关键字',help='暂不支持课程号搜索')

    def setcourseScheduleType(self):
        self.courseScheduleTypeName = self.col2.selectbox('课表类型', ['本科生课表', '研究生课表'], index=0)
        self.courseScheduleType = 'BKSKB' if self.courseScheduleTypeName == '本科生课表' else 'YJSKB'

    def format_year(self, year):
        if year >= 2010:
            return f'{year-2000}-{year-1999}'
        elif year == 2009:
            return '09-10'
        elif year >= 2000:
            return f'0{year-2000}-0{year-1999}'
        elif year == 1999:
            return '99-00'
        else:
            return f'{year-1900}-{year-1899}'
        
    def setyearandseme(self):
        year_now = pd.Timestamp.now().year
        year = self.col1.number_input('年份', min_value=1998, max_value=year_now+1, value=year_now, help='研究生课程数据可查询的时间范围为1998秋季至今')
        semester_now = '春季' if pd.Timestamp.now().month < 7 or year == year_now+1 else '秋季' if pd.Timestamp.now().month > 8 else '暑校'
        semester = self.col2.selectbox('学期', ['春季', '秋季', '暑校'], index=0 if semester_now == '春季' else 1 if semester_now == '秋季' else 2)
        year = year if semester == '秋季' else year - 1
        self.year = self.format_year(year)
        self.term = f'{1 if semester == "秋季" else 2 if semester == "春季" else 3}'

    def setcoursetype(self):
        courses_type_list = get_list(Undergraduate_course_type.list) if self.courseScheduleType == 'BKSKB' else get_list(Postgraduate_course_type.list)
        self.courseTypeName = st.selectbox('课程类型', courses_type_list)
        courese_type_dict =  get_dict(Undergraduate_course_type.list) if self.courseScheduleType == 'BKSKB' else get_dict(Postgraduate_course_type.list)
        format_coursetype = lambda x: courese_type_dict[x]
        self.courseType = format_coursetype(self.courseTypeName)

    def setdeptId(self):
        self.deptName = st.selectbox('开课系所', get_list(Colleges.list),index=1)
        format_deptId = lambda x: get_dict(Colleges.list)[x]
        self.deptId = format_deptId(self.deptName)

    def set(self):
        self.setcoursename()
        self.setcourseScheduleType()
        self.setyearandseme()
        self.setcoursetype()
        self.setdeptId()

    def get(self):
        json = {
            'courseName': self.courseName,
            'courseScheduleType': self.courseScheduleType,
            'courseType': self.courseType,
            'deptId': self.deptId,
            'term': self.term,
            'year': self.year
        }
        if json['courseName'] == 'unset':
            json.pop('courseName')
        if json['courseType'] == '':
            json.pop('courseType')
        return json
    
    def get_all_colleges(self):
        if 'all' in self.deptId_list:
            self.deptId_list.remove('all')
        for id in self.deptId_list:
            self.deptId = id
            yield self.get()