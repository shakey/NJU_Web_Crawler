from collections import defaultdict




def preprocess(fname):
	fin=open(fname).readlines()
	v,ajl=set(),defaultdict(set)
	for line in fin: 
		if len(line.split('\t'))<2:continue
		[y,x]=line.split('\t')
		if x=='' or y=='':continue
		v.add(x.strip())
		v.add(y.strip())
	v,j,num=list(v),0,{}
	for i in v: 
		num[i]=j
		j+=1
	for line in fin: 
		if len(line.split('\t'))<2:continue
		[y,x]=line.split('\t')
		if x=='' or y=='':continue
		ajl[num[x.strip()]].add(num[y.strip()])
	return v,ajl


def calc(v,ajl,iter=100):
	n=len(v)
	pr=[1.0 for i in range(n)]
	while iter>=0:
		tmp=[pr[i] for i in range(n)]
		for i in range(n):
			for j in ajl[i]:
				tmp[j]=pr[j]+pr[i]/(len(ajl[i])*1.0)
		for i in range(n):
			pr[i]=0.15/n+0.85*tmp[i]
		iter-=1
	#print v
	for i in range(n):
		if pr[i]<=10.0**(-4):continue
		print pr[i], v[i]
		#if v[i]=="http://www.nju.edu.cn":print pr[i]
		#if v[i]=="http://cs.nju.edu.cn":print pr[i]
	


[v,ajl]=preprocess("data")
calc(v,ajl)

