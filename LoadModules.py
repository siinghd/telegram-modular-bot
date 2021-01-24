import os
import importlib
class LoadModules:
    modulesloaded={}
    modulesName=[]
    moduleInstaces = []
    def __init__(self):
        self.files=os.listdir("Modules")


    def loadModules(self):
        for file in self.files:
            modName= file[:-3]
            PLUG_NAME= f"Modules.{modName}"
            if "Mod_" in PLUG_NAME:
                self.modulesloaded[modName]=importlib.import_module(PLUG_NAME)

    def loadInstances(self):
        for module in self.modulesloaded:
            this_class = getattr(self.modulesloaded[module], module)
            self.moduleInstaces.append(this_class())


    def printModules(self):
        pass