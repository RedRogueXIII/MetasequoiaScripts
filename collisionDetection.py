# Script Description
#---------------------------
# This script is for collision detection functions.

# Metadata
#---------------------------
# Author: RedRogueXIII (Michael Cecconet)
# Contact: red_rogue_xiii@hotmail.com
# Website: https://github.com/RedRogueXIII/MetasequoiaScripts
# Version Date: July 7, 2016

import MQSystem

#r2 is direction, r1 is origin
def intersectTest( p0, p1, p2, r1, r2):
	#drawDebugTriangle(p0,p1,p2, "lolol")
	if r1 is None or r2 is None:
		#print("Invalid ray.")
		return None
	e1 = p1 - p0
	e2 = p2 - p0
	#print("E1: "+str(e1)+", E2: "+str(e2))
	g = r2.crossProduct(e2)
	a = e1.dotProduct(g)
	#print("G: "+str(g)+", A: "+str(a))
	if a == 0:
		return None
	f = 1/a
	s = r1 - p0
	#print("F: "+str(f)+", S: " + str(s))
	u = f*(s.dotProduct(g))
	if u < 0.0 or u > 1.0:
		#print("U is outside, " + str(u))
		return None
	q = s.crossProduct(e1)
	#print("G: "+str(q))
	v = f*(r2.dotProduct(q))
	if v < 0.0 or v + u > 1.0:
		#print("V is outside, " + str(v))
		return None
	t = f*e2.dotProduct(q)
	#print("U = "+str(u)+ " V = "+str(v)+ " T = "+str(t))
	return MQSystem.newPoint(u,v,t)
	#Only one direction ray? I want both
	'''
	if t <= 0:
		return MQSystem.newPoint(u,v,t)
	else:
		return None
	'''

def doesIntersect( p0, p1, p2, r1, r2):
	result = intersectTest( p0, p1, p2, r1, r2)
	if result is None:
		return False
	else:
		return True;
		
def getIntersectPoint( p0, p1, p2, r1, r2):
	result = intersectTest( p0, p1, p2, r1, r2)
	if result is None:
		return None
	else:
		return uvToPoint( result.x, result.y, result.z, p0, p1, p2)
		
def uvToPoint(u,v,t,v1,v2,v3):
	tri = ( 1-u-v)*v1+u*v2+v*v3
	#print("Contact Point: "+str(tri))
	return tri


def drawDebugPoint(point, debugObjName):
	doc = MQSystem.getDocument()
	obj = MQSystem.newObject()
	obj.name = debugObjName
	obj.addVertex(0,0,0)
	obj.addVertex(point)
	obj.addFace([0,1])
	doc.addObject(obj)

def drawDebugTriangle( p1, p2, p3, debugObjName):
	doc = MQSystem.getDocument()
	obj = MQSystem.newObject()
	obj.name = debugObjName
	obj.addVertex(p1)
	obj.addVertex(p2)
	obj.addVertex(p3)
	obj.addFace([0,1,2])
	doc.addObject(obj)
