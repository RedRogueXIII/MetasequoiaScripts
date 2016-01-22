import MQSystem
import math
from collisionDetection import *

def drawDebugVertex(point):
	doc = MQSystem.getDocument()
	newobj = MQSystem.newObject()
	doc.addObject(newobj)
	newobj.name = "DebugVertex"
	newobj.addVertex(point)
	draw = MQSystem.newPoint(0,100,0)	
	newobj.addVertex(point + draw)
	newobj.addFace([0,1])

def drawDebugLine(points):
	doc = MQSystem.getDocument()
	newobj = MQSystem.newObject()
	doc.addObject(newobj)
	newobj.name = "DebugLine"
	newobj.addVertex(points[0])
	newobj.addVertex(points[1])
	newobj.addFace([0,1])

def drawDebugTriangle(points):
	doc = MQSystem.getDocument()
	newobj = MQSystem.newObject()
	doc.addObject(newobj)
	newobj.name = "DebugTriangle"
	newobj.addVertex(points[0])
	newobj.addVertex(points[1])
	newobj.addVertex(points[2])
	newobj.addFace([0,1,2])
	
def getMax(points):
	result = MQSystem.newPoint(points[0].x, points[0].y, points[0].z)
	for i in range(1, len(points)):
		if points[i].x > result.x:
			result.x = points[i].x
		if points[i].y > result.y:
			result.y = points[i].y
		if points[i].z > result.z:
			result.z = points[i].z
	return result

def getMin(points):
	result = MQSystem.newPoint(points[0].x, points[0].y, points[0].z)
	for i in range(1, len(points)):
		if points[i].x < result.x:
			result.x = points[i].x
		if points[i].y < result.y:
			result.y = points[i].y
		if points[i].z < result.z:
			result.z = points[i].z
	return result
	
def getCenter(points):
	minBounds = getMax(points)
	maxBounds = getMin(points)
	center = minBounds + (maxBounds - minBounds)*0.5
	print("MIN: "+str(minBounds)+" MAX: "+str(maxBounds)+" CENTER: "+str(center))
	return center

# Given a face and object return the list of all the vertices in the face
def getVertices(face, object):
	collection = []
	for i in range(0,len(face.index)):
		collection.append(object.vertex[face.index[i]])
	'''
	stringy = ""
	cheese = MQSystem.newPoint(0,0,0)
	for k in range(0,len(collection)):
		cheese += collection[k].getPos()
		stringy += str(collection[k].getPos())+", "
	print(str(cheese)+" is made of "+stringy)
	'''
	return collection

def getPoints(vColl):
	collection = []
	for i in range(0,len(vColl)):
		collection.append(vColl[i].getPos())
	return collection

def getObjectByName(name):
	doc = MQSystem.getDocument()
	for i in range(0, len(doc.object)):
		if doc.object[i].name == name:
			return doc.object[i]
	return None
	
def printVertices(object):
	string = ""
	for i in range(0, len(object.vertex)):
		string += str(object.vertex[i].getPos())
	print(string)

# Get the camera look vector.
def getCameraLookVector():
	# Find the Camera Look Vector ( Position - Target )
	doc = MQSystem.getDocument()
	aperture = doc.getScene(0)
	unit = aperture.getLookAtPos() - aperture.getCameraPos()
	unit.normalize()
	# print("LOOKING OUT MY CAMERA, WHAT DO I SEE? "+str(unit))
	return unit

# Works for Triangles, still needs breakdown quads and N-Gons to work properly
def raycastClosestPoint(start, vector, targetObject):
	#Define a line from the start and vector, and record all points of contact with the target object.
	contacts = []
	#print("Iterating through faces.")
	for i in range(0, len(targetObject.face)):		
		vCount = targetObject.face[i].numVertex
		if vCount < 3:
			#print("Face "+str(i)+" has no geometry")
			continue
		elif vCount == 3:
			#print("Face "+str(i)+" is a triangle")
			vertices = getVertices(targetObject.face[i], targetObject)
			#print("Get Vertices passed. "+str(vertices[0].getPos())+", "+str(vertices[1].getPos())+", "+str(vertices[2].getPos()))
			#print(str(start)+", "+str(vector))
			test = getIntersectPoint( vertices[0].getPos(), vertices[1].getPos(), vertices[2].getPos(), start, vector)
			if test is None: continue
			contacts.append(test)
		elif vCount > 3:
			#print("Face "+str(i)+" is unsupported")
			vertices = getVertices(targetObject.face[i], targetObject)
			tris = virtualTriangulate(vertices)
			if tris is None: continue
			for j in range(0,len(tris)):
				test = getIntersectPoint( tris[j][0], tris[j][1], tris[j][2], start, vector)
				if test is None: continue
				#print("Running test "+str(j))
				#drawDebugVertex(test)
				contacts.append(test)
				break
	if len(contacts) > 0:
	    return getClosestPoint(start, contacts)
	else:
		return None
	

	
