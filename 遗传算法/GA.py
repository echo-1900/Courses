# coding:utf-8

import random,copy
from Life import Life

#random.randint(i,j)  -> [i,j] ->上下界都包含


class GA(object):
	def __init__(self,calcScore,city_list=[],startIndex=0,groupsize=100,crossrate=0.8,mutationrate=0.1):
		self.groupsize = groupsize
		self.lifelen   = len(city_list)
		self.calcScore = calcScore
		self.crossrate = crossrate
		self.mutationrate = mutationrate
		self.lives = []   #当前种群中所有个体
		self.best  = None #历史最优个体
		self.all_score = 0#种群总得分
		self.city_list = city_list #所有要经过的城市的下标组成的数组
		self.startIndex =startIndex #出发城市下标

	#m当不传入城市列表时默认遍历所有城市
	def initalGroup(self):
		if len(self.city_list)==0:
			self.lifelen = 34
			tmp = [i for i in range(self.lifelen) if i!=self.startIndex] #确保起始城市在第一个
			for i in range(self.groupsize):
				random.shuffle(tmp)
				ret = [self.startIndex]+tmp #确保起始城市不变
				self.lives.append(Life(copy.copy(ret))) #!用copy
		else:
			tmp=self.city_list[1:]#确保起始城市在第一个
			for i in range(self.groupsize):
				random.shuffle(tmp)
				ret = [self.city_list[0]]+tmp #确保起始城市不变
				self.lives.append(Life(copy.copy(ret))) #!用copy


	def prepare(self):
		#进化前的准备工作，选出最优个体，计算种群总得分
		self.all_score=0 #每次进化后归零
		self.best = self.lives[0]
		for i in self.lives:
			i.score = self.calcScore(i)
			self.all_score += i.score
			if i.score > self.best.score:
				self.best = i
			

	def choose(self):
		'''轮盘赌，返回一个选出来的Life对象'''
		randNum = random.uniform(0,self.all_score)
		# print self.all_score
		# print randNum
		for i in self.lives:
			randNum -= i.score
			if randNum <= 0:
				return i

	def cross(self,parent1,parent2):
		'''传入Life对象，返回基因列表'''
		#从1开始，起始城市不能变

		start = random.randint(1,self.lifelen-2) 
		end	  = random.randint(start+1,self.lifelen)
		ret = []
		tmp = parent2.gene[start:end]
		# print parent1
		# print parent2
		# print start
		# print end
		# print tmp

		for i in parent1.gene:
			if parent1.gene.index(i)==start:
				ret.extend(tmp)
			if i not in tmp:
				ret.append(i)
		return ret

	def mutation(self,alife):
		'''传入list，返回基因列表'''
		#从1开始，起始城市不变
		ret = alife
		index1 = random.randint(1,self.lifelen-1)
		index2 = random.randint(1,self.lifelen-1)
		ret[index1],ret[index2] = ret[index2],ret[index1]
		return ret


	def breedChild(self):
		'''局部变量ret为list类型'''
		father = self.choose()
		ret = father.gene[:] #一定要重新复制，不能指向原对象，否则万一choose到之前的best则会把best也变了（生孩子的时候母亲难产死亡）
		#交叉
		if random.random() < self.crossrate:
			mother = self.choose()
			ret = self.cross(father,mother)
			# print father.gene
			# print mother.gene
			# print ret
		#变异
		if random.random() < self.mutationrate:
			ret = self.mutation(ret)
		return Life(ret)

	def evolve(self):
		'''更新种群'''
		self.prepare()

		#优化方案，将当前种群排名前10%的个体全部选择
		self.lives.sort(key=lambda life:life.score,reverse=True)
		tmp = []
		tmp.extend(self.lives[0:self.groupsize//20])
		while(len(tmp)<self.groupsize):
			tmp.append(self.breedChild())
		self.lives = tmp

		# 原始方案，只强制选择历史最优个体
		# tmp = []
		# tmp.append(self.best)#最优个体必被选择
		# for i in range(self.groupsize-1):
		# 	tmp.append(self.breedChild())
		# self.lives = tmp


