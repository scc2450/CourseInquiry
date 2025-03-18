########################
# Constants for the Course Inquiry Project
# version 1.0
# author: Erik
# date: 12/15/2024
########################

import streamlit as st

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    "Referer": "https://dean.pku.edu.cn/service/web/courseSearch.php"
}

init_payload = {
    'coursename': '',
    'teachername': '',
    'yearandseme': '12-13-1',
    'coursetype': '0',
    'yuanxi': '0',
    'startrow': '0'
}

class College:
    name_list = [
    '全部-ALL', '数院-SMS', '物院-PHY', '化院-CHEM', '生科-BIO', '地空-SESS', '工院-COE', '信科-CSEE', 
    '心院-PSY', '软微-SS', '新传-SJC', '中文-CHN', '历史-HIST', '考古-ARC', '哲学-PHIL', '国关-SIS', 
    '经院-ECO', '国发-NSD', '光华-GSM', '汇丰-PHBS', '法院-LAW', '信管-IM', '社系-SOCI', '政管-SG', 
    '大英-ENG', '外院-SFL', '马院-MAR', '体教-PE', '艺术-SOA', '元培-YPC', '城环-UES', '环科-CESE', 
    '材料-MSE', '叉院-AAIS', '教务部-DEAN', '医学部-BJMU', '武装部-XGB', '教育学院-GSE', '歌剧研究院-OPE', 
    '现代农学院-SAAS', '人口研究所-IPR', '人工智能研究院-AI', '建筑与景观学院-CALA', '对外汉语教育学院-HANYU', 
    '产业技术研究院-KJKFB', '中国社科调查中心-ISSS', '创新创业学院-NEW', '共青团北大委员会-YOUTH'
]
    name_code_dict = {
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
}

class Course:
    type_list = ['全部', '思政必修', '思政选择性必修', '劳动教育课', '大学英语', '体育', '通识核心课', '通选课', '全校公选课', '英语授课', '与中国有关的课程']
    type_code_dict = {
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
}

class Server:
    HOST = 'dean.pku.edu.cn'
    Head_img = 'https://dean.pku.edu.cn/service/web/images/banner/banner_net.jpg'
    Target = 'https://dean.pku.edu.cn/service/web/courseSearch_do.php'
    Head_gif = 'https://portal.pku.edu.cn/portal2017/img/img_xnmh1.gif'


class DataFrame:
    column_config = {
        "classNo": "班号",
        "courseId": None,
        "courseName": "课程名称",
        "courseType": "课程类型",
        "credits": "学分",
        "remark": "备注",
        "scheduleTime": "上课时间",
        "scheduleWeek": "上课周数",
        "teacher": "教师",
        "url": st.column_config.LinkColumn(
            "课程简介",
            display_text="点击查看课程详情",
        ),
    }
    column_order = ("courseName", "courseType", "credits", "classNo", "scheduleTime", "scheduleWeek", "teacher", "remark", "url")


def get_dict(list, key='name', value='id'):
    return {x[key]: x[value] for x in list}

def get_list(list, index='name'):
    return [x[index] for x in list]

class Undergraduate_course_type:
    num = 16
    list = [
        {
            "id": "",
            "jc": "",
            "name": "不限"
        },
        {
            "id": "01",
            "jc": "",
            "name": "文科生必修"
        },
        {
            "id": "02",
            "jc": "",
            "name": "理科生必修"
        },
        {
            "id": "03",
            "jc": "",
            "name": "专业必修"
        },
        {
            "id": "04",
            "jc": "",
            "name": "任选"
        },
        {
            "id": "05",
            "jc": "",
            "name": "限选"
        },
        {
            "id": "06",
            "jc": "",
            "name": "通选课"
        },
        {
            "id": "07",
            "jc": "",
            "name": "全校公选课"
        },
        {
            "id": "08",
            "jc": "",
            "name": "思想政治"
        },
        {
            "id": "09",
            "jc": "",
            "name": "大学英语"
        },
        {
            "id": "10",
            "jc": "",
            "name": "军事理论"
        },
        {
            "id": "11",
            "jc": "",
            "name": "体育"
        },
        {
            "id": "12",
            "jc": "",
            "name": "毕业论文/设计"
        },
        {
            "id": "13",
            "jc": "",
            "name": "实习实践"
        },
        {
            "id": "14",
            "jc": "",
            "name": "双学位"
        },
        {
            "id": "15",
            "jc": "",
            "name": "辅修"
        }
    ]

class Postgraduate_course_type:
    num = 4
    list = [
        {
            "id": "",
            "jc": "",
            "name": "不限"
        },
        {
            "id": "10",
            "jc": "",
            "name": "必修"
        },
        {
            "id": "20",
            "jc": "",
            "name": "限选"
        },
        {
            "id": "30",
            "jc": "",
            "name": "选修"
        }
    ]

