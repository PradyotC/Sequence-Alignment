import sys
import time
import psutil

class SeqAlignEff:
	dlt = 30
	alp = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
	amap = ['A','C','G','T']
	val,s1,s2 = None,None,None

	def __init__(self,filename):
		str1, str2 = self.genStrings(self.readFile(filename))
		self.val,self.s1,self.s2 = self.alignEff(str1,str2)

	def alignEff(self,str1,str2):
		m,n = len(str1),len(str2)
		if m>1 and n>1:
			midm = m//2
			r1 = self.fillData(str1[:midm],str2)
			r2 = self.fillData(str1[midm:][::-1],str2[::-1])[::-1]
			min1 = float('inf')
			midn = -1
			for i in range(n+1):
				if min1 > r1[i]+r2[i]:
					min1,midn = r1[i]+r2[i],i
			s11,s12 = str1[:midm],str1[midm:]
			s21,s22 = str2[:midn],str2[midn:]
			val1,rstr11,rstr21=self.alignEff(s11,s21)
			val2,rstr12,rstr22=self.alignEff(s12,s22)
			return val1+val2,rstr11+rstr12,rstr21+rstr22
		else:
			return self.getAlignDyn(str1,str2)

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

	def fillDataDyn(self,str1,str2):
		m, n = len(str1)+1, len(str2)+1
		algnArr = [[0 for _ in range(n)] for _ in range(m)]
		for i in range(m):
			for j in range(n):
				if i == 0:
					algnArr[i][j] = j*self.dlt
				elif j == 0:
					algnArr[i][j] = i*self.dlt
				else:
					c1,c2 = str1[i-1],str2[j-1]
					algnArr[i][j] = min(self.alpha(c1,c2)+algnArr[i-1][j-1], self.dlt+algnArr[i][j-1], self.dlt+algnArr[i-1][j])
		return algnArr

	def getAlignDyn(self,str1,str2):
		algnArr = self.fillDataDyn(str1,str2)
		rstr1,rstr2 = '',''
		m,n = len(str1),len(str2)
		while True:
			if m ==0 and n == 0:
				break
			elif m == 0:
				rstr1 += '_'
				rstr2 += str2[n-1]
				n -= 1
			elif n == 0:
				rstr1 += str1[m-1]
				rstr2 += '_'
				m -= 1
			else:
				a = self.alpha(str1[m-1],str2[n-1]) + algnArr[m-1][n-1]
				b = self.dlt + algnArr[m][n-1]
				c = self.dlt + algnArr[m-1][n]
				mVal = min(a, b, c)
				if mVal == a:
					rstr1 += str1[m-1]
					rstr2 += str2[n-1]
					m -= 1
					n -= 1
				elif mVal == b:
					rstr1 += '_'
					rstr2 += str2[n-1]
					n-=1
				elif mVal == c:
					rstr1 += str1[m-1]
					rstr2 += '_'
					m-= 1
		return algnArr[-1][-1],rstr1[::-1], rstr2[::-1]

	def fillData(self,str1,str2):
		str1, str2 = 'A'+ str1,'A'+ str2
		m, n = len(str1), len(str2)
		algnArr = [[0,self.dlt*i] for i in range(n)]
		for j in range(1,m):
			for i in range(n):
				algnArr[i] = [algnArr[i][1],0]
			algnArr[0][1] = self.dlt*j
			for i in range(1,n):
				c1,c2 = str1[j],str2[i]
				val = min(self.alpha(c1,c2)+algnArr[i-1][0], self.dlt+algnArr[i-1][1], self.dlt+algnArr[i][0])
				algnArr[i][1] = val
		return [i[1] for i in algnArr]

if __name__ == "__main__":
	process = psutil.Process()
	start_time = time.time()
	a = SeqAlignEff(str(sys.argv[1]))
	end_time = time.time()
	time_taken = (end_time - start_time)*1000
	memory_info = process.memory_info()
	memory_consumed = int(memory_info.rss/1024)
	filename = open(str(sys.argv[2]), "w+")
	filename.write(str(a.val)+'\n')
	filename.write(a.s1+'\n')
	filename.write(a.s2+'\n')
	filename.write(str(time_taken)+'\n')
	filename.write(str(memory_consumed))