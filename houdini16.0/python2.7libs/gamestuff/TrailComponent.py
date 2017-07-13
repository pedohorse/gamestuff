from Component import Component

class TrailComponent(Component):
	def __init__(self,gobj):
		super(TrailComponent,self).__init__(gobj)
		self.__trail=[]
		self.__maxlength=1
	
	def update(self):
		super(TrailComponent,self).update()
		gobj=self.gameObject()
		self.__trail.insert(0,(self.time.time(),gobj.position,gobj.angle))
		if(self.time.time()-self.__trail[-1][0] > self.__maxlength):self.__trail.pop()

	def getMaxLength(self):
		return self.__maxlength
		
	def setMaxLength(self,sec):
		self.__maxlength=sec
	
	def getTrailByDist(self,distoffset):
		ltrail=len(self.__trail)
		if(ltrail==0):return (self.time.time(),self.gameObject().position,self.gameObject().angle)
		
		i=0
		dist=0
		pp=self.gameObject().position
		cp=self.__trail[0][1]
		step=(cp-pp).length()
		while(i<ltrail-1 and dist+step<distoffset):
			dist+=step
			i+=1
			pp=cp
			cp=self.__trail[i][1]
			step=(cp-pp).length()
		if(i>=ltrail-1):return self.__trail[-1]
		
		#interpolate
		x0=self.__trail[i]
		x1=self.__trail[i+1]
		t=(distoffset-dist)/step
		
		a0=x0[2]
		a1=x1[2]
		if(a1-a0>180):a1-=360
		elif(a1-a0<-180):a1+=360
		
		return (x0[0]*(1-t)+x1[0]*t,x0[1]*(1-t)+x1[1]*t,a0*(1-t)+a1*t)
	
	def getTrailByTime(self,timeoffset):
		ltrail=len(self.__trail)
		if(ltrail==0):return (self.time.time(),self.gameObject().position,self.gameObject().angle)
		i=0
		totime=self.time.time()-timeoffset
		
		#print(self.__trail)
		while(i<ltrail and self.__trail[i][0]>totime):i+=1
		if(i==ltrail):return self.__trail[-1]
		#if(i==0):return self.__trail[0]
		
		#interpolate
		x0=self.__trail[i]
		x1=self.__trail[i-1]
		t=(totime-x0[0])/(x1[0]-x0[0])
		
		a0=x0[2]
		a1=x1[2]
		if(a1-a0>180):a1-=360
		elif(a1-a0<-180):a1+=360
		
		return (totime,x0[1]*(1-t)+x1[1]*t,a0*(1-t)+a1*t)
		
	def setMaxLength(self,seconds):
		self.__maxlength=seconds