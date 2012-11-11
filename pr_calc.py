from collections import defaultdict




def preprocess(fname):
	fin=open(fname)
	v,ajl=set(),defaultdict(set)
	for line in fin.readlines(): 
		if len(line.split())<2:continue
		[x,y]=line.split('\t')
		v.add(x),v.add(y)
		ajl[x].add(y)
	v,j,najl,num=list(v),0,defaultdict(set),{}
	for i in v: 
		num[i]=j
		j+=1
	for i in ajl:
		for j in ajl[i]: najl[num[i]].add(num[j])
	return v,najl


def calc(v,ajl,iter=100):
	n=len(v)
	pr=[100 for i in range(n)]
	while iter>=0:
		for i in range(n):
			for j in ajl[i]:
				tmp=len(ajl[i])*1.0
				pr[j]=pr[j]+pr[i]/tmp
		for i in range(n):
			pr[i]=0.15/n+0.85*pr[i]
		iter-=1
	#print n,len(ajl)
	for i in range(n):
		print pr[i], v[i]
		#if v[i]=="http://www.nju.edu.cn":print pr[i]
		#if v[i]=="http://cs.nju.edu.cn":print pr[i]
	


v,ajl=preprocess("data")
calc(v,ajl)

