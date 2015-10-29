'''
Created on Oct 15, 2015

@author: peterp
'''
from Tkinter import *
import copy
from tkFileDialog import askopenfilename
import os

from PartProperty import *

def ConvertFileNameToRelativePath(filename):
    if filename!='':
        filenameList=filename.split('/')
        if len(filenameList)>1:
            currentWorkingDirectoryList=os.getcwd().split('/')
            atOrBelow=True
            for tokenIndex in range(min(len(filenameList),len(currentWorkingDirectoryList))):
                if filenameList[tokenIndex]!=currentWorkingDirectoryList[tokenIndex]:
                    atOrBelow=False
                    break
            if atOrBelow: tokenIndex=tokenIndex+1
            if tokenIndex > 0:
                filenameprefix=''
                for i in range(tokenIndex,len(currentWorkingDirectoryList)):
                    filenameprefix=filenameprefix+'../'
                filenamesuffix='/'.join(filenameList[tokenIndex:])
                filename=filenameprefix+filenamesuffix
    return filename

class DeviceProperties(Frame):
    def __init__(self,parent,device):
        Frame.__init__(self,parent)
        self.title = device.PartPropertyByName('type').value
        self.device=device
        self.propertyStrings=[StringVar(value=str(prop.value)) for prop in self.device.propertiesList]
        self.propertyVisible=[IntVar(value=int(prop.visible)) for prop in self.device.propertiesList]
        self.keywordVisible=[IntVar(value=int(prop.keywordVisible)) for prop in self.device.propertiesList]
        propertyListFrame = Frame(self)
        propertyListFrame.pack(side=TOP,fill=X,expand=NO)
        for p in range(len(self.device.propertiesList)):
            if not self.device.propertiesList[p].hidden:
                prop=self.device.propertiesList[p]
                propertyFrame = Frame(propertyListFrame)
                propertyFrame.pack(side=TOP,fill=X,expand=YES)
                propertyVisibleCheckBox = Checkbutton(propertyFrame,variable=self.propertyVisible[p],command=self.onPropertyVisible)
                propertyVisibleCheckBox.pack(side=LEFT,expand=NO,fill=X)
                keywordVisibleCheckBox = Checkbutton(propertyFrame,variable=self.keywordVisible[p],command=self.onKeywordVisible)
                keywordVisibleCheckBox.pack(side=LEFT,expand=NO,fill=X)
                propertyLabel = Label(propertyFrame,width=25,text=prop.description+': ',anchor='e')
                propertyLabel.pack(side=LEFT, expand=NO, fill=X)
                propertyEntry = Entry(propertyFrame,textvariable=self.propertyStrings[p])
                propertyEntry.config(width=8)
                propertyEntry.bind('<Button-1>',lambda event,arg=p: self.onMouseButton1(event,arg))
                propertyEntry.pack(side=LEFT, expand=YES, fill=X)
        rotationFrame = Frame(propertyListFrame)
        rotationFrame.pack(side=TOP,fill=X,expand=NO)
        self.rotationString=StringVar(value=str(self.device.partPicture.current.orientation))
        rotationLabel = Label(rotationFrame,text='rotation: ')
        rotationLabel.pack(side=LEFT,expand=NO,fill=X)
        Radiobutton(rotationFrame,text='0',variable=self.rotationString,value='0',command=self.onOrientationChange).pack(side=LEFT,expand=NO,fill=X)
        Radiobutton(rotationFrame,text='90',variable=self.rotationString,value='90',command=self.onOrientationChange).pack(side=LEFT,expand=NO,fill=X)
        Radiobutton(rotationFrame,text='180',variable=self.rotationString,value='180',command=self.onOrientationChange).pack(side=LEFT,expand=NO,fill=X)
        Radiobutton(rotationFrame,text='270',variable=self.rotationString,value='270',command=self.onOrientationChange).pack(side=LEFT,expand=NO,fill=X)
        Button(rotationFrame,text='toggle',command=self.onToggleRotation).pack(side=LEFT,expand=NO,fill=X)
        mirrorFrame=Frame(propertyListFrame)
        mirrorFrame.pack(side=TOP,fill=X,expand=NO)
        mirrorLabel = Label(mirrorFrame,text='mirror: ')
        mirrorLabel.pack(side=LEFT,expand=NO,fill=X)
        self.mirrorVerticallyVar=IntVar(value=int(self.device.partPicture.current.mirroredVertically))
        mirrorVerticallyCheckBox = Checkbutton(mirrorFrame,text='Vertically',variable=self.mirrorVerticallyVar,command=self.onOrientationChange)
        mirrorVerticallyCheckBox.pack(side=LEFT,expand=NO,fill=X)
        self.mirrorHorizontallyVar=IntVar(value=int(self.device.partPicture.current.mirroredHorizontally))
        mirrorHorizontallyCheckBox = Checkbutton(mirrorFrame,text='Horizontally',variable=self.mirrorHorizontallyVar,command=self.onOrientationChange)
        mirrorHorizontallyCheckBox.pack(side=LEFT,expand=NO,fill=X)
        partPictureFrame = Frame(self)
        partPictureFrame.pack(side=TOP,fill=BOTH,expand=YES)
        self.partPictureCanvas = Canvas(partPictureFrame)
        self.partPictureCanvas.config(relief=SUNKEN,borderwidth=1)
        self.partPictureCanvas.pack(side=TOP,fill=BOTH,expand=YES)
        self.partPictureCanvas.bind('<Button-1>',self.onMouseButton1InPartPicture)
        device.DrawDevice(self.partPictureCanvas,20,-device.partPicture.current.origin[0]+5,-device.partPicture.current.origin[1]+5)

    def onToggleRotation(self):
        self.device.partPicture.current.Rotate()
        self.rotationString.set(str(self.device.partPicture.current.orientation))
        self.onOrientationChange()

    def onOrientationChange(self):
        self.device.partPicture.current.ApplyOrientation(self.rotationString.get(),bool(self.mirrorHorizontallyVar.get()),bool(self.mirrorVerticallyVar.get()))
        self.partPictureCanvas.delete(ALL)
        self.device.DrawDevice(self.partPictureCanvas,20,-self.device.partPicture.current.origin[0]+5,-self.device.partPicture.current.origin[1]+5)

    def onMouseButton1InPartPicture(self,event):
        numPictures=len(self.device.partPicture.partPictureClassList)
        current=self.device.partPicture.partPictureSelected
        origin=self.device.partPicture.current.origin
        selected=current+1
        if selected >= numPictures:
            selected = 0
        self.device.partPicture.SwitchPartPicture(selected)
        self.device.partPicture.current.SetOrigin(origin)
        self.partPictureCanvas.delete(ALL)
        self.device.DrawDevice(self.partPictureCanvas,20,-self.device.partPicture.current.origin[0]+5,-self.device.partPicture.current.origin[1]+5)

    def onPropertyVisible(self):
        for p in range(len(self.device.propertiesList)):
            self.device.propertiesList[p].visible=bool(self.propertyVisible[p].get())
        self.partPictureCanvas.delete(ALL)
        self.device.DrawDevice(self.partPictureCanvas,20,-self.device.partPicture.current.origin[0]+5,-self.device.partPicture.current.origin[1]+5)

    def onKeywordVisible(self):
        for p in range(len(self.device.propertiesList)):
            self.device.propertiesList[p].keywordVisible=bool(self.keywordVisible[p].get())
        self.partPictureCanvas.delete(ALL)
        self.device.DrawDevice(self.partPictureCanvas,20,-self.device.partPicture.current.origin[0]+5,-self.device.partPicture.current.origin[1]+5)

    def onMouseButton1(self,event,arg):
        print 'entry clicked',arg
        if self.device.propertiesList[arg].propertyName == PartPropertyFileName().propertyName:
            extension='.s'+str(self.device['ports'].value)+'p'
            filename=askopenfilename(filetypes=[('s-parameters', extension)])
            filename=ConvertFileNameToRelativePath(filename)
            self.propertyStrings[arg].set(filename)
        elif self.device.propertiesList[arg].propertyName == PartPropertyWaveformFileName().propertyName:
            extension='.txt'
            filename=askopenfilename(filetypes=[('waveforms', extension)])
            filename=ConvertFileNameToRelativePath(filename)
            self.propertyStrings[arg].set(filename)

class DevicePropertiesDialog(Toplevel):
    def __init__(self,parent,device):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.device = device

        self.title('Add '+device['description'].value)

        self.parent = parent

        self.result = None

        self.DeviceProperties = DeviceProperties(self,device)
        self.initial_focus = self.body(self.DeviceProperties)
        self.DeviceProperties.pack(side=TOP,fill=BOTH,expand=YES,padx=5, pady=5)

        self.buttonbox()

        #self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):
        self.result=copy.deepcopy(self.device)
        for p in range(len(self.device.propertiesList)):
            self.result.propertiesList[p].value=self.DeviceProperties.propertyStrings[p].get()
            self.result.propertiesList[p].visible=bool(self.DeviceProperties.propertyVisible[p].get())