'''
@Description:
@Author: michael
@Date: 2021-08-31 10:00:00
LastEditTime: 2021-08-31 20:00:00
LastEditors: michael
'''

class ApiPressure:

    # -------接口性能测试配置-------
    # 接口类型
    method = "post"

    # 接口地址
    # url = "http://localhost:8081/swcw/back/sysLogin.action"
    # 接口参数
    # data = {"username": "admin", "password": "123456"}

    # url = "http://118.193.47.247:8007/api/search/general_search"
    # data = b'{"id": "123","search_content": "3E Bioventures Capital"}'

    # url = "http://118.193.47.247:8007/api/fund/fund_list"
    # data = b'{"uid": "27"}'

    # 线程数
    thread_num = 1

    # 每个线程循环次数
    one_work_num = 1

    # 每次请求时间间隔
    loop_sleep = 0

    # 平均响应时间列表
    response_time = []

    # 错误信息列表
    error = []

    # 接口 200， 但是返回的信息是错误的列表 
    error_info_list = []


    # 设置 check_request 接口访问的配置值
    def check_request_config(self):
    
        self.method = "post"
        self.url = "http://118.193.47.247:8007/api/meeting/check_request"
        self.data = b'{"id": "149","request_type": "1","data_num": "3"}'
        self.thread_num = 1
        self.one_work_num = 1
        self.loop_sleep = 0
        self.response_time = []
        self.error = []
        self.error_info_list = []


    # 查看返回 code 是否成功
    def check_request(self, info_result):

        # 查看返回 code 码是否正确
        # if info_result['code'] != 200:
        #     return info_result['message']

        # 查看返回值数量是否与 postMan 一致 - check_request 接口测试
        if info_result['count'] != 6:
            return ['check_request_count count:' + str(info_result['count'])]

        return []

        # 查看返回值的接口测试 - general_search 接口测试
        # if info_result['code'] != 200:
        #     error_info_list.append(info_result)
        # else:
        #     if len(info_result['data']) != 1:
        #         error_info_list.append('error info 1')
        # return {'code': 201, 'message': '添加搜索日志失败'}

        return []






