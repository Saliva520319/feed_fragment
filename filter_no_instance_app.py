#! /usr/bin/env python
# _*_ coding:utf-8 _*_


import subprocess
from multiprocessing.dummy import Pool as ThreadPool

def _execute(cmd):
        try:
            pipe = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = pipe.communicate()
            if not stderr:

                result = filter(lambda x: x, stdout.split("\n"))
                return result
            else:
                return []
        except Exception as e:
            raise

def get_service_by_path(path):
    return _execute("get_services_by_path {}".format(path))


def func(app_name):
    try:
        result = _execute("monquery -n {} -i CPU_USED_PERCENT.MATRIX -t instance -d 600 -s 20180522200000 -e 20180522230000".format(app_name))
    except Exception as error:
        raise
    if len(result):
        print("{}\tYES".format(app_name))
    else:
        print("{}\tNO".format(app_name))
if __name__ == '__main__':
    app_list = get_service_by_path("BAIDU_PS_SUPERPAGE_FEED_sofacloud")
    #app_name = "ann-rank-suzhou.SUPERPAGE.sz"
    #func(app_name)
    thread_num = 10
    pool = ThreadPool(thread_num)
    pool.map(func, app_list)
