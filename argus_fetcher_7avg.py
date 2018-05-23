#! /usr/bin/python2.7
"""
@brief: ArgusFetcher7Avg
@author: gaochuansong
"""
import commands
from datetime import datetime
from datetime import timedelta
from argus_fetcher import ArgusFetcher

class ArgusFetcher7Avg(ArgusFetcher):
    """
    fetch service data as avg of 7 days
    """
    def __init__(self):
        timeFormat = '%Y%m%d%H%M%S'
        timeAcross = 7
        end = datetime.now()
        start = end - timedelta(days = timeAcross)
        self.end = end.strftime(timeFormat)
        self.start = start.strftime(timeFormat)

    def parseFloat(self, v):
        """
        parse argus value
        """
        tmp = v.strip()
        if tmp == 'null':
            return -1
        try:
            return float(v)
        except Exception as e:
            return -1

    def get_instance_by_service(self, service):
        """
        invoke get_instance_by_service in host
        """
        (status, output) = commands.getstatusoutput('get_instance_by_service %s -o' % service)
        if status != 0:
            print 'get_instance_by_service %s failed: %s' % (service, output)
            #print "*************"
            return None
        if output == '':
            return (0, -1)
        lines = output.split('\n')
        #print "########"
       	#print lines
        #print "########"
        offset = lines[0].split()[1]
        # static inst num
        data = {}
        for line in lines:
            idc = line.split()[0].split('.')[-1]
            if idc not in data:
                data[idc] = 0
            data[idc] = data[idc] + 1
        return (len(lines), offset, data)

    def fetch_service_quota(self, service, offset):
        """
        cpu: 0.1core
        mem: 1GB
        """
        monqueryItems = 'CPU_QUOTA.MATRIX,MEM_QUOTA.MATRIX'
        cmd = 'monquery -n %s.%s -i %s' % (offset, service, monqueryItems)
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            return None
        lines = output.split('\n')
        if len(lines) != 2:
            return None
        values = lines[1].split()
        if '(' not in values[1] or '(' not in values[2]:
            return None
        cpustr = values[1].split('(')[0]
        memstr = values[2].split('(')[0]
        cpu = self.parseFloat(cpustr)
        mem = self.parseFloat(memstr)
        #print "####cpu,mem quota:" + str(cpu) +" , " + str(mem)
        if -1 == cpu or -1 == mem:
            return None
        return (cpu, mem / 1024000)

    def fetch_service_used(self, service):
        """
        cpu: 0.1core
        mem: 1GB
        """
        inter = 600
        monqueryItems = 'CPU_USED_PERCENT.MATRIX_avg'
        #monqueryItems = 'CPU_USED_PERCENT.MATRIX_avg,MEM_USED_PERCENT.MATRIX_avg'
        timeFormat = '%Y%m%d'
        timeAcross = 7
        end = datetime.now()
        start = end - timedelta(days = timeAcross)
        endday = end.strftime(timeFormat)
        startday = start.strftime(timeFormat)
        cpu_avg_list = []
        for i in range(int(startday),int(endday)):
                starttime = str(i) + '080000'
                endtime = str(i) + '110000'
                cmd = 'monquery -i %s -n %s -d %s -s %s -e %s -f max'\
                    % (monqueryItems, service, inter,  starttime, endtime)
	        print cmd
                (status, output) = commands.getstatusoutput(cmd)
                if status != 0:
                    #print "############## failed used:" + str(i)
                    return None 
                #print "####used :" + output
                cpu_avgs = output.split('\n')
                if len(cpu_avgs) <= 1:
                    #print "############## failed used 2:" + str(i)
                    return None
                for index in range(1, len(cpu_avgs)):
                    values = cpu_avgs[index].split()
                    if len(values) != 3:
                        return None
                    tmpcpu = self.parseFloat(values[2])
                    if tmpcpu == -1:
                        return None
                    cpu_avg_list.append(tmpcpu)
        cpu_avg_list.sort()
        #print "#########after sort :" + str(cpu_avg_list)
        #n = int(timeAcross * 3 * 3600 * 0.99/inter)
        cpu_used_max = 0
        if len(cpu_avg_list) > 0 :
            m = int(len(cpu_avg_list) * 0.99)
            cpu_used_max = cpu_avg_list[m]
        #print n,cpu_used_max

        monqueryItems = 'CPU_USED_PERCENT.MATRIX_avg,MEM_USED_PERCENT.MATRIX_avg'
        #monqueryItems = 'MEM_USED_PERCENT.MATRIX_avg'
        cmd = 'monquery -i %s -n %s -d 86400 -s %s -e %s -f max'\
                % (monqueryItems, service, self.start, self.end)
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
         #   print "############## failed used"
            return None 
        #print "####used :" + output
        peakPerDays = output.split('\n')
        if len(peakPerDays) <= 1:
            return None
        cpu_list = []
        mem_list = []
        for index in range(1, len(peakPerDays)):
            values = peakPerDays[index].split()
            if len(values) != 4:
                return None
            tmpcpu = self.parseFloat(values[2])
            tmpmem = self.parseFloat(values[3])
            if tmpcpu == -1:
                return None
            if tmpmem == -1:
                return None
            cpu_list.append(tmpcpu)
            mem_list.append(tmpmem)
        cpu_list.sort()
        mem_list.sort()
        #print "#######************used: " + str(mem_list)
        #return (cpu_list[len(cpu_list) / 2], \
        #        mem_list[len(mem_list)/ 2] / 1024000.0)
        return (cpu_list[len(cpu_list) / 2], \
                mem_list[len(mem_list)/ 2], \
                cpu_used_max)

    def fetch_service_data(self, service):
        """
        fill service data
        """
        #print "--------------start get ndeninstance"
        inst_num_tuple = self.get_instance_by_service(service)
        if inst_num_tuple is None or inst_num_tuple[0] <= 0:
            return None
        #print "--------------start get quota"
        service_quota_tuple = self.fetch_service_quota(service, inst_num_tuple[1])
        if service_quota_tuple is None:
            return None
        #print "--------------start get used"
        service_used_tuple = self.fetch_service_used(service)
        if service_used_tuple is None:
            return None
        data = {}
        data['service_name'] = service
        data['cpu_quota'] = service_quota_tuple[0]
        data['mem_quota'] = service_quota_tuple[1]
        data['cpu_used_percent'] = round(service_used_tuple[0],2)
        data['cpu_used_percent_max'] = round(service_used_tuple[2],2)
