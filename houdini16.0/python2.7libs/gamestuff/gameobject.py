
import os
import time
import importlib
import traceback
import re

import Component

import hou #for Vector2 and callbacks
from math import *

from PySide2.QtCore import *
from PySide2.QtGui import *  #for native keypress handling

class GameObject(object):
	__globalInit=False
	__startTime=0;
	__lastTime=-1
	__curTime=-1
	__instances=[]
	__destroyQueue=[]
	__toResolveDestroyQueue=False
	
	__keyCatcher=None
	_keystatusdown={}
	_keystatuspressed={}
	_keystatusreleased={}
	
	__modules=[]
	__modulesNeedRescan=True
	
	__paused=False
	__msgBuf1={}
	__msgBuf2={}
	__messages=__msgBuf1
	
	#helper class
	class TimeData:
		def __init__(self,time,timestep):
			self.__time=time
			self.__deltaTime=timestep
			
		def time(self):
			return self.__time
			
		def deltaTime(self):
			return self.__deltaTime
	
	#real shit from here
	
	
	@classmethod
	def scanModules(cls):
		'''
		scans for user modules
		'''
		#scan for modules
		basepath=os.path.dirname(__file__)
		cls.__modules=[x for x in os.listdir(basepath) if os.path.isdir(os.path.join(basepath,x)) and os.path.isfile(os.path.join(basepath,x,"__init__.py"))]
		print("found modules:")
		print(cls.__modules)
	
	def __init__(self,name="noname"):
		'''
		its better to keep name unique to be able to search by items
		if it's not unique - first match will be returned in search
		'''
		if(GameObject.__modulesNeedRescan):
			GameObject.scanModules()
			GameObject.__modulesNeedRescan=False
		
		self.time=GameObject.TimeData(0,0)
		self.__components=[]
		self.__componentsToStart=[]
		self.__name=name
		self.__transform=None
		self.__transform=GameObject.Transform(self)
		#self.position=hou.Vector2((0,0))
		#self.angle=0.0 #degrees, cuz fuck you
		#self.__started=False
		self.__destroyed=False
		
		#self.__messages=[]
		
		GameObject.__instances.append(self)
	
	def destroy(self):
		if(self.__destroyed):return
		print("obj marked to be destroyed")
		
		GameObject.__destroyQueue.append(self)
		self.__destroyed=True
		GameObject.__toResolveDestroyQueue=True
	
	def __start(self):
		'''
		just call all the onstart callbacks
		'''
		self.angle=self.angle%360
		for component in self.__components:
			component.time=self.time
			try:
				component.onStart()
			except Exception as e:
				print("GameObject %s: Exception during onStart of %s"%(self.__name,type(component).__name__))
				print(e.message)
				print("traceback")
				print(traceback.format_exc())
				
	
	def __update(self):
		self.angle=self.angle%360
		if(len(self.__componentsToStart)>0):
			for component in self.__componentsToStart:
				component.time=self.time
				try:
					component.onStart()
				except Exception as e:
					print("GameObject %s: Exception during onStart of %s"%(self.__name,type(component).__name__))
					print(e.message)
					print("traceback")
					print(traceback.format_exc())
			self.__componentsToStart=[]
			return
		
		for component in self.__components:
			component.time=self.time
			try:
				component.update()
			except Exception as e:
				print("GameObject %s: Exception during update of %s"%(self.__name,type(component).__name__))
				print(e.message)
				print("traceback")
				print(traceback.format_exc())
				
		if(len(GameObject.__messages)>0):
			currMsgs=GameObject.__messages
			if(GameObject.__messages is GameObject.__msgBuf1):
				GameObject.__messages=GameObject.__msgBuf2
			else:
				GameObject.__messages=GameObject.__msgBuf1
				
			for obj in currMsgs:
				for msg in currMsgs[obj]:
					for comp in obj.__components:
						rcv=getattr(comp,msg[0],None)
						if(rcv is None):continue
						if(callable(rcv)):
							try:
								if(msg[1] is None):
									rcv()
								else:
									rcv(msg[1])
							except Exception as e:
								print("GameObject %s: Exception during message %s sending to %s"%(obj.__name,str(msg),type(comp).__name__))
								print(e.message)
								print("traceback")
								print(traceback.format_exc())
								
			currMsgs.clear()

	
	#DONT USE AND DEL
	#def __processMessages(self):
	#	for msg in self.__messages:
	#		for comp in self.__components:
	#			rcv=getattr(comp,msg[0],None)
	#			if(rcv is None):continue
	#			if(callable(rcv)):
	#				try:
	#					if(msg[1] is None):
	#						rcv()
	#					else:
	#						rcv(msg[1])
	#				except Exception as e:
	#					print("GameObject %s: Exception during message %s sending to %s"%(self.__name,str(msg),type(comp).__name__))
	#					print(e.message)
	#					print("traceback")
	#					print(traceback.format_exc())
	#	self.__messages=[]
	
	
	def addComponent(self,compname):
		module=None
		try:
			module=importlib.import_module("gamestuff."+compname)
		except:
			bad=True
			for modulename in GameObject.__modules:
				try:
					#print("trying to import "+"gamestuff."+modulename+"."+compname)
					module=importlib.import_module("gamestuff."+modulename+"."+compname)
					bad=False
					break
				except:
					pass
			if(bad):
				print("module "+compname+" not found")
				return None
		try:
			comp=getattr(module,compname)(self)
		except:
			print("couldnt create component  %s class instance"%compname)
			return None
		#a little cheat to keep shape component always atop
	
		if(len(self.__components)>0 and type(self.__components[-1]).__name__=="ShapeComponent"):
			self.__components.insert(-1,comp)
		else:
			self.__components.append(comp)
		self.__componentsToStart.append(comp)
			
	
		return comp
	
	def getComponent(self,compname):
		'''
		returns a component in this object that has
		compname somewhere in inheritance hierarchy
		or None if none found
		'''
		for comp in self.__components:
			classnames=[x.__name__ for x in type(comp).__mro__]
			for name in classnames:
				name=name[name.rfind(".")+1:]
				if(name==compname):
					return comp
				if(name=="Component"):break #we hit component bedrock
		return None
		
