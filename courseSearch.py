import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

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

payload = {
    'coursename': '',
    'teachername': '',
    'yearandseme': '12-13-1',
    'coursetype': '0',
    'yuanxi': '0',
    'startrow': '0'
}
col1, col2 = st.columns(2)
payload['coursename'] = col1.text_input('课程名称/课程号')
payload['teachername'] = col2.text_input('教师名称')
# 年份与学期
year = col1.number_input('年份', min_value=2000, max_value=2024, value=2024)
semester = col2.selectbox('学期', ['春季', '秋季'])
year = year - 1 if semester == '春季' else year
payload['yearandseme'] = f'{year-2000}-{year-1999}-{1 if semester == "秋季" else 2}'
# 课程类型映射
# format_func = lambda x: x if x != '全部' else '0'
coursetype_list = ['全部', '思政必修', '思政选择性必修', '劳动教育课', '大学英语', '体育', '通识核心课', '通选课', '全校公选课', '英语授课', '与中国有关的课程']
format_coursetype = lambda x: {
    '全部': '0',
    '思政必修': '1-08',
    '思政选择性必修': '2-思政选择性必修课',
    '劳动教育课': '2-劳动教育课',
    '大学英语': '1-09',
    '体育': '1-11',
    '通识核心课': '2-通识核心课',
    '通选课': '2-通选课',
    '英语授课': '3-英文',
    '与中国有关的课程': '2-与中国有关课程',
    '全校公选课': '1-07',
}[x]
payload['coursetype'] = format_coursetype(st.selectbox('课程类型', coursetype_list))
# st.write(payload['coursetype'])
yuanxi_list = ['全部', '数院', '物院', '化院', '生科', '地空', '工院', '信科', '心院', '软微', '新传', '中文', '历史', '考古', '哲学', '国关', '经院', '国发', '光华', '法院', '信管', '社系', '政管', '大英', '外院', '马院', '体教', '艺术', '元培', '城环', '环科', '教务部', '医学部']
format_yuanxi = lambda x: {
    '全部': '0',
    '数院': '00001',
    '物院': '00004',
    '化院': '00010',
    '生科': '00011',
    '地空': '00012',
    '工院': '00086',
    '信科': '00048',
    '心院': '00016',
    '软微': '00017',
    '新传': '00018',
    '中文': '00020',
    '历史': '00021',
    '考古': '00022',
    '哲学': '00023',
    '国关': '00024',
    '经院': '00025',
    '国发': '00062',
    '光华': '00028',
    '法院': '00029',
    '信管': '00030',
    '社系': '00031',
    '政管': '00032',
    '大英': '00038',
    '外院': '00039',
    '马院': '00040',
    '体教': '00041',
    '艺术': '00043',
    '元培': '00046',
    '城环': '00126',
    '环科': '00127',
    '教务部': '00612',
    '医学部': '10180',
}[x]
payload['yuanxi'] = format_yuanxi(st.selectbox('开课系所', yuanxi_list))
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
    st.session_state.startrow = '0'
if st.button('查询'):
    st.session_state.show_form = True
    payload['startrow'] = st.session_state.startrow
if st.session_state.show_form:
    response_data={'status':'init','courselist':[],'count':0}
    response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload)
    
    if response.status_code == 200:  # 确保状态码为 200
        try:
            response_data = response.json()  # 尝试解析 JSON
        except requests.JSONDecodeError:
            st.write("响应不是有效的 JSON 格式：", response.text)
            print(1111111111111111111)
    else:
        print(response.status_code)
        st.error("网络连接失败")
    if response_data['status'] == 'ok':
        st.success(f"查询成功, 共查询到: {response_data['count']}条课程信息，当前展示第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
    if response_data['status'] == 'no':
        payload['startrow'] = '0'
        response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload)
        st.success(f"查询成功, 共查询到: {response_data['count']}条课程信息，当前展示第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
    # print(response.text)

    # for course in response['courselist']:
    #     with st.form(f"form_{course['xh']}"):
    #         st.subheader(f"课程: {course['kcmc']} (编号: {course['kch']})")

    #         # 提取和展示上课时间
    #         sksj_soup = BeautifulSoup(course['sksj'], 'html.parser')
    #         sksj_list = [p.text for p in sksj_soup.find_all('p')]
    #         sksj = "，".join(sksj_list)

    #         # 提取教师信息
    #         teacher_soup = BeautifulSoup(course['teacher'], 'html.parser')
    #         teacher = teacher_soup.text.strip() if teacher_soup.text else "未指定"

    #         # 表单字段
    #         st.text_input("课程名称", value=course['kcmc'], key=f"kcmc_{course['xh']}")
    #         st.text_input("开课学院", value=course['kkxsmc'], key=f"kkxsmc_{course['xh']}")
    #         st.text_area("上课时间", value=sksj, key=f"sksj_{course['xh']}")
    #         st.text_input("教师", value=teacher, key=f"teacher_{course['xh']}")
    #         st.number_input("学分", value=float(course['xf']), key=f"xf_{course['xh']}", min_value=0.0, step=0.5)
    #         st.text_input("备注", value=course['bz'], key=f"bz_{course['xh']}")

    #         # 提交按钮
    #         submitted = st.form_submit_button("保存")
    course_data = response_data['courselist']
    soup_parser(course_data)
    
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
        'kch': '课程号',
        'kcmc': '课程名称',
        'kctxm': None,
        'kkxsmc': '开课系所名称',
        'sksj': '上课时间',
        'teacher': '教师',
        'zxjhbh': None,
        'jxbh': None,
        'qzz': None,
        'xf': '学分',
        'bz': None,
    }
    st.dataframe(course_data, column_config =column_config)
    max_page_index = int(response_data['count']) // 100 + 1
    page_index = st.number_input('页码', min_value=1, step=1, max_value=max_page_index, value=1)
    st.session_state.startrow = str((page_index - 1) * 100)

# 转存为csv文件
import csv
from bs4 import BeautifulSoup