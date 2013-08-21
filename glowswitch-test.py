#Author: Jbrodin

#A simple program used to make a color-changing orb
#Requires the Panda3D game engine to run

import direct.directbase.DirectStart
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import NodePath,TextNode
from panda3d.core import Camera,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
import sys
from direct.showbase.DirectObject import DirectObject #enables sys.accept

class World(DirectObject):
    def __init__(self):

        #Load switch model
        self.glowswitch = loader.loadModel("glowswitch")
        self.sphere=self.glowswitch.find("**/sphere") #finds a subcomponent of the .egg model... sphere is the name of the sphere geometry in the .egg file
        self.glowswitch.reparentTo(render)

        base.disableMouse() #mouse-controlled camera cannot be moved within the program
        camera.setPosHpr( 0, -6.5, 1.4, 0, -2, 0)

        #Light up everything an equal amount
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.95, .95, 1.05, 1))
        render.setLight(render.attachNewNode(ambientLight))

        #Add lighting that only casts light on one side of everything in the scene
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(.2, .2, .2, .1)) #keepin it dim
        directionalLight.setSpecularColor(Vec4(0.2, 0.2, 0.2, 0.2))
        render.setLight(render.attachNewNode(directionalLight))

        #initalize sequence variable
        self.ChangeColorSeq = Sequence(Wait(.1))

        #start with blue by default
        self.changeOrbColor(.1,0,.6,.3,.2,1)
                            #^(R min, Gmin, Bmin, Rmax, Gmax, Bmax)
        
        #user controls
        #note that changing the color means it will "pulse" that color and therefore needs a range of color values
        self.accept("1", self.changeOrbColor,[.6,.1,.1,1,.3,.3]) #change orb color to red
        self.accept("2", self.changeOrbColor,[.1,.6,.1,.3,1,.3])#change orb color to green
        self.accept("3", self.changeOrbColor,[.1,0,.6,.3,.2,1]) #change orb color to blue
        self.accept("escape", sys.exit)

        instructions = OnscreenText(text="1: Change to red \n2: Change to Green \n3: Change to Blue \nEsc: Exit",
                                     fg=(1,1,1,1), pos = (-1.3, -.82), scale = .05, align = TextNode.ALeft)


    def changeOrbColor(self,Ra,Ga,Ba,Rz,Gz,Bz):
        self.ChangeColorSeq.finish() #end the last sequence
        BrightenSwitch = self.sphere.colorScaleInterval(2, Vec4(Ra,Ga,Ba,1), Vec4(Rz,Gz,Bz,1)) #the first number inside the () gives the amount of time this takes to execute
        DarkenSwitch = self.sphere.colorScaleInterval(2, Vec4(Rz,Gz,Bz,1), Vec4(Ra,Ga,Ba,1))
        self.ChangeColorSeq = Sequence(BrightenSwitch,Wait(.1),DarkenSwitch,Wait(.1))
        self.ChangeColorSeq.loop()        

   
w = World()
run()
