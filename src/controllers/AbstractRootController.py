""" A common interface for any controller that will affect a root model """
class AbstractRootController(object):
    """ Handle a command object. Could be sent internally from AppController, or
    from the Web Interface
    @arg command """
    def handleCommand(self, command):
        raise NotImplementedError()

    """ Get current info describing the internal state of the model. Used
    by the Web Interface 
    @return a dictionary of information, caller is in charge of formatting"""
    def getInfo(self):
        raise NotImplementedError()

    def handleKeyboardEvent(self, e):
        pass

    def handleMouseEvent(self, e):
        pass