#        print "++++++++++++++++++++" + str(service_quota_tuple[1]) + "," + str(service_used_tuple[1])
        data['mem_used_percent'] = round( service_used_tuple[1],2)
        data['inst_num'] = inst_num_tuple[0]
        data['inst_dist'] = inst_num_tuple[2]
        return data

if __name__ == '__main__':
    af = ArgusFetcher7Avg()

    #filename='/home/work/yaojun/survey/services.20180420.NOVA'
    filename='/home/work/yaojun/survey/services.20180420.OPERA'
    f = open(filename)
    lines = f.readlines()
    for i in lines:
        servicename = i.replace('\n','')
        data =  af.fetch_service_data(servicename)        
        if data is None:
            print servicename
        else: 
            print '%s,%s,%s,%s,%s,%s,%s,%s' %(data['service_name'],data['inst_dist'].keys()[0],data['inst_num'],data['cpu_quota'],data['cpu_used_percent'],data['cpu_used_percent_max'],data['mem_quota'],data['mem_used_percent']) 

    #services = ['ADX-MATRIX.NOVA.gz']
    #data = af.fetch_service_data('ADX-MATRIX.NOVA.gz')
    #print data

#    af = ArgusFetcher7Avg()
#
#    #services= ['ADX-MATRIX.NOVA.gz']
#    #data = af.fetch_service_data('ADX-MATRIX.NOVA.gz')
#    servicename = 'opera-ps-ctrxserver-056-nj.IM.nj02'
#    data = af.fetch_service_data(servicename)
#    if data is None:
#        print servicename
#    else:
#        print '%s,%s,%s,%s,%s,%s,%s,%s' %(data['service_name'],data['inst_dist'].keys()[0],data['inst_num'],data['cpu_quota'],data['cpu_used_percent'],data['cpu_used_percent_max'],data['mem_quota'],data['mem_used_percent']) 

