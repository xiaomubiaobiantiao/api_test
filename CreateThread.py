#!/usr/bin/env pytho
# -*- coding: utf_8 -*-
import threading
import requests
import time
import re
from time import sleep
# from ApiPressure import apiPressure



class CreateThread:

    # -------接口性能测试配置-------
    # 接口类型
    method = "post"

    # 接口地址
    # url = "http://localhost:8081/swcw/back/sysLogin.action"
    # 接口参数
    # data = {"username": "admin", "password": "123456"}

    # url = "http://118.193.47.247:8003/api/meeting/check_request"
    # data = b'{"id": "149","request_type": "1","data_num": "3"}'

    # url = "http://118.193.47.247:8003/api/search/general_search"
    # data = b'{"id": "123","search_content": "3E Bioventures Capital"}'

    url = "http://118.193.47.247:8007/api/fund/fund_list"
    data = b'{"uid": "27"}'

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


    def __init__(self, apiObject = None):

        if apiObject is None:
            print('请传参数')
            return 'error'

        self.apiObject = apiObject
        self.method = apiObject.method
        self.url = apiObject.url
        self.data = apiObject.data
        self.thread_num = apiObject.thread_num
        self.one_work_num = apiObject.one_work_num
        self.loop_sleep = apiObject.loop_sleep
        self.response_time = apiObject.response_time
        self.error = apiObject.error
        self.error_info_list = apiObject.error_info_list


    # 接口函数
    async def thread_api(self):
        global results
        try:
            if self.method == "post":
                results = requests.post(self.url, self.data, self.data)
            if self.method == "get":
                results = requests.get(self.url, self.data)
            return results
        except requests.ConnectionError:
            return results


    # 获取响应时间 单位ms
    async def thread_response(self):
        responsetime = float(await self.thread_api().elapsed.microseconds) / 1000
        return responsetime
    
 
    # 获取平均相应时间 单位ms
    async def thread_response_avg(self):
        avg = 0.000
        l = len(self.response_time)
        for num in self.response_time:
            avg += 1.000 * num / l
        return avg
    

    # 获取当前时间格式
    async def thread_time(self):
        return time.asctime(time.localtime(time.time()))


    # 获取错误的返回状态码
    async def thread_error(self):
        try:

            if self.thread_api().status_code == 200:
                info_result = eval(self.thread_api().text)

                result = await self.apiObject.check_request(info_result)
                if len(result) != 0:
                    self.error_info_list.append(result)
                # 查看返回 code 是否成功
                # if info_result['code'] != 200:
                #     error_info_list.append('error info')

                # 查看返回值数量是否与 postMan 一致 - check_request 接口测试
                # if info_result['count'] != 5:
                #     error_info_list.append('error info')

                # 查看返回值的接口测试 - general_search 接口测试
                # if info_result['code'] != 200:
                #     error_info_list.append(info_result)
                # else:
                #     if len(info_result['data']) != 1:
                #         error_info_list.append('error info 1')
                # return {'code': 201, 'message': '添加搜索日志失败'}
            else:
                self.error.append(self.thread_api().status_code)

        except AttributeError:
            self.error.append("连接失败")


    # 工作线程循环
    async def thread_work(self):
        threadname = await threading.currentThread().getName()
        print ("[", threadname, "] Sub Thread Begin")
        for i in range(self.one_work_num):
            await self.thread_api()
            print ("接口请求时间： ", await self.thread_time())
            self.response_time.append(await self.thread_response())
            await self.thread_error()
            # sleep(loop_sleep)
        print ("[", threadname, "] Sub Thread End")
    

    async def thread_main(self):
        start = time.time()
        threads = []

        # 启动所有线程
        for i in range(self.thread_num):
            t = await threading.Thread(target=await self.thread_work())
            t.setDaemon(True)
            threads.append(t)
        for t in threads:
            t.start()

        # 主线程中等待所有子线程退出
        for t in threads:
            t.join()

        end = time.time()

        print ("========================================================================")
        print ("接口性能测试开始时间：", time.asctime(time.localtime(start)))
        print ("接口性能测试结束时间：", time.asctime(time.localtime(end)))
        print ("接口地址：", self.url)
        print ("接口类型：", self.method)
        print ("线程数：", self.thread_num)
        print ("每个线程循环次数：", self.one_work_num)
        print ("每次请求时间间隔：", self.loop_sleep)
        print ("总请求数：", self.thread_num * self.one_work_num)
        print ("错误请求数：", len(self.error))
        print ("返回的接口信息错误数", len(self.error_info_list))
        print ("总耗时（秒）：", end - start)
        print ("每次请求耗时（秒）：", (end - start) / (self.thread_num * self.one_work_num))
        print ("每秒承载请求数（TPS)：", (self.thread_num * self.one_work_num) / (end - start))
        print ("平均响应时间（毫秒）：", await self.thread_response_avg())
        print ("打印错误列表", self.error_info_list)

