from Component import Component
import hou

class ScoreComponent(Component):
	def __init__(self,gobj,nodelevel="/obj"):
		super(ScoreComponent,self).__init__(gobj)
		self.__score=0
		self.__rewriteNeeded=True
		self.__shapes=[]
		self.__nodelevel=nodelevel
		
	def addScore(self,add):
		self.__score+=add
		self.__rewriteNeeded=True
		
	def update(self):
		gobj=self.gameObject()
		
		if(self.__rewriteNeeded):
			spareshapes=[x for x in self.__shapes]
			self.__shapes=[]
			stext=str(self.__score)
			for x in stext:
				node=None
				if(len(spareshapes)>0):
					node=spareshapes.pop(0)
				else:	
					node=hou.node(self.__nodelevel).createNode("null","score")
				
				node.setUserData("nodeshape","numbers"+x)
				self.__shapes.append(node)
				
			for shape in spareshapes:
				shape.destroy()
			self.__rewriteNeeded=False
		
		#position shapes
		pos=gobj.position
		for shape in self.__shapes:
			shape.setPosition(pos)
			pos+=hou.Vector2(0.75,0)
			
	def onDestroy(self):
		for shape in self.__shapes:
			shape.destroy()