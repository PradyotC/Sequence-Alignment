import sys
import time
import psutil

class SeqAlignDyn:

    dlt = 30
    alp = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
    amap = ['A','C','G','T']
    algnArr = []
    str1,str2,m,n = None, None, None, None
    rstr1,rstr2 = None, None
    
    def __init__(self,inFile):
        inp = self.readFile(inFile)
        dataList = self.genStrings(inp)
        self.fillData(dataList)
        self.getAlignment()
        
    def readFile(self,filename):
        with open(filename,'r') as f:
            inArr = f.readlines()
        return [i.rstrip('\n') for i in inArr]

    def genStrings(self,inp):    
        strings = []
        str1 = None
        for i in inp:
            if i.isalpha():
                if str1:
                    strings.append(str1)
                str1 = i
            else:
                str1 = str1[:int(i)+1]+str1+str1[int(i)+1:]
        strings.append(str1)
        return strings
            
    def alpha(self,v1,v2):
        return self.alp[self.amap.index(v1)][self.amap.index(v2)]
    
    def fillData(self,dataList):
        self.str1, self.str2 = dataList
        self.m, self.n = len(self.str1), len(self.str2) 
        self.algnArr = [[0 for _ in range(self.n+1)] for _ in range(self.m+1)]
        for i in range(self.m+1):
            for j in range(self.n+1):
                if i == 0:
                    self.algnArr[i][j] = j*self.dlt
                elif j == 0:
                    self.algnArr[i][j] = i*self.dlt
                else:
                    c1,c2 = self.str1[i-1],self.str2[j-1]
                    self.algnArr[i][j] = min(self.alpha(c1,c2)+self.algnArr[i-1][j-1], self.dlt+self.algnArr[i][j-1], self.dlt+self.algnArr[i-1][j])

    def getAlignment(self):
        m,n = self.m,self.n
        rstr1, rstr2 = '',''
        while True:
            if m ==0 and n == 0:
                break
            elif m == 0:
                rstr1 += '_'
                rstr2 += self.str2[n-1]
                n -= 1
            elif n == 0:
                rstr1 += self.str1[m-1]
                rstr2 += '_'
                m -= 1
            else:
                a = self.alpha(self.str1[m-1],self.str2[n-1]) + self.algnArr[m-1][n-1]
                b = self.dlt + self.algnArr[m][n-1]
                c = self.dlt + self.algnArr[m-1][n]
                mVal = min(a, b, c)
                if mVal == a:
                    rstr1 += self.str1[m-1]
                    rstr2 += self.str2[n-1]
                    m -= 1
                    n -= 1
                elif mVal == b:
                    rstr1 += '_'
                    rstr2 += self.str2[n-1]
                    n-=1
                elif mVal == c:
                    rstr1 += self.str1[m-1]
                    rstr2 += '_'
                    m-= 1
        self.rstr1,self.rstr2 = rstr1[::-1], rstr2[::-1]                     

process = psutil.Process()
start_time = time.time()
a=SeqAlignDyn(str(sys.argv[1]))
end_time = time.time()
time_taken = (end_time - start_time)*1000
memory_info = process.memory_info()
memory_consumed = int(memory_info.rss/1024)
filename = open(str(sys.argv[2]), "w+")
filename.write(str(a.algnArr[-1][-1])+'\n')
filename.write(a.rstr1+'\n')
filename.write(a.rstr2+'\n')
print(a.m+a.n)
print(time_taken)
print(memory_consumed)
filename.write(str(time_taken)+'\n')
filename.write(str(memory_consumed))