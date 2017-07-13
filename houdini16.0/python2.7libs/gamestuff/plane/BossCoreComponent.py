from gamestuff.Component import Component
from gamestuff.gameobject import GameObject
from PlaneGameDirector import PlaneGameDirector

from hou import Vector2

class BossCoreComponent(Component):
	
	def __init__(self,gobj):
		super(BossCoreComponent,self).__init__(gobj)
		self.__parts={}

		
		
		self.__state="goto"
		self.__nextState="stage1"
		self.__targetpos=Vector2((0,15))
	
	def update(self):
		gobj=self.gameObject()
		dt=self.time.deltaTime()
		
		if(self.__state=="goto"):
			d=self.__targetpos-gobj.position
			speed=2
			dl=d.length()
			if(dl<=0.00001):
				self.__state=self.__nextState
				self.__nextState=""
				return
			d=min(dl,speed*dt)*d/dl
			gobj.position+=d
		elif(self.__state=="stage1"):
			#init
			if(self.__nextState==""):
				self.__nextState="stage1_tailremain"
				self.__parts["taill"].sendMessage("setActive",True)
				self.__parts["tailr"].sendMessage("setActive",True)
			#do stuff
			if(self.__parts["taill"] is None and self.__parts["tailr"] is None):
				self.__targetpos=Vector2(0,15)
				self.__state="goto"
				return
		elif(self.__state=="stage1_tailremain"):
			#init
			if(self.__nextState==""):
				self.__nextState="stage2"
				self.__parts["b4"].sendMessage("setActive",True)
			#do stuff
			if(self.__parts["b4"] is None):
				self.__targetpos=Vector2(8,9)
				self.__state="goto"
	
		
	def partDestroyed(self,part):
		for key in self.__parts:
			if(self.__parts[key]==part):
				self.__parts[key]=None
				break
	
	def onStart(self):
		#here we create the boss himself
		gobj=self.gameObject()
		b1=GameObject("enemy_BOSS_HEAD")
		b1.transform.setParent(gobj.transform,False)
		b1.addComponent("ShapeComponent").setBaseShape("big_boss_body1")
		b1.addComponent("BoundingBoxComponent")
		b1.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b1.addComponent("BossPartComponent").setLives(20)
		
		
		b2=GameObject("enemy_BOSS_CENTER")
		b2.transform.setParent(gobj.transform,False)
		b2.addComponent("ShapeComponent").setBaseShape("big_boss_body2")
		b2.addComponent("BoundingBoxComponent")
		b2.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b2.addComponent("BossPartComponent").setLives(20)
		
		
		b3=GameObject("enemy_BOSS_BODY")
		b3.transform.setParent(gobj.transform,False)
		b3.addComponent("ShapeComponent").setBaseShape("big_boss_body3")
		b3.addComponent("BoundingBoxComponent")
		b3.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b3.addComponent("BossPartComponent").setLives(20)
		
		
		b4=GameObject("enemy_BOSS_TAIL")
		b4.transform.setParent(gobj.transform,False)
		b4.addComponent("ShapeComponent").setBaseShape("big_boss_body4")
		b4.addComponent("BoundingBoxComponent")
		b4.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b4.addComponent("BossPartComponent").setLives(20)
		
		
		wl=GameObject("enemy_BOSS_WINDL")
		wl.transform.setParent(gobj.transform,False)
		wl.addComponent("ShapeComponent").setBaseShape("big_boss_wingl")
		wl.addComponent("BoundingBoxComponent")
		wl.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		wl.addComponent("BossPartComponent").setLives(20)
		
		
		wr=GameObject("enemy_BOSS_WINDR")
		wr.transform.setParent(gobj.transform,False)
		wr.addComponent("ShapeComponent").setBaseShape("big_boss_wingr")
		wr.addComponent("BoundingBoxComponent")
		wr.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		wr.addComponent("BossPartComponent").setLives(20)
		
		
		tl=GameObject("enemy_BOSS_TAILL")
		tl.transform.setParent(gobj.transform,False)
		tl.addComponent("ShapeComponent").setBaseShape("big_boss_taill")
		tl.addComponent("BoundingBoxComponent")
		tl.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		tl.addComponent("BossPartComponent").setLives(20)
		
		
		tr=GameObject("enemy_BOSS_TAILR")
		tr.transform.setParent(gobj.transform,False)
		tr.addComponent("ShapeComponent").setBaseShape("big_boss_tailr")
		tr.addComponent("BoundingBoxComponent")
		tr.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		tr.addComponent("BossPartComponent").setLives(20)
		
		trtt=GameObject("enemy_TRturret")
		trtt.transform.setParent(tr.transform,False);
		trtt.transform.localPosition=Vector2((-4.3,-10.0))
		shp=trtt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		trtt.addComponent("TurretComponent")
		
		
		self.__parts={"b1":b1,"b2":b2,"b3":b3,"b4":b4,"wingl":wl,"wingr":wr,"taill":tl,"tailr":tr}
		