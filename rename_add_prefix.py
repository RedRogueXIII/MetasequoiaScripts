def applyPrefix( prefix, name):
	test = name.find(prefix)
	if test == -1 or test != 0:
		name = prefix + name
	return name
	
class renamePrefixDialog(MQWidget.Dialog):

	def __init__(self, parent):
		MQWidget.Dialog.__init__(self, parent)
		
		self.title = "Add Prefix to Selected Objects"
		
		self.frame0 = self.createHorizontalFrame(self)
		
		self.label = MQWidget.Label(self.frame0)
		self.label.text = "Prefix:"
		
		self.pText = MQWidget.Edit(self.frame0)
		self.pText.text = ""
		
		self.plabel = MQWidget.Label(self.frame0)
		self.plabel.text = "Recursive:"
		
		self.rCheck = MQWidget.CheckBox(self.frame0)
		self.rCheck.checked = 1
		
		self.frame1 = self.createHorizontalFrame(self)
		self.frame1.uniformSize = True

		self.okbtn = MQWidget.Button(self.frame1)
		self.okbtn.text = MQSystem.getResourceString("OK")
		self.okbtn.modalResult = "ok"
		self.okbtn.default = 1
		self.okbtn.fillBeforeRate = 1
		self.cancelbtn = MQWidget.Button(self.frame1)
		self.cancelbtn.text = MQSystem.getResourceString("Cancel")
		self.cancelbtn.modalResult = "cancel"
		self.cancelbtn.default = 1
		self.cancelbtn.fillAfterRate = 1

# for all objects that are selected , rename them with prefix.
# if recursive is on, rename their children objects too.


dlg = renamePrefixDialog(MQWidget.getMainWindow())

if dlg.execute() == "ok":	
	recursiveApply = dlg.rCheck.checked
	prefix = dlg.pText.text
	if prefix[len(prefix) - 1] != '_':
		prefix += '_'	
	doc = MQSystem.getDocument()
	for i in range(0, len(doc.object)):
		if doc.object[i] is None: continue
		if doc.object[i].select == 1:
			doc.object[i].name = applyPrefix(prefix, doc.object[i].name)
			if recursiveApply == 1:
				for k in range(i, len(doc.object)):
					if doc.object[k] is None: continue
					if doc.isAncestorObject(  doc.object[i], doc.object[k]):
						doc.object[k].name = applyPrefix(prefix, doc.object[k].name)
				
		'''		
		currentObj.name = applyPrefix(prefix, currentObj.name)
		if recursiveApply == 1:
			chd = doc.getChildObjectCount(doc.object[i])
			for j in range(0, chd):				
				childObj = doc.getChildObject( doc.object[i] , j )
				childObj.name = applyPrefix(prefix, childObj.name)
		'''
