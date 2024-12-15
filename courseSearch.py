import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
st.set_page_config(page_title='PKU Course Search', layout='wide')
st.header('White Whale Univ. Course Search')
st.image('https://dean.pku.edu.cn/service/web/images/banner/banner_net.jpg', use_column_width=True)
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
col1, col2 = st.columns(2)
payload['coursename'] = col1.text_input('课程名称/课程号/关键字')
payload['teachername'] = col2.text_input('教师名称/关键字')
# 年份与学期
year_now = pd.Timestamp.now().year
year = col1.number_input('年份', min_value=2010, max_value=year_now+1, value=year_now, help='可查询的时间范围为2012秋季至今')
semester_now = '春季' if pd.Timestamp.now().month < 7 or year == year_now+1 else '秋季' if pd.Timestamp.now().month > 8 else '暑校'
semester = col2.selectbox('学期', ['春季', '秋季', '暑校'], index=0 if semester_now == '春季' else 1 if semester_now == '秋季' else 2)
year = year if semester == '秋季' else year - 1
payload['yearandseme'] = f'{year-2000}-{year-1999}-{1 if semester == "秋季" else 2 if semester == "春季" else 3}'
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
coursetype = st.selectbox('课程类型', coursetype_list)
payload['coursetype'] = format_coursetype(coursetype)
# st.write(payload['coursetype'])
yuanxi_list = [
    '全部-ALL', '数院-SMS', '物院-PHY', '化院-CHEM', '生科-BIO', '地空-SESS', '工院-COE', '信科-CSEE', 
    '心院-PSY', '软微-SS', '新传-SJC', '中文-CHN', '历史-HIST', '考古-ARC', '哲学-PHIL', '国关-SIS', 
    '经院-ECO', '国发-NSD', '光华-GSM', '汇丰-PHBS', '法院-LAW', '信管-IM', '社系-SOCI', '政管-SG', 
    '大英-ENG', '外院-SFL', '马院-MAR', '体教-PE', '艺术-SOA', '元培-YPC', '城环-UES', '环科-CESE', 
    '材料-MSE', '叉院-AAIS', '教务部-DEAN', '医学部-BJMU', '武装部-XGB', '教育学院-GSE', '歌剧研究院-OPE', 
    '现代农学院-SAAS', '人口研究所-IPR', '人工智能研究院-AI', '建筑与景观学院-CALA', '对外汉语教育学院-HANYU', 
    '产业技术研究院-KJKFB', '中国社科调查中心-ISSS', '创新创业学院-NEW', '共青团北大委员会-YOUTH'
]
format_yuanxi = lambda x: {
    '全部-ALL': '0',
    '数院-SMS': '00001',
    '物院-PHY': '00004',
    '化院-CHEM': '00010',
    '生科-BIO': '00011',
    '地空-SESS': '00012',
    '工院-COE': '00086',
    '信科-CSEE': '00048',
    '心院-PSY': '00016',
    '软微-SS': '00017',
    '新传-SJC': '00018',
    '中文-CHN': '00020',
    '历史-HIST': '00021',
    '考古-ARC': '00022',
    '哲学-PHIL': '00023',
    '国关-SIS': '00024',
    '经院-ECO': '00025',
    '国发-NSD': '00062',
    '光华-GSM': '00028',
    '汇丰-PHBS': '00201',     
    '法院-LAW': '00029',
    '信管-IM': '00030',
    '社系-SOCI': '00031',
    '政管-SG': '00032',
    '大英-ENG': '00038',
    '外院-SFL': '00039',
    '马院-MAR': '00040',
    '体教-PE': '00041',
    '艺术-SOA': '00043',
    '元培-YPC': '00046',
    '城环-UES': '00126',
    '环科-CESE': '00127',
    '材料-MSE': '00232',
    '叉院-AAIS': '00084',
    '教务部-DEAN': '00612',
    '医学部-BJMU': '10180',
    '武装部-XGB': '00607',
    '教育学院-GSE': '00067',
    '歌剧研究院-OPE': '00192',
    '现代农学院-SAAS': '00211',
    '人口研究所-IPR': '00068',
    '人工智能研究院-AI': '00225',
    '建筑与景观学院-CALA': '00195',
    '对外汉语教育学院-HANYU': '00044',
    '产业技术研究院-KJKFB': '00199',
    '中国社科调查中心-ISSS': '00187',
    '创新创业学院-NEW': '00671',
    '共青团北大委员会-YOUTH': '00651',

}[x]
yuanxi = st.selectbox('开课系所', yuanxi_list)
payload['yuanxi'] = format_yuanxi(yuanxi)

st.sidebar.write(f"课程名称/课程号: {payload['coursename']}")
st.sidebar.write(f"教师名称: {payload['teachername']}")
st.sidebar.write(f"年份与学期: {payload['yearandseme']}")
st.sidebar.write(f"课程类型: {coursetype}")
st.sidebar.write(f"开课系所: {yuanxi}")

if 'show_form' not in st.session_state:
    st.session_state.show_form = False
    st.session_state.startrow = '0'
if st.button('查询'):
    st.session_state.show_form = True
    payload['startrow'] = st.session_state.startrow
if st.session_state.show_form:
    response_data={'status':'init','courselist':[],'count':0}
    response = requests.post('https://dean.pku.edu.cn/service/web/courseSearch_do.php', data=payload, headers=headers)
    
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
    #拼接课程详情链接
    for course in course_data:
        course['kch'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kch']
        course['kcmc'] = 'https://dean.pku.edu.cn/service/web/courseDetail.php?flag=1&zxjhbh=' + course['zxjhbh'] + '#' + course['kcmc']
    
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
        'xf': st.column_config.NumberColumn(
            "学分",
            format="{:.1f}",
            width='small'
        ),  
        'bz': '备注',
    }
    st.dataframe(course_data, column_config =column_config, use_container_width=True)
    max_page_index = int(response_data['count']) // 100 + 1
    page_index = st.number_input('页码(修改页码后请再次单击‘查询’)', min_value=1, step=1, max_value=max_page_index, value=1)
    st.session_state.startrow = str((page_index - 1) * 100)

# 转存为csv文件
import csv
from bs4 import BeautifulSoup