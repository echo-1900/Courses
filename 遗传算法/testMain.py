# coding: utf-8

from GA import GA
from InitalCities import calcDist,cityList

#不传入城市列表时默认经过所有城市
ga = GA(calcScore=lambda life: 1.0 /calcDist(life))
#传入城市列表时只经过指定城市
#ga = GA(city_list=[i for i in range(20)],calcScore=lambda life: 1.0 /calcDist(life))
ga.initalGroup()

def testMain():
	best = 500
	for i in range(500):
		ga.evolve()
		if 1.0/ga.best.score<best:
			best = 1.0/ga.best.score
			print (str(i) + ": " + str(best))
	for gene in ga.best.gene:
		print (cityList[gene][0] + "->",end="")

testMain()