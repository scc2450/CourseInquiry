########################
# Constants for the Course Inquiry Project
# version 1.0
# author: Erik
# date: 12/15/2024
########################

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
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
