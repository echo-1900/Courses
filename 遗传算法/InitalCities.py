# coding: utf-8

from math import sqrt

def loadCity():
	cityList =[]
	with open("data.txt","r") as f:
		for line in f.readlines():
			cityList.append(line.rstrip().split(","))
	return cityList


def calcDist(life):
	'''传入life对象，返回距离'''
	dist = 0
	for i in range(-1,len(life.gene)-1):
		x1 = float(cityList[life.gene[i]][1])
		x2 = float(cityList[life.gene[i+1]][1])
		y1 = float(cityList[life.gene[i]][2])
		y2 = float(cityList[life.gene[i+1]][2])
		dist += sqrt(pow(x1-x2,2)+pow(y1-y2,2))
	return dist

cityList = loadCity()
#二维数组[["city1_name","经度","维度"],]