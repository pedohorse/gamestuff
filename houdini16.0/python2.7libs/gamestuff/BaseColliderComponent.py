from Component import Component
import hou

class BaseColliderComponent(Component):
	def __init__(self,gobj):
		super(BaseColliderComponent,self).__init__(gobj)
		
		#warning: these radiuses are super important and it's your responsibility to set them in children classes
		self._radius=99999
		self._radius2=99999
		self._pivot=hou.Vector2()
		
	def getConvexHull(self):
		'''
		should return specific convex hull points in a list or touple 
		'''
		raise NotImplementedError()
		
	def isPointInside(self,pointpos,offset=0):
		'''
		should return True if point is inside the collider, False otherwise
		'''
		raise NotImplementedError()
		
		#and that collision detection code should move here
		
	@classmethod
	def cross2d(cls,a,b):
		'''
		helper function
		'''
		return a[0]*b[1]-a[1]*b[0]
	
	
	def __crosscheck(self,pts,opts):
		'''
		helper function
		returns (isNonintersecting? , axis of separation)
		'''
		pp=pts[-1]
		good=False
		axis=hou.Vector2()
		for p in pts:
			v=p-pp
			good=True
			for op in opts:
				if(self.cross2d(v,op-pp)>0):
					good=False
					break
			if(good):
				axis=v
				break
			pp=p
		return (good,axis)
	
	
	def collidesWith(self,otherobj):
		'''
		checks is this bbox collides with another gameobject
		returns 
		'''
		ocol=None
		if(isinstance(otherobj,BaseColliderComponent)):
			ocol=otherobj
		elif(isinstance(otherobj,type(self.gameObject()))):
			ocol=otherobj.getComponent("BaseColliderComponent")
			if(ocol is None):return False
			
		if((self.gameObject().position+self._pivot - ocol.gameObject().position-ocol._pivot).length() > self._radius+ocol._radius):return False
		opts=ocol.getConvexHull()
		
		pts=self.getConvexHull()
		
		(good,_)=self.__crosscheck(pts,opts)
		if(good):return False
		(good,_)=self.__crosscheck(opts,pts)
		if(good):return False
		return True