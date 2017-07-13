from Component import Component
import hou

class ShapeComponent(Component):
	
	def __init__(self,gobj,shapename="light",nodelevel="/obj"):
		super(ShapeComponent,self).__init__(gobj)
		
		basenode=hou.node(nodelevel)
		self.__mynode=basenode.createNode("null","n0")
		self.__mynode.setUserData("nodeshape",shapename+"_0")
		self.__baseshape=shapename
		self.__lastShapeid=-1
		self.__shapeid=0
		self.__mynode.setUserData("nodeshape",self.__baseshape+"_0")
		self.__animated=False
		self.__animationFrame=0
		self.__lastAnimationFrame=-1
		
		self.__currentShapeName=self.__baseshape+"_0"
		
		self.update() #immediately set pos and shape
	
	def setAnimationFrame(self,frame):
		self.__animationFrame=int(frame)
	
	def setAnimated(self,isAnimated):
		self.__animated=isAnimated
		if(self.__animated):
			self.__currentShapeName="_".join([self.__baseshape,str(self.__animationFrame),str(self.__shapeid)])
		else:
			self.__currentShapeName="_".join([self.__baseshape,str(self.__shapeid)])
		self.__mynode.setUserData("nodeshape",self.__currentShapeName)
	
	def setBaseShape(self,baseshape):
		self.__baseshape=baseshape
		#self.__mynode.setUserData("nodeshape",self.__baseshape+"_0")
		self.__lastShapeid=-1
		self.__lastAnimationFrame=-1
		self.update() #immediately set pos and shape
		#todo: here we should signal colliders that shape changed
		
	def getBaseShape(self):
		return self.__baseshape
		
	def setColor(self,clr):
		if(type(clr) is hou.Color):
			self.getHouNode().setColor(clr)
		else:
			self.getHouNode().setColor(hou.Color(clr))
	
	def getCurrentShapeName(self):
		return self.__currentShapeName
	
	def getHouNode(self):
		'''
		gets the visual representation - hou.Node
		please, dont destroy the node or do anything inappropriate with it
		moving it also wont work, cuz this component rewrites it's position and shape every update
		'''
		return self.__mynode
	
	def update(self):
		gobj=self.gameObject()
		
		pos=gobj.position
		ang=float(gobj.angle)
		
		self.__shapeid=int(round(ang/22.5))%16
		#print("%d %d"%(self.__shapeid,ang))
		if(self.__animated):
			if(self.__shapeid!=self.__lastShapeid or self.__lastAnimationFrame!=self.__animationFrame):
				self.__currentShapeName="_".join([self.__baseshape,str(self.__animationFrame),str(self.__shapeid)])
				self.__mynode.setUserData("nodeshape",self.__currentShapeName)
				self.__lastAnimationFrame=self.__animationFrame
		else:
			if(self.__shapeid!=self.__lastShapeid):
				self.__currentShapeName="_".join([self.__baseshape,str(self.__shapeid)])
				self.__mynode.setUserData("nodeshape",self.__currentShapeName)
		self.__mynode.setPosition(pos)
		self.__lastShapeid=self.__shapeid
		
	def onDestroy(self):
		self.__mynode.destroy()