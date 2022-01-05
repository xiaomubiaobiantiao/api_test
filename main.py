'''
@Description:
@Author: michael
@Date: 2021-08-31 10:00:00
LastEditTime: 2021-08-31 20:00:00
LastEditors: michael
'''

from CreateThread import CreateThread
from ApiPressure import ApiPressure

if __name__ == '__main__':

    # for i in range(1):
    # print(f' fro {i} -----------------------')
    apiPressure = ApiPressure()
    apiPressure.check_request_config()
    createThread = CreateThread(apiPressure)
    createThread.thread_main()




