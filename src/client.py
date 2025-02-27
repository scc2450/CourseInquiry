########################
# client for course inquiry
# version 1.0
# author: Erik
# date: 12/151/2024
########################

from .const import headers, init_payload, Server
from .utils import Singleton

import requests, streamlit as st

class CourseSearchClient(metaclass=Singleton):
    def __init__(self):
        self.headers = headers
        self.payload = init_payload
        self.response_data = {'status':'init','courselist':[],'count':0}
        self.course_data = None
        self.all_course_conut = 0
        self.max_page_index = 1
        self.page_index = 1
    
    def search(self, depth=1, payload=None, mode='inquiry'):
        self.payload = payload if payload else self.payload
        response = requests.post(Server.Target, data=self.payload, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            st.error("网络连接失败")    
        else:
            try:
                response_data = response.json()  # 尝试解析 JSON
            except requests.JSONDecodeError:
                st.write("响应不是有效的 JSON 格式：", response.text)
            if response_data['status'] == 'ok' and response_data['count'] != 0:
                if mode == 'inquiry':
                    st.success(f"查询成功, 共查询到{response_data['count']}条课程信息，当前展示第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
                elif mode == 'download':
                    # st.success(f"共{response_data['count']}条课程信息，正在抓取第{response_data['courselist'][0]['xh']}-{response_data['courselist'][-1]['xh']}条")
                    pass
            else:
                if depth <= 1:
                    self.payload['startrow'] = '0'
                    return self.search(depth=depth+1, payload=self.payload, mode=mode)
                else:
                    st.error("未查询到任何课程信息")
                    return []
            self.response_data = response_data
            self.course_data = response_data['courselist']
            self.all_course_conut = int(response_data['count'])
            self.max_page_index = self.all_course_conut // 100 + 1 if self.all_course_conut % 100 != 0 else self.all_course_conut // 100
            return self.response_data
