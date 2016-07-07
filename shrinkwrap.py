# Script Description
#---------------------------
# This script is for projecting vertices onto existing geometric surfaces.
# It requires multiple Metasequoia objects to works, from the current active Metasequoia object it projects the selected vertices onto a second target object's geometry.
# It offers different projection options, (X,Y,Z, Camera View, Custom Vector, and Per Vertex)
# X, Y, Z, Camera View, Custom Vector only project all selected vertices along a single straight direction specified to the closest point of the target geometry.
# Per-Vertex option projects per vertice by the vertex normal, so it wraps geometry instead. 


# Metadata
#---------------------------
# Author: RedRogueXIII (Michael Cecconet)
# Contact: red_rogue_xiii@hotmail.com
# Website: https://github.com/RedRogueXIII/MetasequoiaScripts
# Version Date: July 7, 2016

# TODO
#---------------------------
# Fix Quadrilateral triangulation scheme to match Metasequoia default.
# No support for N-Gons yet.
# Ideally change from Dialog to Window so that camera can be adjusted before committing changes.
# Does not account for subdivision, mirror, or lathe modifiers, only existing geometry. 

from scriptUtilities import *
import timeit

class VectorSelectDialog(MQWidget.Dialog):

	def vectorModeChangedCallback(self,sender):
		self.XBAWKS.enabled = False
		self.YBAWKS.enabled = False
		self.ZBAWKS.enabled = False

		if self.WHERE.currentIndex == 0:
			#print ("Picked X Axis Option")
			self.myDisplayVector = MQSystem.newPoint(1,0,0)
		elif self.WHERE.currentIndex == 1:
			#print ("Picked Y Axis Option")
			self.myDisplayVector = MQSystem.newPoint(0,1,0)
		elif self.WHERE.currentIndex == 2:
			#print ("Picked Z Axis Option")
			self.myDisplayVector = MQSystem.newPoint(0,0,1)
		elif self.WHERE.currentIndex == 3:
			#print ("Picked Camera View Option")
			self.myDisplayVector = getCameraLookVector()
		elif self.WHERE.currentIndex == 4:
			#print ("Picked Custom Vector Option")
			self.myDisplayVector = self.myCustomVector
			self.XBAWKS.enabled = True
			self.YBAWKS.enabled = True
			self.ZBAWKS.enabled = True
		elif self.WHERE.currentIndex == 5:
			#print ("Picked Per-Vertex Option")
			self.myDisplayVector = MQSystem.newPoint(0,0,0)

		self.XBAWKS.text = str(self.myDisplayVector.x)
		self.YBAWKS.text = str(self.myDisplayVector.y)
		self.ZBAWKS.text = str(self.myDisplayVector.z)

	def customVectorChangedCallback(self,sender):
		self.myCustomVector.x = float(self.XBAWKS.text)
		self.myCustomVector.y = float(self.YBAWKS.text)
		self.myCustomVector.z = float(self.ZBAWKS.text)

	def targetObjectChangedCallback(self,sender):
		doc = MQSystem.getDocument()
		for n in range( 0, doc.numObject):
			#print("TESTING "+doc.object[n].name + " against " + self.TARGET.getItem(self.TARGET.currentIndex) )
			if doc.object[n] is None: continue
			if doc.object[n].name == self.TARGET.getItem(self.TARGET.currentIndex):
				pos = n
				break
		self.TargetObject = doc.object[pos]

	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)

		doc = MQSystem.getDocument()
		activeObj = doc.currentObjectIndex

		self.title = "Shrinkwrap Baybi"

		self.frame0 = self.createHorizontalFrame(self)

		self.label = MQWidget.Label(self.frame0)
		self.label.text = "Raycast Vector Direction:"

		self.WHERE = MQWidget.ComboBox(self.frame0)
		self.WHERE.addItem("X Axis")
		self.WHERE.addItem("Y Axis")
		self.WHERE.addItem("Z Axis")
		self.WHERE.addItem("Camera view")
		self.WHERE.addItem("Custom")
		self.WHERE.addItem("Per-Vertex Normal")

		self.WHERE.addChangedEvent(self.vectorModeChangedCallback)

		self.frame1 = self.createHorizontalFrame(self)
		self.frame1.uniformSize = True

		self.myCustomVector = MQSystem.newPoint(1,0,0)
		self.myDisplayVector = self.myCustomVector

		self.cDirLabel = MQWidget.Label(self.frame1)
		self.cDirLabel.text = "Vector ( X Y Z ):"
		self.XBAWKS = MQWidget.Edit(self.frame1)
		self.YBAWKS = MQWidget.Edit(self.frame1)
		self.ZBAWKS = MQWidget.Edit(self.frame1)

		self.XBAWKS.numeric = "double"
		self.YBAWKS.numeric = "double"
		self.ZBAWKS.numeric = "double"

		self.XBAWKS.text = str(self.myDisplayVector.x)
		self.YBAWKS.text = str(self.myDisplayVector.y)
		self.ZBAWKS.text = str(self.myDisplayVector.z)

		self.XBAWKS.enabled = False
		self.YBAWKS.enabled = False
		self.ZBAWKS.enabled = False

		self.XBAWKS.addChangedEvent(self.customVectorChangedCallback)
		self.YBAWKS.addChangedEvent(self.customVectorChangedCallback)
		self.ZBAWKS.addChangedEvent(self.customVectorChangedCallback)

		self.frame3 = self.createHorizontalFrame(self)
		self.frame3.uniformSize = True

		self.TargetObject = MQSystem.newObject()

		self.labelTarget = MQWidget.Label(self.frame3)
		self.labelTarget.text = "Select Target Object : "
		self.TARGET = MQWidget.ComboBox(self.frame3)
		# Populate TARGET with list of all Objects in the scene.
		for n in range( 0, doc.numObject):
			obj = doc.object[n]
			if obj is None: continue
			if n != activeObj:
				self.TARGET.addItem(obj.name)

		self.TARGET.addChangedEvent(self.targetObjectChangedCallback)

		self.frame2 = self.createHorizontalFrame(self)
		self.frame2.uniformSize = True

		self.okbtn = MQWidget.Button(self.frame2)
		self.okbtn.text = MQSystem.getResourceString("OK")
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.cancelbtn = MQWidget.Button(self.frame2)
		self.cancelbtn.text = MQSystem.getResourceString("Cancel")
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.default = 1
		self.cancelbtn.fillAfterRate = 1

