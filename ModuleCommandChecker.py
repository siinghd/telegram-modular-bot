from LoadModules import LoadModules

loadModules = LoadModules()
loadModules.loadModules()
loadModules.loadInstances()
def checkCommand(bot,message):
    for instance in loadModules.moduleInstaces:
        try:
            instance.getEveryMessageMethod(message, bot)  # How to check whether this exists or not
            # Method exists and was used.
        except AttributeError:
            pass
        # Method does not exist; What now?
        for name in instance.mod_name:
            if name in message.text or name + "@szBrokenBot" in message.text:
                instance.handleOnCommand(bot, message, name)

def checkCallback(bot,call):
    for instance in loadModules.moduleInstaces:
        for name in instance.mod_call_handler_name:
            if name == call.message.text:
                instance.callBackHandler(bot, call, name)