#		lst=[x for x in self.__components if type(x).__name__==compname]
#		if(len(lst)==0):
#			#lst=[x for x in self.__components if issubclass(x,eval(compname+"."+compname))]
#			#if(len(lst)==0):
#			raise AttributeError()
#			
#		return lst[0]
	
	def sendMessage(self,message,parms=None):
		if(self not in GameObject.__messages):
			GameObject.__messages[self]=[]
		GameObject.__messages[self].insert(0,(message,parms))
			
	
	#transform
	@property
	def transform(self):
		return self.__transform

	@transform.setter
	def transform(self,val):
		if(self.__transform is not None and self.__transform is not val):
			raise ValueError("gameobject cannot be reassigned transforms")
			#why do i do this restriction?.... technically - it doesnt matter
		self.__transform=val

	@property
	def position(self):
		'''
		shortcut to transform.position
		'''
		return self.transform.position

	@position.setter
	def position(self,pos):
		self.transform.position=pos

	@property
	def angle(self):
		'''
		shortcut to transform.angle
		'''
		return self.transform.angle

	@angle.setter
	def angle(self,ang):
		self.transform.angle=ang

	def fwd(self):
		'''
		shortcut to transform.fwd()
		'''
		return self.transform.fwd()
		

	class Transform(object):
		def __init__(self,gobj):
			if(not isinstance(gobj,GameObject)):
				raise TypeError("gobj must be a valid GameObject instance")
			gobj.transform=self
			self.__gameObject=gobj
			self.__localposition=hou.Vector2()
			self.__parent=None
			self.__children=set()
			self.__localangle=0

			self.__position=hou.Vector2()   #actually cached position
			self.__angle=0 #actually cached angle

			self.__requiresupdate=True
			self.__transmat=None#hou.Matrix3(1)
			self.__itransmat=None#hou.Matrix3(1)

			
		def gameObject(self):
			return self.__gameObject
			
			
		def __m3v2(self,mtx3,vec2):
			p=[0,0]
			p[0]=vec2[0]*mtx3.at(0,0) + vec2[1]*mtx3.at(1,0) + mtx3.at(2,0)
			p[1]=vec2[0]*mtx3.at(0,1) + vec2[1]*mtx3.at(1,1) + mtx3.at(2,1)
			return hou.Vector2((p[0],p[1]))		
		
		
		def parent(self):
			return self.__parent
			
		def children(self):
			'''
			should be used only to iterate
			should not ever be changed from outside the class
			'''
			return self.__children
		
		def setParent(self,parent,keep_global_pos=True):
			if(not isinstance(parent, GameObject.Transform) and parent is not None):
				raise TypeError("Parent should be a transform or None")
			if(self.__parent is parent):return
			gpos=self.position
			if(self.__parent is not None):
				self.__parent.__children.remove(self)
			self.__parent=parent
			if(parent is not None):
				parent.__children.add(self)
			
			if(keep_global_pos):
				self.position=gpos #here we make sure global pos after reparenting stays the same
			else:
				self.__setChanged()
			# self.__setChanged() #no need since it will be called in position setter
			#BUT if you choose to make optimize pos setters in a way they might sometimes avoid calling __setChanged - it should be called here explicitly!


		def __setChanged(self):
			'''
			informs node and its children that their's global transform require updating
			there should not be any situations when you would want to call that from outside of this class
			'''
			self.__requiresupdate=True
			for child in self.__children:
				child.__setChanged()
		
		def update(self):
			'''
			updates global position and angle from hierarchy and locals
			'''
			if(not self.__requiresupdate):return
			
			if(self.__parent is None):
				self.__angle=self.__localangle      #warning, even though we copy mutable ref - we still do not operate on those objects ever
				self.__position=self.__localposition
			else:
				self.__angle=(self.__parent.angle+self.__localangle)%360
				self.__position=self.__m3v2(self.__parent.getTransform(),self.__localposition)
			self.__requiresupdate=False
			self.__transmat=None
			self.__itransmat=None
			

				
		def getTransform(self):
			self.update()
			if(self.__transmat is None):
				rangle=radians(self.__localangle)
				co=cos(rangle)
				si=sin(rangle)
				pos=self.__localposition
				localmat=hou.Matrix3(((co,si,0.0),(-si,co,0.0),(pos[0],pos[1],1.0)))
				if(self.__parent is not None):
					self.__transmat=self.__parent.getTransform()*localmat
				else:
					self.__transmat=localmat
			return self.__transmat
		
		def getInverseTransform(self):
			self.update()
			if(self.__itransmat is None):
				self.__itransmat=self.getTransform().inverted()
			return self.__itransmat
			
		
		@property
		def position(self):
			self.update()
			return self.__position

		@position.setter
		def position(self,pos):
			if(not isinstance(pos,hou.Vector2)):
				raise TypeError("position must be of type Vector2")
			if(self.__parent is not None):
				iptr=self.__parent.getInverseTransform()
				lp=self.__m3v2(iptr,pos)
				self.localPosition=lp
			else:
				self.localPosition=pos
				#self.__position=Vector2((pos[0],pos[1])) to preserve uniform behaviour this will be set during next transform update


		@property
		def localPosition(self):
			return self.__localposition

		@localPosition.setter
		def localPosition(self,pos):
			if(not isinstance(pos,hou.Vector2)):
				raise TypeError("position must be of type Vector2")
			self.__localposition=hou.Vector2((pos[0],pos[1]))
			self.__setChanged()

		#same shit with angles TBD
		@property
		def angle(self):
			self.update()
			return self.__angle

		@angle.setter
		def angle(self,ang):
			if(not (isinstance(ang,float) or isinstance(ang,int))):
				raise TypeError("angle must be a float or int")

			if(self.__parent is not None):
				self.localAngle=(ang-self.__parent.angle)%360
			else:
				self.localAngle=ang
		
		@property
		def localAngle(self):
			return self.__localangle
			
		@localAngle.setter
		def localAngle(self,ang):
			if(not (isinstance(ang,float) or isinstance(ang,int))):
				raise TypeError("angle must be a float or int")
			self.__localangle=ang
			self.__setChanged()
		
		#also
		def fwd(self):
			'''
			get forward pointin normal hou.Vector2
			'''
			rangle=radians(self.angle)
			si=sin(rangle)
			co=cos(rangle)
			x=-si
			y=co
			return hou.Vector2((x,y))
			
		def lookAtPointAngle(self,point):
			d=point-self.position
			d=d.normalized()
			angle=degrees(acos(d[1]))
			if(d[0]>0):angle=360-angle
			return angle

	
	def getName(self):
		return self.__name
	
	def setName(self,name):
		self.__name=name
		#if any hashings took place - rehash now
	
	def debugInfo(self):
		print(self.__components)
		print(self.__instances)
		
	#usefull static methods	
	@classmethod
	def isKeyDown(cls,key):
		'''
		GameObject instance objects can check the keyboard state with this shit
		'''
		if not(key in cls._keystatusdown):return False
		return cls._keystatusdown[key]
	
	@classmethod
	def isKeyPressed(cls,key):
		if not(key in cls._keystatuspressed):return False
		return cls._keystatuspressed[key]
	
	@classmethod
	def isKeyReleased(cls,key):
		if not(key in cls._keystatusreleased):return False
		return cls._keystatusreleased[key]
	
	@classmethod
	def findObject(cls,name):
		'''
		finds and returns the first object that matches name
		or returns None if not found
		'''
		l=cls.findObjects(name)
		if(len(l)==0):return None
		return l[0]
	
	@classmethod
	def findObjects(cls,name):
		l=[x for x in cls.__instances if re.match(name,x.__name) is not None]
		return l
	
	#control static methods
	@classmethod
	def destroyAllObjects(cls):
		'''
		Spare noone and may god have mercy upon their souls!
		'''
		cins=len(cls.__instances)
		for obj in cls.__instances:
			obj.destroy()
		cls.__resolveDestroyQueue()
		cls.__instances=[]
		
	@classmethod
	def reset(cls):
		'''
		reset the game state
		'''
		cls.__paused=False
		cls.destroyAllObjects()
		cls.__globalInit=False
		GameObject.__modulesNeedRescan=True
	
	#internal static methods
	@classmethod
	def __resolveDestroyQueue(cls):
		if(cls.__toResolveDestroyQueue):
			for obj in cls.__destroyQueue:
				if obj in cls.__instances:
					for component in obj.__components:
						try:
							component.onDestroy()
						except Exception as e:
							print("GameObject %s: Exception during destroying %s"%(obj.__name,type(component).__name__))
							print(e.message)
							print("traceback")
							print(traceback.format_exc())
					#remove from hierarchy
					for child in list(obj.transform.children()):
						child.setParent(None)
					obj.transform.setParent(None)
					#destroy destroy
					cls.__instances.remove(obj)
			cls.__destroyQueue=[]
			cls.__toResolveDestroyQueue=False
			
	
	#utility static methods
	@classmethod
	def globalUpdateCallback(cls):
		'''
		this global callback should be attached to some global timer or event loop
		there are more convenient wrappers lower
		'''
		#first destroy everything queued
		cls.__resolveDestroyQueue()
		##and continue
		cls.__lastTime=cls.__curTime
		timetime=time.time()
		
		if(not cls.__globalInit):
			cls.__startTime=timetime
			cls.__lastTime=-0.04
			cls.__globalInit=True
				
		cls.__curTime=timetime-cls.__startTime
		deltaTime=cls.__curTime-cls.__lastTime
		
		if(cls.isKeyPressed(Qt.Key_P)):
			cls.__paused=not cls.__paused
			if(cls.__paused):
				cls.__pausedTime=timetime
			else:
				pdt=timetime-cls.__pausedTime
				cls.__startTime+=pdt
				cls.__curTime-=pdt
		
		pausebypass=False
		if(cls.isKeyPressed(Qt.Key_O) and cls.__paused):
			pausebypass=True
		
		if(cls.__paused and not pausebypass):
			GameObject._keystatusreleased.clear()
			GameObject._keystatuspressed.clear()
			return
		
		for obj in cls.__instances:
			obj.time=GameObject.TimeData(cls.__curTime,deltaTime)
			obj.__update()
			
		#now serve messages		
		#TODO: rethink concept - maybe messages should be delivered in between object updates
		#for obj in cls.__instances:
		#	obj.__processMessages()
			
		
		GameObject._keystatusreleased.clear()
		GameObject._keystatuspressed.clear()
			
	@classmethod
	def installKeyCatcher(cls):
		if(cls.__keyCatcher is not None):return
		cls.__keyCatcher=GameObject._KeyCatcher()
		app=QGuiApplication.instance()
		cls.__keyCatcher.moveToThread(app.thread())
		app.installEventFilter(cls.__keyCatcher)
	
	@classmethod
	def uninstallKeyCatcher(cls):
		if(cls.__keyCatcher is None):return
		app=QGuiApplication.instance()
		app.removeEventFilter(cls.__keyCatcher)
		cls.__keyCatcher=None
	
	@classmethod
	def startHoudiniLoop(cls):
		cls.reset()
		cls.installEventFilter()
		if(cls.globalUpdateCallback not in hou.ui.eventLoopCallbacks()):
			hou.ui.addEventLoopCallback(cls.globalUpdateCallback)
	
	@classmethod	
	def pauseHoudiniLoop(cls):
		if(cls.globalUpdateCallback in hou.ui.eventLoopCallbacks()):
			hou.ui.removeEventLoopCallback(cls.globalUpdateCallback)
	
	@classmethod	
	def unpauseHoudiniLoop(cls):
		if(cls.globalUpdateCallback not in hou.ui.eventLoopCallbacks()):
			hou.ui.addEventLoopCallback(cls.globalUpdateCallback)
		
	@classmethod
	def stopHoudiniLoop(cls):
		if(cls.globalUpdateCallback in hou.ui.eventLoopCallbacks()):
			hou.ui.removeEventLoopCallback(cls.globalUpdateCallback)
		cls.uninstallKeyCatcher()
		cls.destroyAllObjects()
	
	class _KeyCatcher(QObject):
		def __init__(self,parent=None):
			super(GameObject._KeyCatcher,self).__init__(parent)
			
		def eventFilter(self,obj,event):
			if(event.type()==QEvent.KeyPress):
				GameObject._keystatusdown[event.key()]=True
				GameObject._keystatuspressed[event.key()]=True
				#print("key %d pressed"%event.key())
			if(event.type()==QEvent.KeyRelease):
				GameObject._keystatusdown[event.key()]=False
				GameObject._keystatusreleased[event.key()]=True
				#print("key %d released"%event.key())
				
			return super(GameObject._KeyCatcher,self).eventFilter(obj,event)
			