# ----------------------------------------------------------------

dlg = VectorSelectDialog(MQWidget.getMainWindow())

if dlg.execute() == "ok":
	start = timeit.timeit()
	#print("Attempting to run: "+dlg.WHERE.getItem(dlg.WHERE.currentIndex)+str(dlg.myDisplayVector))
	ray = dlg.myDisplayVector
	ray.normalize()
	#print("RAY: "+str(ray))
	doc = MQSystem.getDocument()
	verts = getActiveSelectedVertices()
	if verts is None:
		print("No active vertices selected.")
	else:
		if dlg.WHERE.currentIndex == 5:
			#print("Rays are vertex normals")
			newPos = [None] * len(verts)
			for i in range(0,len(verts)):
				result = raycastClosestPoint(verts[i].getPos(), getVertexNormal(verts[i]), dlg.TargetObject)
				if result is None: continue
				newPos[i] = result
			# Cannot move vertices immediately because other vertex normal calculations rely on original positioning.
			for j in range(0,len(newPos)):
				if newPos[j] is None: continue
				verts[j].setPos(newPos[j])

		elif dlg.WHERE.currentIndex > -1 and dlg.WHERE.currentIndex < 5:
			#print("Use single ray vector")
			for i in range(0,len(verts)):
				#print("Testing Ray direction "+str(ray)+", origin "+str(verts[i].getPos()))
				result = raycastClosestPoint(verts[i].getPos(), ray, dlg.TargetObject)
				if result is None: continue
				verts[i].setPos(result)

		else:
			print("Unexpected Error "+str(dlg.WHERE.currentIndex) )
	end = timeit.timeit()
	print(end - start)
	# Calculate raycasts per vertex

	# Move vertices to closest hit
