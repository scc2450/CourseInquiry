########################
# client for course inquiry
# version 1.0
# author: Erik
# date: 12/151/2024
########################
from const import headers, init_payload, Server
import requests
class Singleton(type):
    """
    Singleton Metaclass
    @link https://github.com/jhao104/proxy_pool/blob/428359c8dada998481f038dbdc8d3923e5850c0e/Util/utilClass.py
    """
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._inst[cls]

class CourseSearchClient(metaclass=Singleton):
    def __init__(self):
        self.headers = headers
        self.payload = init_payload
        self.response_data = None
        self.course_data = None
        self.max_page_index = 1
        self.page_index = 1
        self.all_course_conut = 0
    
    def search(self, payload):
        self.payload = payload
        response = requests.post(Server.Target, data=payload, headers=headers)
        # if response.status_code == 200: