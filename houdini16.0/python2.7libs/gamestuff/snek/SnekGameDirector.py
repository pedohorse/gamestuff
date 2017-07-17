import random

from gamestuff.Component import Component
from SnekFoodComponent import SnekFoodComponent
from gamestuff import gameobject

import math
from hou import Vector2
import hou

class SnekGameDirector(Component):
	__instanced=False
	def __init__(self,gobj):
		if(SnekGameDirector.__instanced):raise Exception("SnekGameDirector is already in the game")
		SnekGameDirector.__instanced=True
		super(SnekGameDirector,self).__init__(gobj)
		self.__lastfoodspawntime=0
		self.__gameover=False
		self.__scoreobject=None
		self.__deathtimer=0
	
	def isGameOver(self):
		return self.__gameover
	
	def onStart(self):
		#scan field for exsisting nodes
		exnodes=[x for x in hou.node("/obj").children() if abs(x.position().x())<10 and abs(x.position().y())<10]
		for node in exnodes:
			exfood=gameobject.GameObject("exfood")
			exfood.position=node.position()
			exfood.addComponent("ExistingNodeShapeComponent").assignHouNode(node)
			exfood.addComponent("SnekFoodComponent")
			exfood.addComponent("BoundingBoxComponent").readjust("","")
	
		#create head
		go=gameobject.GameObject("head")
		shp=go.addComponent("ShapeComponent")
		shp.setBaseShape("snek_head")
		shp.setColor((0.2,0.5,0.15))
		
		go.addComponent("TrailComponent")
		chead=go.addComponent("SnekHeadComponent")
		
		go.addComponent("BoundingBoxComponent").offsetBbox(0.175)
		go.addComponent("ActiveCollisionCheckerComponent")

		#create start body
		gp=go
		startlength=5
		for i in range(startlength):
			gb=gameobject.GameObject("tail")
			shp=gb.addComponent("ShapeComponent")
			shp.setColor((0.2,0.5,0.15))
			if(i==startlength-1):shp.setBaseShape("snek_tail")
			else:shp.setBaseShape("snek_torso")

			gb.addComponent("TrailComponent")
			stc=gb.addComponent("SnekTailComponent")
			stc.setHead(gp)
			stc.setTailOffset(0.5)
			
			gb.addComponent("BoundingBoxComponent")
			#gb.addComponent("DebugBboxComponent")
			
			chead.addControllableTailObjects([gb])
			
			gp=gb
			
		#create score
		self.__scoreobject=gameobject.GameObject("SCORE")
		self.__scoreobject.addComponent("ScoreComponent")
		self.__scoreobject.position=Vector2(11,9.5)
		
	
	def spawnFood(self,pos):
		food=gameobject.GameObject("food")
		food.position=pos
		food.addComponent("ShapeComponent").setBaseShape("snek_food")
		
		food.addComponent("SnekFoodComponent")
		
		food.addComponent("BoundingBoxComponent")
		
		food.addComponent("MoveSpinComponent").setVel(Vector2(),450)
		
	
	
	def update(self):
		if(self.__gameover):
			self.__deathtimer+=self.time.deltaTime()
			self.__scoreobject.position=Vector2(7*math.sin(self.__deathtimer*2),0)
			return
		timepassed=self.time.time()-self.__lastfoodspawntime
		
		if(SnekFoodComponent.totalFoodCount()==0 or random.random()<timepassed*0.001):
			self.spawnFood(Vector2(9.0*2*(random.random()-0.5),9.0*2*(random.random()-0.5)))
			self.__lastfoodspawntime=self.time.time()
	
	def onDestroy(self):
		SnekGameDirector.__instanced=False
	
	def snekAte(self):
		self.__scoreobject.getComponent("ScoreComponent").addScore(1)
		pass
		
	def snekDied(self):
		print("GAME OVER")
		self.__gameover=True