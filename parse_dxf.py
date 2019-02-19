import math
import ezdxf
import utils
import numpy as np
import cv2
import pylab as plt
from color_index import color_index

def get_msp_bound(msp):
	MAX=0x7FFFFFF
	left=top=MAX
	right=bottom=-MAX
	for polyline in msp:
		pts = polyline.points()
		for x,y in pts:
			left=min(left,x)
			top=min(top,y)
			right=max(right,x)
			bottom=max(bottom,y)
	return top,left,bottom,right

def display_msp(msp,size):
	print(size)
	canvas = np.ones(size, np.uint8)*255
	for polyline in msp:
		print('polyline: ' + str(polyline))
		pts = polyline.points()
		pre = None
		start = None
		for i, x in enumerate(pts):
			now = utils.tuple_int(x)
			if not i:
				pre = tuple(now)
				start = tuple(now)
				continue
			cv2.line(canvas, pre, now, (0, 0, 0))
			pre = tuple(now)
		cv2.line(canvas, pre, start, (0, 0, 0))
	plt.imshow(canvas)
	plt.show()


def cross( v1, v2):
	return (v1.S[0] - v1.E[0]) * (v2.S[1] - v2.E[1]) - (v1.S[1] - v1.E[1]) * (v2.S[0] - v2.E[0])

