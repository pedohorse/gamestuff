from gamestuff.Component import Component
from PlaneGameDirector import PlaneGameDirector
from gamestuff.gameobject import GameObject
from hou import Vector2

class StackShapesComponent(Component):
	def __init__(self,gobj):
		super(StackShapesComponent,self).__init__(gobj)
		self.__shapeObjs=[]
		self.__offset=Vector2((0.2,0))
		self.__shapeBaseName=""
		self.__count=0
	
	def setCount(self,count):
		if(self.__count==count):return
		if(self.__count<count):
			for i in range(count-self.__count):
				go=self.__createAnotherShape()
				go.transform.localPosition=self.__offset*(self.__count+i)
				go.transform.setParent(self.gameObject().transform,False)
				self.__shapeObjs.append(go)
		else:
			for i in range(self.__count-count):
				self.__shapeObjs.pop(-1).destroy()
		self.__count=count
		self.__recolor()
	
	
	def __recolor(self):
		clr=1.0
		for obj in reversed(self.__shapeObjs):
			obj.sendMessage("setColor",(clr,clr,clr))
			clr=(clr-0.4)*0.75+0.4
		
	def __createAnotherShape(self):
		go=GameObject("stackshapepiece")
		go.addComponent("ShapeComponent").setBaseShape(self.__shapeBaseName)
		return go
	
	def setBaseShape(self,baseshape):
		self.__shapeBaseName=baseshape
		for obj in self.__shapeObjs:
			obj.sendMessage("setBaseShape",self.__shapeBaseName)
	
	def onStart(self):
		pass
		
	def update(self):
		pass