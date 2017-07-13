from gamestuff.Component import Component
from gamestuff.gameobject import GameObject
from hou import Vector2
import hou
import random

class PlaneGameDirector(Component):

	__instance=None
	def __init__(self,gobj):
		super(PlaneGameDirector,self).__init__(gobj)
		self.__globalVel=Vector2()
		self.__level=None
		self.__timer=0
		self._bulletcache=[]
		self._firepuffcache=[]
		if(PlaneGameDirector.__instance is not None):raise Exception("TOO MANY DIRECTORS!!")
		PlaneGameDirector.__instance=self
		
		self.__clouds=[] #(px,py,sx,sy,depth)
		self.__neds=[]
		
		self.__playerCached=None
	
	def setNeds(self,neds):
		'''
		sets list of network editors to draw shapes onto
		'''
		self.__neds=neds
	
	@classmethod
	def instance(cls):
		return cls.__instance
	
	def onDestroy(self):
		PlaneGameDirector.__instance=None
		for ne in self.__neds:	
			ne.setShapes(())
			
	
	def onStart(self):
		print("trying to load level...")
		levelnode=hou.node("/obj/plane_level_bosstest")
		if(levelnode is None):
			print("level not found")
		else:
			nodes=[x for x in levelnode.children() if x.name().find("plane_")==0]
			nodes.sort(key=lambda x: x.position()[1])
			self.__level=[(x.position(),x) for x in nodes]
			print("level loaded")
			print(self.__level)
		
		self.__globalVel=Vector2(0,-10)
	
		self.createPlayer(Vector2(0,-8))
		
		#for i in range(8):
		#	self.createEnemySimple("plane_evil01",Vector2(-4+i,9),Vector2(0,-4),2,2,i*0.1)
		
	
	def __genCloud(self,xminsize,xmaxsize,yminsize,ymaxsize,mindepth,maxdepth):
		csx=random.uniform(xminsize,xmaxsize)
		csy=random.uniform(yminsize,ymaxsize)
		cx=random.uniform(-9-csx*0.5,9+csx*0.5)
		if(cx+csx*0.5>10):
			cx=0.5*(cx-0.5*csx+10)
			csx=2*(10-cx)
		if(cx-csx*0.5<-10):
			cx=0.5*(cx+0.5*csx-10)
			csx=2*(10+cx)
		cy=10+csy*0.5
		cd=random.uniform(mindepth,maxdepth)
		clr=0.4-(cd-1)/9.0*0.2
		return [cx,cy,csx,csy,cd,clr]
	
	
	def update(self):
		dt=self.time.deltaTime()
		self.__timer+=dt
		if(self.__level is not None):
			while(len(self.__level)>0 and self.__level[0][0][1]<self.__timer*10):
				entry=self.__level.pop(0)
				pos=entry[0]
				node=entry[1]
				#print(node.name())
				if(node.name().find("plane_small")==0):
					self.createEnemySimple("plane_evil01",Vector2(pos[0],9.9),Vector2(node.evalParm("velx"),node.evalParm("vely")),node.evalParm("sinAmp"),node.evalParm("sinFreq"),node.evalParm("sinOffset"),destroyCallback=self.explosion)
				elif(node.name().find("plane_big")==0):
					self.createEnemySimple("plane_evil02",Vector2(pos[0],9.9),Vector2(node.evalParm("velx"),node.evalParm("vely")),node.evalParm("sinAmp"),node.evalParm("sinFreq"),node.evalParm("sinOffset"),node.evalParm("lives"),node.evalParm("shooting"),node.evalParm("shootRowCount"),node.evalParm("projectilesCount"),node.evalParm("spreadHalfangle"),node.evalParm("shootRowDelay"),node.evalParm("shootReloadTime"),node.evalParm("shootAngle"),self.bigExplosion)
				elif(node.name().find("plane_boss_type1")==0):
					self.createBoss(Vector2(pos[0],9.9))
		
		if(len(self.__neds)>0):
			needsort=False
			if(random.random()<0.7*dt):
				self.__clouds.append(self.__genCloud(1,20,1,20,1,10))
				needsort=True
			if(random.random()<0.35*dt):
				self.__clouds.append(self.__genCloud(2,4,2,4.5,1,1.25))
				needsort=True	
			if(needsort):
				self.__clouds.sort(key=lambda x:x[4],reverse=True)
				
			shapelist=[]
			removelist=[]
			for cloud in self.__clouds:
				cloud[0]+=self.__globalVel[0]*dt/cloud[4]
				cloud[1]+=self.__globalVel[1]*dt/cloud[4]
				if(cloud[1]+cloud[3]*0.5 < -10):
					removelist.append(cloud)
				else:
					clr=cloud[5]
					shapelist.append(hou.NetworkShapeBox(hou.BoundingRect(cloud[0]-cloud[2]*0.5,cloud[1]-cloud[3]*0.5,cloud[0]+cloud[2]*0.5,cloud[1]+cloud[3]*0.5),color=hou.Color((clr,clr,clr)),alpha=0.9,screen_space=False))
			for item in removelist:
				self.__clouds.remove(item)
			
			for ne in self.__neds:	
				ne.setShapes(shapelist)
		self.__playerCached=None #to update in case player was killed or shit
		
	#helper functions
	
	def getPlayer(self):
		if(self.__playerCached is None):
			self.__playerCached=GameObject.findObject("PLAYER")
		return self.__playerCached
	
	def getGlobalVel(self):
		return self.__globalVel
	
	def isOutOfGameArea(self,pos):
		return pos[0]<-10 or pos[0]>10 or pos[1]<-10 or pos[1]>11
	
	def createPlayer(self,pos):
		go=GameObject("PLAYER")
		shp=go.addComponent("ShapeComponent")
		shp.setBaseShape("plane_plane")
		#shp.setAnimated(True)
		go.addComponent("PlaneComponent")
		go.addComponent("BoundingBoxComponent").readjust("8_0","8_0")
		go.addComponent("PlanePlayerControl")
		go.position=pos
		return go
		
	def createEnemySimple(self,shape,pos,vel,sinAmp,sinFreq,sinOffset,lives=None,shooting=None,shootRowCount=None,projectilesCount=None,spreadHalfangle=None,shootRowDelay=None,shootReloadTime=None,shootAngle=None,destroyCallback=None,additionalComponents=None):
		go=GameObject("enemy_simple_Plane")
		go.position=pos
		shp=go.addComponent("ShapeComponent")
		shp.setBaseShape(shape)
		#shp.setAnimated(True)
		go.addComponent("PlaneComponent")
		go.addComponent("BoundingBoxComponent").readjust("8_0","8_0")
		cnf=go.addComponent("PlaneEvilSimple")
		cnf.setConfig(vel,sinAmp,sinFreq,sinOffset,lives,shooting,shootRowCount,projectilesCount,spreadHalfangle,shootRowDelay,shootReloadTime,shootAngle,destroyCallback)
		ac=go.addComponent("ActiveCollisionCheckerComponent")
		ac.setCollisionMask("bullet_player")
		
		if(additionalComponents is not None):
			for compname in additionalComponents:
				go.addComponent(compname)
				
		return go
		
	def createBoss(self,pos):
		go=GameObject("enemy_BOSS")
		go.position=pos+Vector2(0,20)
		go.addComponent("BossCoreComponent")
		
		return go
	
	def fireBullet(self,pos,angle,speed,tag,clr=(1,1,0.36)):
		#print(len(self._bulletcache))
		if(len(self._bulletcache)==0):
			go=GameObject("bullet_"+tag)
			go.position=pos*1
			go.angle=angle
			shp=go.addComponent("ShapeComponent")
			shp.setBaseShape("plane_bullet")
			shp.setColor(clr)
			go.addComponent("PlaneBullet").setConfig(speed)
			go.addComponent("BoundingBoxComponent")
		else:
			cp=self._bulletcache.pop()
			cpgo=cp.gameObject()
			cpgo.position=pos
			cpgo.angle=angle
			cpgo.setName("bullet_"+tag)
			cp.shapeShortcut().setColor(clr)
			cp.setConfig(speed)
			cp.setActive(True)
		
		
	def explosion(self,pos,vel=None,**kwargs):
		if(vel is None):vel=Vector2()
		go=GameObject("explosion")
		go.position=pos
		shp=go.addComponent("ShapeComponent")
		shp.setBaseShape("plane_boomMain")
		shp.setAnimated(True)
		shp.setColor((0,0,0))
		go.addComponent("ExplosionComponent").setVel(vel*1)
		return go
	
	def bigExplosion(self,pos,vel=None,time=1.0,**kwargs):
		go=GameObject("bigExplosion")
		go.position=pos
		be=go.addComponent("BigExplosionComponent")
		be.setTimer(time)
		if("jitterShape" in kwargs):
			be.setJitterShape(kwargs["jitterShape"])
		return go
		
	def firePuff(self,pos,angle,vel=None,fwdShift=0,animSpeed=1):
		if(vel is None):vel=Vector2()
		if(len(self._firepuffcache)==0):
			go=GameObject("puff")
			go.angle=angle
			go.position=pos+go.fwd()*fwdShift
			shp=go.addComponent("ShapeComponent")
			shp.setBaseShape("plane_boomWhisp")
			shp.setAnimated(True)
			fpf=go.addComponent("FirePuffComponent")
			fpf.setVel(vel*1)
			fpf.setAnimSpeed(animSpeed)
			return go
		else:
			cp=self._firepuffcache.pop(0)
			cpgo=cp.gameObject()
			cpgo.angle=angle
			cpgo.position=pos+cpgo.fwd()*fwdShift
			cp.setActive(True)
			
			cp.setVel(vel)
			cp.setAnimSpeed(animSpeed)
			return cpgo