#! /usr/bin/env python
# _*_ coding:utf-8 _*_


################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Fetch instance data(CPU) base on BNS.

Authors: chufengze(chufengze@baidu.com)
Date:    2018年5月22日 15:07
"""


import codecs
import fire
import os
import subprocess

from datetime import datetime
from datetime import timedelta
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool






class Argus(object):


    def __init__(self, cycle=7, _start_from="200000", _end_to="230000"):
        self._app_list = []
        self._timeFormat = "%Y%m%d%H%M%S"
        self._cycle = int(cycle) 
        self._today =  datetime.now().strftime(self._timeFormat)[:8]
        self._last_cycle_day = (datetime.now() - timedelta(days=self._cycle)).strftime(self._timeFormat)[:8]
        # TODO: Need to be flexible$chufengze$2018年5月23日$
        self._start_from = _start_from
        self._end_to = _end_to

    def fetch_data(self, service_name, *args, **kwargs):
        pass
        print("Yes")

    def _execute(self, cmd):
        try:
            pipe = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
            stdout, stderr = pipe.communicate()
            if not stderr:
                return filter(lambda x: x, stdout.split("\n"))
        except Exception as e:
            print str(e)
            return []
    def _parse_data(self, data_list):
        """
        Return a list, which contains item metrics.
        """
        if len(data_list) < 2:
            pass
        else:
            result = map(lambda x: float(x.split().split("(")[0]), data_list[1:])
        return result
    def _thread_run(self, func, sequence):
        # NOTE: Hard code thread number.
        thread_num=100
        pool = ThreadPool(thread_num)
        results = pool.map(func, sequence)
        return results
    # TODO: customize BNS module $chufengze$2018年4月1
    def get_service_by_path(self, path):
        return self._execute("get_services_by_path {}".format(path))

    # TODO: customize single monquery module$chufengze$2018年4月1
    def get_average_by_service(self, service_name):
        interval=600
        item = "CPU_USED_PERCENT.MATRIX"
        #cycle=7
        time_from = "20180522200000"
        time_to = "20180522230000"
        if not item.endswith(".MATRIX"):
            print("Only usful if the monitorng item ends with .MATRIX.")
            return []
        cmd_template = "monquery -n {} -i {} -t instance -d {} -s {} -e {}"
        raw_data = self._execute(cmd_template.format(service_name, item, interval, time_from, time_to))
        if len(raw_data) < 2:
            print(service_name)
        else:
            pass
        parsed_data = map(lambda x: float(x.split()[-1]), raw_data[1:])
        return sum(parsed_data) / len(parsed_data)
    def get_service_quota(self, service_name, item, ):
        pass
    
    def run(self, echo=True, out_file="./output_list"):

        

        # NOTE: Hard code service name
        app_list = self.get_service_by_path("BAIDU_PS_SUPERPAGE_FEED_sofacloud")
        
        for item in app_list:
            try:
            #    cpu_avg = self.get_average_by_service(item)
                print(item)
                self._execute("monquery -n {} -i CPU_USED_PERCENT.MATRIX -t instance -d 600 -s 20180522200000 -e 20180522230000".format(item))
            #mem_avg = self._thread_run(mem_func, app_list)
            except Exception as error:
                print(str(error))
        #
        """
        if echo:
            print("*" * 30)
            print(cpu_avg)
            #print("*" * 30)
            #print(mem_avg)
        else:
            pass
        
        if not os.path.exists(out_file):
            with codecs.open(out_file, mode="w+", encoding="utf-8") as doc:
                doc.write("\n".join(results))
        else:
            print("File [{}] already exist, try customize your output file.(Using option '--out_file=filename')".format(out_file))
        """

if __name__ == "__main__":
    argus = Argus()
    fire.Fire(argus)