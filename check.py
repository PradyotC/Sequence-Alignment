import sys
from efficient import SeqAlignEff

class SeqAlignDyn:

    dlt = 30
    alp = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
    amap = ['A','C','G','T']
    algnArr = []
    str1,str2,m,n = None, None, None, None
    alignments1 = []
    alignments2 = []
    
    def __init__(self,inFile):
        inp = self.readFile(inFile)
        dataList = self.genStrings(inp)
        self.fillData(dataList)
        self.getAlignments()
        
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

    def getAlignments(self):
        perlist = [['a','b','c'],['a','c','b'],['b','a','c'],['b','c','a'],['c','a','b'],['c','b','a']]
        d1 = {'a':0,'b':0,'c':0}
        for i in perlist:
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
                    d1['a'] = self.alpha(self.str1[m-1],self.str2[n-1]) + self.algnArr[m-1][n-1]
                    d1['b'] = self.dlt + self.algnArr[m][n-1]
                    d1['c'] = self.dlt + self.algnArr[m-1][n]
                    mVal = min(d1['a'], d1['b'], d1['c'])
                    for j in i:
                        bool1 = False
                        if mVal == d1['a'] and j == 'a':
                            rstr1 += self.str1[m-1]
                            rstr2 += self.str2[n-1]
                            m -= 1
                            n -= 1
                            bool1 = True
                        elif mVal == d1['b'] and j == 'b':
                            rstr1 += '_'
                            rstr2 += self.str2[n-1]
                            n-=1
                            bool1 = True
                        elif mVal == d1['c'] and j == 'c':
                            rstr1 += self.str1[m-1]
                            rstr2 += '_'
                            m-= 1
                            bool1 = True
                        if bool1:
                            break
            self.alignments1.append(rstr1[::-1])
            self.alignments2.append(rstr2[::-1])                     

filelist = []
outfilelist = []
for i in range(1,6):
    filelist.append('./SampleTestCases/input'+str(i)+'.txt')
    outfilelist.append('./SampleTestCases/output'+str(i)+'.txt')
for i in range(1,16):
    filelist.append('./datapoints/in'+str(i)+'.txt')
for i in range(len(outfilelist)):
    k = filelist[i]
    a=SeqAlignDyn(k)
    c = open(outfilelist[i]).readlines()
    if c[1].rstrip('\n') in a.alignments1 and c[2].rstrip('\n') in a.alignments2:
        b=SeqAlignEff(k)
        print(k,b.s1 in a.alignments1 and b.s2 in a.alignments2)
while i<len(filelist):
    k = filelist[i]
    a=SeqAlignDyn(k)
    b=SeqAlignEff(k)
    print(k,b.s1 in a.alignments1 and b.s2 in a.alignments2)
    i+=1