# UNIMPLEMENETED - Given a quad or N-Gon, create a tesselated representation of the shape without changing the source geometry
def virtualTriangulate(points):
	# final triangle count will be vertexCount - 2
	triangles = []
	vertexCount = len(points)
	if vertexCount == 4:
		# Quad -> Shortest diagonal
		e1 = points[0].getPos() - points[2].getPos()
		e2 = points[1].getPos() - points[3].getPos()
		m1 = quickMagnitude(e1)
		m2 = quickMagnitude(e2)
		if m1 == m2 or m1 < m2:
			#print("Quad split method A")
			triangles.append([points[0].getPos(),points[1].getPos(),points[2].getPos()])
			triangles.append([points[0].getPos(),points[2].getPos(),points[3].getPos()])
			return triangles
		elif m1 > m2:
			#print("Quad split method B")
			triangles.append([points[0].getPos(),points[1].getPos(),points[3].getPos()])
			triangles.append([points[1].getPos(),points[2].getPos(),points[3].getPos()])
			return triangles
	else:
		# N-Gon -> Do magic.
		return None
	return None

# Non Squared magnitude value
def quickMagnitude(p1):
	return math.sqrt(p1.x**2 + p1.y**2 + p1.z**2)

# Non Squared distance value
def quickDistance(p1,p2):
	return (p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2

# Pick closest point to origin from a given set
def getClosestPoint(origin, points):
	closest = quickDistance(origin, points[0])
	iNum = 0
	for i in range (1, len(points)):
		# Calculate distance between point and origin
		calc = quickDistance(origin, points[i])
		if calc < closest:
			closest = calc
			iNum = i
	return points[iNum]

# Calculate the surface normal of a given face in the active object.
def getFaceNormal(inFace, obj):
	'''
	Calculate the face normal
	U = p2 - p1
	V = p3 - p1
	Nx = UyVz - UzVy
	Ny = UzVx - UxVz
	Nz = UxVy - UyVx
	'''
	doc = MQSystem.getDocument()
	normal = MQSystem.newPoint(0,0,0)
	U = obj.vertex[inFace.index[1]].getPos() - obj.vertex[inFace.index[0]].getPos()
	V = obj.vertex[inFace.index[2]].getPos() - obj.vertex[inFace.index[0]].getPos()

	normal.x = U.y * V.z - U.z * V.y
	normal.y = U.z * V.x - U.x * V.z
	normal.z = U.x * V.y - U.y * V.x

	normal.normalize()

	return normal * -1

# Does not account for smoothing angle limits.
def getVertexNormal(inVertex):
	# Calculate the vertex normal
	doc = MQSystem.getDocument()
	obj = doc.object[doc.currentObjectIndex]
	vertexNormal = MQSystem.newPoint(0,0,0)
	for i in inVertex.faces:
		# print( "Face " + str(i) + " is connected to vertex " + str(inVertex.id) )
		if getFaceNormal(obj.face[i], obj) is None: continue
		# print( "Face " + str(i) + " has a normal of " + str( getFaceNormal(obj.face[i])) )
		vertexNormal += getFaceNormal(obj.face[i], obj)
		# Calculate the VERTEX NORMAL HEREEEEE
	vertexNormal.normalize()
	return vertexNormal

# Get all the selected vertices in the scene
def getActiveSelectedVertices():
	doc = MQSystem.getDocument()
	pointList = []
	obj = doc.object[doc.currentObjectIndex]
	if obj is None or obj.lock == 1:
		return None
	for vi in obj.vertex:
		if vi is None: continue
		if vi.select == 1:
			# print(vi)
			pointList.append(vi)
				# Put all the vertices into an array ( as references hopefully ) then return that.
	return pointList