def dist(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def GetAreaOfTriangle(p1, p2, p3):
	'''计算三角形面积   海伦公式'''
	area = 0.0
	p1p2 = dist(p1, p2)
	p2p3 = dist(p2, p3)
	p3p1 = dist(p3, p1)
	s = (p1p2 + p2p3 + p3p1) / 2.0
	area = s * (s - p1p2) * (s - p2p3) * (s - p3p1)  # 海伦公式
	area = math.sqrt(area)
	return area

def GetAreaOfPolyGon(points):
	area = 0
	if (len(points) < 3):
		raise Exception("error")

	for i in range(0, len(points) - 1):
		p1 = points[i]
		p2 = points[i + 1]

		triArea = (p1[0] * p2[1] - p2[0] * p1[1]) / 2
		area += triArea
	return abs(area)

class LineSet(object):

	class Line(object):

		S=();E=()
		Next=None;Prior=None
		# def __eq__(self, other):
		# 	if self.S[0]==other.S[0] and \
		# 	   self.E[0] == other.E[0] and \
	     # 	   self.S[1] == other.S[1] and \
		# 	   self.E[1] == other.E[1] :
		# 		return True
		# 	return False
		# def __hash__(self):
		#
		def __str__(self):
			return f'({self.S[0]},{self.S[1]})->({self.E[0]},{self.E[0]})'
		def __init__(self,S,E):
			self.S=S
			self.E=E

		def t(self):
			try:
				return (self.E[1]-self.E[0])/(self.S[1]-self.S[0])
			except BaseException:
				return 0
		def n(self):
			try:
				return -1/self.t()
			except BaseException:
				return 0x7FFFFFFF
		def mid_pt(self):
			S = self.S;E = self.E
			return (S[0]+E[0])/2,(S[1]+E[1])/2
		def long(self):
			return dist(self.S,self.E)
		def is_intersect(self,line,seg):
			'''判断直线与线段是否相交'''
			def intersect_pt(u1,u2,v1,v2):
				'''求交点'''
				# L = LineSet.Line
				ret=list(u1)
				try:
					t=((u1[0]-v1[0])*(v1[1]-v2[1])-(u1[1]-v1[1])*(v1[0]-v2[0])) \
					/((u1[0]-u2[0])*(v1[1]-v2[1])-(u1[1]-u2[1])*(v1[0]-v2[0]))
				except BaseException:
					return None
				ret[0] += (u2[0] - u1[0]) * t
				ret[1] += (u2[1] - u1[1]) * t
				return tuple(ret)
				pass
			A=line.S; B=line.E; C=seg.S; D=seg.E
			L=LineSet.Line
			ans=cross(L(A, B), L(A, D)) * cross(L(A, B), L(A, C))
			if ans<=0:
				return intersect_pt(A,B,C,D)
			return None
		def getABC(self):
			x1,y1=self.S
			x2,y2=self.E
			A=y2-y1
			B=x1-x2
			C=x2*y1-x1*y2
			return A,B,C
		def circle_intersect(self,O,r):
			x1,y1=S=self.S
			x2,y2=E=self.E
			d1=dist(O,S)-r
			d2=dist(O,E)-r
			if d1*d2<0:
				return True
			elif d1<0 and d2 <0:
				return False
			else:
				A,B,C=self.getABC()
				x0,y0=O
				try:
					d=abs(x0*A+y0*B+C)/math.sqrt(A**2+B**2)
				except BaseException:
					return False
				if d<r:
					angle1 = (O[0] - x1) * (x2 - x1) + (O[1] - y1) * (y2 - y1);
					angle2 = (O[0] - x2) * (x1 - x2) + (O[1] - y2) * (y1 - y2);
					if (angle1 > 0 and angle2 > 0):
						return True
			return False
		def test(self):
			A=self.__init__((1, 2), (3, 4))

			print(type(A))

	def __init__(self,polyline):
		self.lines = []
		self.pts = []
		self.color = None
		print('polyline: ' + str(polyline))
		pts = polyline.points()
		pre = None;start = None
		preL=None;self.startL=None
		for i, x in enumerate(pts):
			self.pts.append(list(x))	#
			now = list(x)				#
			if i==0:
				pre = tuple(now)
				start = tuple(now)
				continue
			line = self.Line(pre, now)
			if i==1:
				self.startL=line
			line.Prior=preL
			if preL:preL.Next=line
			self.lines.append(line)
			pre = tuple(now)
			preL=line
		line = self.Line(pre, start)
		self.startL.Prior=line
		line.Next=self.startL
		self.lines.append(line)

	def get_bound(self):
		MAX = 0x7FFFFFF
		left = top = MAX
		right = bottom = -MAX
		for x, y in self.pts:
			left = min(left, x)
			top = min(top, y)
			right = max(right, x)
			bottom = max(bottom, y)
		return top, left, bottom, right
	def display(self,size):
		canvas = np.ones(size, np.uint8)*255
		line=self.startL;i=0
		while True:
			# print(i);i+=1
			if not line: break
			cv2.line(canvas, line.S, line.E, (0, 0, 0))
			line=line.Next
			if line is self.startL:
				break
		plt.imshow(canvas)
		plt.show()
	def display_line(self,size,obj_line):
		canvas = np.ones(size, np.uint8)*255
		line=self.startL;i=0
		while True:
			# print(i);i+=1
			if not line: break
			color=(0,0,0)
			width=1
			if line is obj_line:
				color=(255,0,0);width=3
			cv2.line(canvas, line.S, line.E, color,width)
			line=line.Next
			if line is self.startL:
				break
		plt.imshow(canvas)
		plt.show()
	def dislay_several_line(self,size,obj_line,lines):
		canvas = np.ones(size, np.uint8)*255
		line=self.startL;i=0
		while True:
			# print(i);i+=1
			if not line: break
			color=(0,0,0)
			width=1
			if line is obj_line:
				color=(255,0,0);width=1
			if line in lines:
				color = (0, 255, 0);width = 1
			cv2.line(canvas, line.S, line.E, color,width)
			line=line.Next
			if line is self.startL:
				break
		plt.imshow(canvas)
		plt.show()
	def display_new_line(self,size,nlines):
		canvas = np.ones(size, np.uint8)*255
		line=self.startL;i=0
		while True:
			# print(i);i+=1
			if not line: break
			color=(0,0,0)
			width=1
			cv2.line(canvas, line.S, line.E, color,width)
			line=line.Next
			if line is self.startL:
				break
		for line in nlines:
			color=(255,0,0)
			width=1
			cv2.line(canvas, utils.tuple_int(line.S), utils.tuple_int(line.E), color,width)
		plt.imshow(canvas)
		plt.show()
	def find_vertical_intersect(self,line):
		a=line.mid_pt()
		n=line.n()
		b=a[0]+1,a[1]+n
		v=self.Line(a,b)
		ans=[]
		# print(v.t())
		for l in self.lines:
			if l is line:
				continue
			intersect=l.is_intersect(v,l)
			if intersect:
				# print(l)
				# print(l.t())
				ans.append([l,intersect])
		return ans
	def find_circle_intersect(self,O,r):
		ans=[]
		for l in self.lines:
			if l.circle_intersect(O,r):
				ans.append(l)
		return ans
	def calc_width(self):
		line=self.startL
		nlines=[]
		pre=()
		max_width=0;mean_width=0
		while True:
			if not line:
				break
			pair=self.find_vertical_intersect(line)
			mind=0x7FFFFFF
			pt=None
			for l,spt in pair:
				di=dist(spt,line.mid_pt())
				if di<mind:
					mind=di
					pt=self.Line(spt,line.mid_pt()).mid_pt()
			if pt:
				cc=self.find_circle_intersect(pt,2*mind)
				if not pre:
					pre=pt
				else:
					nl=self.Line(pre,pt)
					pre=pt
					nlines.append(nl)
			line=line.Next
			mean_width+=mind
			max_width=max(max_width,mind)
		return max_width,mean_width
		# print(len(nlines))
		# self.display_new_line([500,500,3],nlines)
	def growth(self,line,neglect):
		k=0.7
		d=10
		def ok(v,lst):
			t=v.t()
			mid_pt=v.mid_pt()
			ok=False
			for l in lst:
				di = dist(mid_pt, l.mid_pt())
				print('di',di)
				if di<d:
					if abs(t-l.t())<k:
						ok=True
				else:
					lst.remove(l)
			return ok
		removed=set()
		ans=[]
		while True:
			if not line:
				break
			if line in neglect :
				break
			pair=self.find_vertical_intersect(line)
			# t=line.t()
			if ok(line,pair):
				removed|=set(pair)
				ans.append(line)
			else:break
			line=line.Next
		return ans,removed,line
	def segment_process(self):
		line=self.startL
		neglect=set()
		while True:
			if not line: break
			ans,removed,line=self.growth(line,neglect)
			ans+=list(removed)
			neglect|=removed
			print(len(ans))
			line_set.dislay_several_line([500,500,3], self.startL, ans)
			pass
	def reverse(self,size):
		def process_reverse( pt, Height):
			pt = (pt[0], Height - pt[1])
			return pt
		for line in self.lines:
			line.S=process_reverse(line.S,size[1])
			line.E=process_reverse(line.E,size[1])
		for i in range(len(self.pts)):
			self.pts[i][1]=size[0]-self.pts[i][1]
	def paint_polygon(self,size,canvas,ID):
		top, left, bottom, right=self.get_bound()
		x0=int((left+right)/2)
		y0=int((top+bottom)/2)
		fill_color=self.color
		# canvas = np.ones(size, np.uint8) * 255
		pts=np.array(self.pts,np.int32)
		pts=pts.reshape([-1,1,2])
		# print(canvas.dtype)
		cv2.fillPoly(canvas,[pts],fill_color)   #tuple(map(int,fill_color))
		font=cv2.FONT_HERSHEY_COMPLEX_SMALL#tuple(map(int,self.pts[-1]))
		cv2.putText(canvas,'%02d'%ID,(x0,y0), font, 1.2,(255,255,255),2)
		# cv2.polylines(canvas, [pts], True, (0, 0, 0), 1)
		# plt.imshow(canvas)
		# plt.show()
	def form_report(self):
		'''return long,max_width,mean_width'''
		long=0
		for l in self.lines:
			long+=l.long()
		long/=2
		max_width,sum_width=self.calc_width()
		ptn=len(self.pts)
		mean_width=sum_width/ptn
		area=GetAreaOfPolyGon(self.pts)
		return long,max_width,mean_width,area,sum_width,ptn



	# line_set.fun()
# display_msp(msp,int_bound)
