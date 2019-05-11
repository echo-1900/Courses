# coding: utf-8

from GA import GA 

def calc_score(life):
	return sum(life.gene[0:5])

# 测试initalGroup方法
# 成功
# def testInitial():
# 	testInital = GA(calcScore=calc_score)
# 	testInital.initalGroup()
# 	print (len(testInital.lives))
# 	print (testInital.lives[0].gene)
# 	print (testInital.lives[1].gene)
# 	print (testInital.lives[2].gene)
# testInitial()


# 测试prepare方法
# 成功
# def testPrepare():
# 	testPrepare = GA(calcScore=calc_score,startIndex=3)
# 	testPrepare.initalGroup()
# 	testPrepare.prepare()
# 	print (testPrepare.lives)
# 	print (testPrepare.best.gene)
# 	print (testPrepare.best.score)
# testPrepare()


#测试choose和prepare方法
#成功
# def testChoose():
# 	testChoose = GA(calcScore=calc_score)
# 	testChoose.initalGroup()
# 	testChoose.prepare()
# 	ret = testChoose.choose()
# 	print(testChoose.best.score)
# 	print(testChoose.best.gene)
# 	print (ret.score)
# 	print(ret.gene)
# testChoose()


#测试cross方法
#成功
# def testCross():
# 	testCross = GA(calcScore=calc_score)
# 	testCross.initalGroup()
# 	print (testCross.lives[0].gene)
# 	print (testCross.lives[1].gene)
# 	ret = testCross.cross(testCross.lives[0],testCross.lives[1])
# 	print (ret)
# testCross()


#测试mutation方法
# 成功
# def testMutation():
# 	testMutation = GA(calcScore=calc_score)
# 	testMutation.initalGroup()
# 	print (testMutation.lives[0].gene)
# 	print (testMutation.mutation(testMutation.lives[0].gene))
# testMutation()

#测试breed方法
# 成功
# def testBreed():
# 	testBreed = GA(calcScore=calc_score)
# 	testBreed.initalGroup()
# 	testBreed.prepare()
# 	test = testBreed.breedChild()
# 	print (test.gene)
# testBreed()

#测试evolve方法
# 成功
# def testEvolve():
# 	testEvolve = GA(calcScore=calc_score)
# 	testEvolve.initalGroup()
# 	for i in range(100):
# 		testEvolve.evolve()
# 		print (testEvolve.best.score)
# testEvolve()