class Colleges:
    num = 48
    list = [
        {
            "id": "all",
            "jc": "全部",
            "name": "全部"
        },
        {
            "id": "00001",
            "jc": "数学",
            "name": "数学科学学院"
        },
        {
            "id": "00004",
            "jc": "物理",
            "name": "物理学院"
        },
        {
            "id": "00010",
            "jc": "化学",
            "name": "化学与分子工程学院"
        },
        {
            "id": "00011",
            "jc": "生科",
            "name": "生命科学学院"
        },
        {
            "id": "00012",
            "jc": "地空",
            "name": "地球与空间科学学院"
        },
        {
            "id": "00013",
            "jc": "环境",
            "name": "环境学院"
        },
        {
            "id": "00016",
            "jc": "心理",
            "name": "心理与认知科学学院"
        },
        {
            "id": "00017",
            "jc": "软微",
            "name": "软件与微电子学院"
        },
        {
            "id": "00018",
            "jc": "新传",
            "name": "新闻与传播学院"
        },
        {
            "id": "00020",
            "jc": "中文",
            "name": "中国语言文学系"
        },
        {
            "id": "00021",
            "jc": "历史",
            "name": "历史学系"
        },
        {
            "id": "00022",
            "jc": "考古",
            "name": "考古文博学院"
        },
        {
            "id": "00023",
            "jc": "哲学",
            "name": "哲学系"
        },
        {
            "id": "00024",
            "jc": "国关",
            "name": "国际关系学院"
        },
        {
            "id": "00025",
            "jc": "经院",
            "name": "经济学院"
        },
        {
            "id": "00028",
            "jc": "光华",
            "name": "光华管理学院"
        },
        {
            "id": "00029",
            "jc": "法学",
            "name": "法学院"
        },
        {
            "id": "00030",
            "jc": "信管",
            "name": "信息管理系"
        },
        {
            "id": "00031",
            "jc": "社会",
            "name": "社会学系"
        },
        {
            "id": "00032",
            "jc": "政管",
            "name": "政府管理学院"
        },
        {
            "id": "00038",
            "jc": "",
            "name": "英语系"
        },
        {
            "id": "00039",
            "jc": "外院",
            "name": "外国语学院"
        },
        {
            "id": "00040",
            "jc": "马院",
            "name": "马克思主义学院"
        },
        {
            "id": "00041",
            "jc": "体教",
            "name": "体育教研部"
        },
        {
            "id": "00042",
            "jc": "科学与社会",
            "name": "科学与社会研究中心"
        },
        {
            "id": "00043",
            "jc": "艺术",
            "name": "艺术学院"
        },
        {
            "id": "00044",
            "jc": "对外汉语",
            "name": "对外汉语教育学院"
        },
        {
            "id": "00046",
            "jc": "元培",
            "name": "元培学院"
        },
        {
            "id": "00048",
            "jc": "信科",
            "name": "信息科学技术学院"
        },
        {
            "id": "00062",
            "jc": "国发",
            "name": "国家发展研究院"
        },
        {
            "id": "00067",
            "jc": "教育",
            "name": "教育学院"
        },
        {
            "id": "00068",
            "jc": "人口",
            "name": "人口研究所"
        },
        {
            "id": "00084",
            "jc": "叉院",
            "name": "前沿交叉学科研究院"
        },
        {
            "id": "00086",
            "jc": "工学",
            "name": "工学院"
        },
        {
            "id": "00100",
            "jc": "",
            "name": "集成电路学院"
        },
        {
            "id": "00101",
            "jc": "",
            "name": "计算机学院"
        },
        {
            "id": "00106",
            "jc": "",
            "name": "智能学院"
        },
        {
            "id": "00107",
            "jc": "",
            "name": "电子学院"
        },
        {
            "id": "00126",
            "jc": "城环",
            "name": "城市与环境学院"
        },
        {
            "id": "00127",
            "jc": "环科",
            "name": "环境科学与工程学院"
        },
        {
            "id": "00182",
            "jc": "分子",
            "name": "分子医学研究所"
        },
        {
            "id": "00192",
            "jc": "歌剧",
            "name": "歌剧研究院"
        },
        {
            "id": "00195",
            "jc": "景观",
            "name": "建筑与景观设计学院"
        },
        {
            "id": "00208",
            "jc": "燕京",
            "name": "燕京学堂"
        },
        {
            "id": "00232",
            "jc": "",
            "name": "材料科学与工程学院"
        },
        {
            "id": "00233",
            "jc": "",
            "name": "未来技术学院"
        },
        {
            "id": "10180",
            "jc": "医学部",
            "name": "医学部教学办"
        }
    ]

class CourseScheduleList:
    init_payload = {
        # 'courseName': "",
        'courseScheduleType': "BKSKB",
        # 'courseType': "",
        'deptId': "00001",
        'term': "1",
        'year': "24-25"
    }
