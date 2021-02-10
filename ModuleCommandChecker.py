from LoadModules import LoadModules

loadModules = LoadModules()
loadModules.loadModules()
loadModules.loadInstances()
def checkCommand(message):
    for instance in loadModules.moduleInstaces:
        try:
            instance.getEveryMessageMethod(message)  # How to check whether this exists or not
            # Method exists and was used.
        except AttributeError:
            pass
        # Method does not exist; What now?
        for name in instance.mod_commands:
            if name in message.text or name + "@szBrokenBot" in message.text:
                instance.handleOnCommand(message, name)
                break

def checkCallback(call):
    for instance in loadModules.moduleInstaces:
        for name in instance.mod_call_handler_name:
            if name == call.message.text or name == call.data:
                instance.callBackHandler(call, name)

def getActiveModNames():
    return loadModules.modulesName
def getHelpOfModule(name):
    for instance in loadModules.moduleInstaces:
            if name == instance.mod_name:
                return instance.help_mod()
