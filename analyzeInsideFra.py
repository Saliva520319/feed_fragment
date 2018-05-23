#! /usr/bin/python2.7

class DataAnalyze():

#    def __init(self):
 
    
    def getData(self):
        filename='/home/work/yaojun/survey/services.20180424.OPERA.quzao'
        #filename='/home/work/yaojun/survey/test.data'
        f = open(filename)
        lines = f.readlines()
        startnum = len(lines)
        efficientnum = 0
        efficientdata = {}
        for i in lines:
            datatmp = i.replace('\n','')
            data = datatmp.split(',') 
            if len(data) == 8:
                efficientnum = efficientnum + 1
                efficientdata[data[0]] = data
	#print startnum,efficientnum
        #print efficientdata
        return efficientdata
                
                
               
    def usedRateAverage(self,datas,usedIndex,quotaIndex,insnumIndex):
        usedSum = 0
        quotaSum = 0
        num = 0
        for i in datas:
            item = datas[i]
            if float(item[usedIndex]) < 200 and float(item[usedIndex]) > 0 :
                num = num + 1 
                usedSum = usedSum + float(item[usedIndex]) * float(item[quotaIndex]) * float(item[insnumIndex]) 
                quotaSum = quotaSum + float(item[quotaIndex]) * float(item[insnumIndex])
        avg = usedSum/quotaSum
        return avg,num
            
    
    def insideFragement(self,datas,usedIndex,quotaIndex,insnumIndex,usedRateAvg):
        greaterFragementSum = 0
        smallerFragementSum = 0
        smallerFragementNum = 0
        greaterFragementNum = 0
        quotasum = 0

        for i in datas:
            item = datas[i]
            #print "-------",item
            usedRes = float(item[usedIndex])
            if usedRes < 200 and usedRes > 0 :
                quotasum = quotasum + float(item[quotaIndex]) * float(item[insnumIndex])
                if usedRes > usedRateAvg :
                    greaterFragementNum = greaterFragementNum + 1
                    FragementRes = (usedRes - usedRateAvg) * float(item[quotaIndex]) * float(item[insnumIndex])
                    greaterFragementSum = greaterFragementSum + FragementRes 
                    #print "---+++",FragementRes
                    #print "+++",greaterFragementSum
                else:
                    smallerFragementNum = smallerFragementNum + 1
                    FragementRes = (usedRateAvg - usedRes) * float(item[quotaIndex]) * float(item[insnumIndex])
                    smallerFragementSum = smallerFragementSum + FragementRes
                    #print "---+++",FragementRes
                    #print "---",smallerFragementSum
        smallerInsideFragementRate = smallerFragementSum/quotasum
        greaterInsideFragementRate = greaterFragementSum/quotasum

        
        return "smallerInsideFragementRate,smallerFragementSum,smallerFragementNum,greaterInsideFragementRate,greaterFragementSum,greaterFragementNum",smallerInsideFragementRate,smallerFragementSum,smallerFragementNum,greaterInsideFragementRate,greaterFragementSum,greaterFragementNum 
                

#    def insideFragementResource():

if __name__ == '__main__':
    da = DataAnalyze()
    res = da.getData()

    print "================cpu===================="
    cpuRateRes = da.usedRateAverage(res,5,3,2)
    cpuRateavg = cpuRateRes[0]
    print "cpuRateavg:",cpuRateavg
    insideFra =  da.insideFragement(res,5,3,2,cpuRateavg)
    print insideFra

    print "================mem===================="
    memRateRes = da.usedRateAverage(res,7,6,2)
    memRateavg = memRateRes[0]
    print "memRateavg:",memRateavg
    insideFra =  da.insideFragement(res,7,6,2,memRateavg)
    print insideFra
