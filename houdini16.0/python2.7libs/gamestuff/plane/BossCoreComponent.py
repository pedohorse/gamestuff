from gamestuff.Component import Component
from gamestuff.gameobject import GameObject
from PlaneGameDirector import PlaneGameDirector

from hou import Vector2
from math import *

class BossCoreComponent(Component):
	
	def __init__(self,gobj):
		super(BossCoreComponent,self).__init__(gobj)
		self.__parts={}

		
		
		self.__state="goto"
		self.__nextState="stage1"
		self.__targetpos=Vector2((0,15))
		
		self.__assfire=None
		self.__stage1_timer=0
		self.__stage1_c=0
		self.__stage2_timer=0
		self.__stage2_spawntimer=0
		self.__stage2_c=0
		self.__stage3_timer=0
		self.__stage3_c=0
		self.__stage3_speed=0
		self.__stage3_timer=0
	
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
		elif(self.__state=="stage1"):											#STATE STAGE1
			#init
			if(self.__nextState==""):
				self.__nextState="stage1_tailremain"
				self.__parts["taill"].sendMessage("setActive",True)
				self.__parts["tailr"].sendMessage("setActive",True)
			#do stuff
			self.__stage1_timer+=dt
			gobj.position[0]+=0.2*cos(self.__stage1_timer)
			if(self.__parts["taill"] is None and self.__stage1_c%2==0):
				self.__stage1_c+=1
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b4"].transform)
				af.transform.localPosition=Vector2((-1.351,-9.179))
				af.transform.localAngle=107
				af.addComponent("BurningComponent").setConfig(length=2,intensity=1,angleVariation=90)
			if(self.__parts["tailr"] is None and (self.__stage1_c/2)%2==0):
				self.__stage1_c+=2
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b4"].transform)
				af.transform.localPosition=Vector2((1.351,-9.179))
				af.transform.localAngle=253
				af.addComponent("BurningComponent").setConfig(length=2,intensity=1,angleVariation=90)
				
			#translate
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
			self.__stage1_timer+=dt
			gobj.position[0]+=0.4*cos(self.__stage1_timer*2)
			#translate
			if(self.__parts["b4"] is None):
				self.__targetpos=Vector2(9,9)
				self.__state="goto"
				
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b3"].transform)
				af.transform.localPosition=Vector2((0,-7.18))
				af.transform.localAngle=180
				af.addComponent("BurningComponent").setConfig(length=4,intensity=0.5)
				
				if(self.__assfire is None):
					goass=GameObject("killzone_enemy")
					goass.transform.setParent(self.__parts["b3"].transform,False)
					self.__assfire=goass.addComponent("AssfireComponent")
				
		elif(self.__state=="stage2"):												#STATE STAGE2
			#init
			if(self.__nextState==""):
				self.__nextState="stage3"
				self.__parts["wingl"].sendMessage("setActive",True)
				self.__parts["wingr"].sendMessage("setActive",True)

			#do stuff
			self.__stage2_timer+=dt
			x=self.__stage2_timer*0.2
			x=(0.5+0.5*cos(x))**(20**(-cos(x)))
			gobj.position[0]=2*(x-0.5)*9
			if(x<0.05 or x>0.95):
				self.__stage2_spawntimer+=dt
				if(self.__stage2_spawntimer>=0.7):
					self.__stage2_spawntimer=0
					PlaneGameDirector.instance().createEnemySimple("plane_evil01","s", Vector2((0,9.9)), Vector2((0,-4)),2,2,0,destroyCallback=PlaneGameDirector.instance().explosion)
					#PlaneGameDirector.instance().createEnemySimple("plane_evil01","s", Vector2((4,9.9)), Vector2((0,-4)),2,2,0)
			self.__assfire.setFlameMode(int(1.5+1.5*sin(self.__stage2_timer-radians(90))))
			
			if(self.__parts["wingl"] is None and self.__stage2_c%2==0):
				self.__stage2_c+=1
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b2"].transform)
				af.transform.localPosition=Vector2((-1.803,-0.045))
				af.transform.localAngle=90
				af.addComponent("BurningComponent").setConfig(length=5,intensity=1,angleVariation=90)
			if(self.__parts["wingr"] is None and (self.__stage2_c/2)%2==0):
				self.__stage2_c+=2
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b2"].transform)
				af.transform.localPosition=Vector2((1.803,-0.045))
				af.transform.localAngle=270
				af.addComponent("BurningComponent").setConfig(length=5,intensity=1,angleVariation=90)
			
			#translate
			if(self.__parts["wingl"] is None and self.__parts["wingr"] is None):
				self.__targetpos=Vector2((0,6))
				self.__assfire.setFlameMode(0)
				self.__state="goto"
		elif(self.__state=="stage3"):												#STATE STAGE3
			#init
			if(self.__nextState==""):
				self.__nextState="destroy"
				self.__parts["b3"].sendMessage("setActive",True)
			#do stuff
			if(self.__parts["b3"] is None and self.__stage3_c==0):
				self.__stage3_c=1
				self.__parts["b2"].sendMessage("setActive",True)
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b2"].transform)
				af.transform.localPosition=Vector2((0,-3.0))
				af.transform.localAngle=180
				af.addComponent("BurningComponent").setConfig(length=4,intensity=1.5)
			if(self.__parts["b2"] is None and self.__stage3_c==1):
				self.__stage3_c=2
				self.__parts["b1"].sendMessage("setActive",True)
				#fire up the ass a bit
				af=GameObject("assfire")
				af.transform.setParent(self.__parts["b1"].transform)
				af.transform.localPosition=Vector2((0,3.0))
				af.transform.localAngle=180
				af.addComponent("BurningComponent").setConfig(length=4,intensity=2)
				
			mult=1 + self.__stage3_c*0.5
			self.__stage3_timer+=dt*mult
			if(self.__stage3_timer>1.5):
				self.__stage3_speed=min(self.__stage3_speed+3*dt*mult,7)
				if(gobj.position[1]>25):
					self.__stage3_speed=0
					player=PlaneGameDirector.instance().getPlayer()
					ppx=0
					if(player is not None):ppx=player.position[0]
					gobj.position=Vector2((ppx,-16))
					self.__stage3_timer=0
			gobj.position+=Vector2((0,self.__stage3_speed*dt))
			
			#translate
			if(self.__parts["b1"] is None):
				self.__targetpos=Vector2((0,5))
				self.__state="desetroy"
				PlaneGameDirector.instance().stuffWasDestroyed(self.gameObject(),True)
				gobj.destroy()
				PlaneGameDirector.instance().bigExplosion(Vector2((0,0)),time=5,radius=8)
				
		
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
		shp=b1.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_body1")
		shp.setColor((0.6,0.6,0.65))
		b1.addComponent("BoundingBoxComponent")
		b1.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b1.addComponent("BossPartComponent").setLives(40)
		
		
		b2=GameObject("enemy_BOSS_CENTER")
		b2.transform.setParent(gobj.transform,False)
		shp=b2.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_body2")
		shp.setColor((0.6,0.6,0.65))
		b2.addComponent("BoundingBoxComponent")
		b2.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b2.addComponent("BossPartComponent").setLives(30)
		
		
		b3=GameObject("enemy_BOSS_BODY")
		b3.transform.setParent(gobj.transform,False)
		shp=b3.addComponent("ShapeComponent")
		shp.setColor((0.6,0.6,0.65))
		shp.setBaseShape("big_boss_body3")
		b3.addComponent("BoundingBoxComponent")
		b3.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b3.addComponent("BossPartComponent").setLives(70)
		
		
		b4=GameObject("enemy_BOSS_TAIL")
		b4.transform.setParent(gobj.transform,False)
		shp=b4.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_body4")
		shp.setColor((0.6,0.6,0.65))
		b4.addComponent("BoundingBoxComponent")
		b4.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		b4.addComponent("BossPartComponent").setLives(70)
		
		
		wl=GameObject("enemy_BOSS_WINDL")
		wl.transform.setParent(gobj.transform,False)
		shp=wl.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_wingl")
		shp.setColor((0.6,0.6,0.65))
		wl.addComponent("BoundingBoxComponent")
		wl.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		wl.addComponent("BossPartComponent").setLives(200)
		
		
		wr=GameObject("enemy_BOSS_WINDR")
		wr.transform.setParent(gobj.transform,False)
		shp=wr.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_wingr")
		shp.setColor((0.6,0.6,0.65))
		wr.addComponent("BoundingBoxComponent")
		wr.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		wr.addComponent("BossPartComponent").setLives(200)
		
		
		tl=GameObject("enemy_BOSS_TAILL")
		tl.transform.setParent(gobj.transform,False)
		shp=tl.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_taill")
		shp.setColor((0.6,0.6,0.65))
		tl.addComponent("BoundingBoxComponent")
		tl.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		tl.addComponent("BossPartComponent").setLives(70)
		
		
		tr=GameObject("enemy_BOSS_TAILR")
		tr.transform.setParent(gobj.transform,False)
		shp=tr.addComponent("ShapeComponent")
		shp.setBaseShape("big_boss_tailr")
		shp.setColor((0.6,0.6,0.65))
		tr.addComponent("BoundingBoxComponent")
		tr.addComponent("ActiveCollisionCheckerComponent").setCollisionMask("bullet_player")
		tr.addComponent("BossPartComponent").setLives(70)
		
		trtt=GameObject("enemy_TRturret")
		trtt.transform.setParent(tr.transform,False);
		trtt.transform.localPosition=Vector2((4.3,-10.0))
		trtt.transform.localAngle=180
		shp=trtt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		trtt.addComponent("TurretComponent").setActive(False)
		
		tltt=GameObject("enemy_TLturret")
		tltt.transform.setParent(tl.transform,False);
		tltt.transform.localPosition=Vector2((-4.3,-10.0))
		tltt.transform.localAngle=180
		shp=tltt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		tltt.addComponent("TurretComponent").setActive(False)
		
		b4tt=GameObject("enemy_B4turret")
		b4tt.transform.setParent(b4.transform,False);
		b4tt.transform.localPosition=Vector2((0,-9.0))
		b4tt.transform.localAngle=180
		shp=b4tt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		b4tt.addComponent("TurretComponent").setActive(False)
		
		wltt=GameObject("enemy_WLturret")
		wltt.transform.setParent(wl.transform,False);
		wltt.transform.localPosition=Vector2((-9.0,-1.26))
		wltt.transform.localAngle=180
		shp=wltt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		wltt.addComponent("TurretComponent").setActive(False)
		
		wrtt=GameObject("enemy_WRturret")
		wrtt.transform.setParent(wr.transform,False);
		wrtt.transform.localPosition=Vector2((9.0,-1.26))
		wrtt.transform.localAngle=180
		shp=wrtt.addComponent("ShapeComponent")
		shp.setBaseShape("turret")
		shp.setColor((0.3,0.3,0.35))
		wrtt.addComponent("TurretComponent").setActive(False)
		
		self.__parts={"b1":b1,"b2":b2,"b3":b3,"b4":b4,"wingl":wl,"wingr":wr,"taill":tl,"tailr":tr}
		