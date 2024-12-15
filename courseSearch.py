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
st.set_page_config(page_title='PKU Course Search', layout='wide')
st.header('White Whale Univ. Course Search')
st.image(Server.Head_img, use_column_width=True)
def soup_parser(course_data):
    for course in course_data:
        sksj_soup = BeautifulSoup(course['sksj'], 'html.parser')
        sksj_list = [p.text for p in sksj_soup.find_all('p')]
        sksj = "，".join(sksj_list) if sksj_list else "时间单独分配"
        course['sksj'] = sksj
        teacher_soup = BeautifulSoup(course['teacher'], 'html.parser')
        teacher_list = [p.text for p in teacher_soup.find_all('p')]
        teacher = "/".join(teacher_list) if teacher_list else "未指定"
        course['teacher'] = teacher
    return course_data

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
    payload['startrow'] = st.session_state.startrow
if st.session_state.show_form:
    response_data={'status':'init','courselist':[],'count':0}
    response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=my_payload.get(), headers=headers)
    
    if response.status_code == 200:  # 确保状态码为 200
        try:
            response_data = response.json()  # 尝试解析 JSON
        except requests.JSONDecodeError:
            st.write("响应不是有效的 JSON 格式：", response.text)
    else:
        print(response.status_code)
        st.error("网络连接失败")
    # st.write(payload['startrow'])
    # st.json(response_data)
    if response_data['status'] == 'ok' and response_data['count'] != 0:
        st.success(f"查询成功, 共查询到{response_data['count']}条课程信息，当前展示第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
    elif response_data['status'] == 'no':
        payload['startrow'] = '0'
        response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload, headers=headers)
        response_data = response.json()
        if response_data['status'] == 'ok' and response_data['count'] != 0:
            st.success(f"查询成功, 共查询到{response_data['count']}条课程信息，当前展示第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
        else:
            st.error("未查询到任何课程信息")
            
    course_data = response_data['courselist']
    soup_parser(course_data)
    #拼接课程详情链接
    for course in course_data:
        course['kch'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kch']
        course['kcmc'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kcmc']
    
    st.dataframe(course_data, column_config =column_config, use_container_width=True)
    max_page_index = int(response_data['count']) // 100 + 1
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