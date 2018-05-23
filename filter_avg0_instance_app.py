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

def get_average_by_service(service_name):
        interval=600
        item = "CPU_USED_PERCENT.MATRIX"
        #cycle=7
        time_from = "20180522200000"
        time_to = "20180522230000"
        cmd_template = "monquery -n {} -i {} -t instance -d {} -s {} -e {}"
        raw_data = _execute(cmd_template.format(service_name, item, interval, time_from, time_to))
        parsed_data = map(lambda x: float(x.split()[-1]), raw_data[1:])
        return sum(parsed_data) / len(parsed_data)

def func(app_name):
    try:
        result = get_average_by_service(app_name)
    except Exception:
        raise
    if result <= 0:
        print(app_name)
    else:
        pass
if __name__ == '__main__':
    data = open("./input.txt", "r").read().split("\n")
    app_list = filter(lambda x: x, data)
    #app_name = "ann-rank-suzhou.SUPERPAGE.sz"
    #func(app_name)
    thread_num = 1000
    pool = ThreadPool(thread_num)
    pool.map(func, app_list)
