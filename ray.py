#!/usr/bin/python3
import math
import numpy.matlib as np
import sys

fin=open(sys.argv[1],"r")
try:
	json=eval(fin.read())
finally:
	fin.close()
screen=json['screen']
camera=json['camera']
objects=json['objects']

w=screen['w']
h=screen['h']
ratiox=screen['ratiox']
ratioy=screen['ratioy']
if len(sys.argv) > 2:
	w=int(sys.argv[2])
if len(sys.argv) > 3:
	h=int(sys.argv[3])
if len(sys.argv) > 4:
	ratiox=float(sys.argv[4])
if len(sys.argv) > 5:
	ratioy=float(sys.argv[5])
ww=1.*ratiox
hh=ww*h/w*ratioy
tab=[['.' for x in range(w)] for y in range(h)]
e=np.array(camera['loc'],dtype=float)
f=np.array(camera['front'],dtype=float)
u=np.array(camera['up'],dtype=float)
sphs=[]
for sph in objects:
	sphs += [np.array(sph['data'],dtype=float)]
u/=np.linalg.norm(u)
r=np.cross(f,u)
u=np.cross(r,f)
u/=np.linalg.norm(u)
r/=np.linalg.norm(r)

def SolveTri(a,b,c):
	d=b*b-4*a*c
	t1=0.
	t2=0.
	sol=0
	if d>0:
		sd=math.sqrt(d)
		t1=(-b-sd)/2/a
		t2=(-b+sd)/2/a
		sol=2
	elif d==0:
		t1=-b/2/a
		sol=1
	return sol,t1,t2

HUGE_VAL=1e100
def Intersec(s,o,v):
	c=np.array(s[0:3])
	rad=s[3]
	vt=o-c
	a=np.dot(v,v)
	b=2*np.dot(v,vt)
	c=np.dot(vt,vt)-rad*rad
	sol,t1,t2=SolveTri(a,b,c)
	if sol==2:
		if t1<t2:
			t=t1
		else:
			t=t2
	elif sol==1:
		t=t1
	else:
		t=HUGE_VAL
	return t

def Trace(o,v):
	tmin=HUGE_VAL
	omin=0
	for s in sphs:
		t=Intersec(s,o,v)
		if t>0 and t<tmin:
			tmin=t
			omin=s
	rr,gg,bb = 0, 0, 0
	if tmin<HUGE_VAL:
		rr, gg, bb = omin[4], omin[5], omin[6]
	return rr,gg,bb

def Render():
	for j in range(h):
		vu=u*(j-h/2)/h*hh
		for i in range(w):
			vr=r*(i-w/2)/w*ww
			v=f+vu+vr
			v/=np.linalg.norm(v)
			rr,gg,bb=Trace(e,v)
			tab[h-j-1][i]=[rr,gg,bb]

def Draw():
	for row in tab:
		for e in row:
			r, g ,b = e
			print(" %3.f,%3.f,%3.f" % (100*r,100*g,100*b),end="")
		print("")

def Draw0():
	for row in tab:
		for e in row:
			r, g ,b = e
			if r>=g and r>=b:
				if b>0:
					if g>0:
						col='W'
					else:
						col='V'
				else:
					if g>0:
						col='M'
					else:
						col='R'
			elif g>=b:
				if b>0:
					col='Y'
				else:
					col='G'
			elif b>0:
				col='B'
			else:
				col='K'
			print(e,end="")
		print("")

Render()
Draw()
