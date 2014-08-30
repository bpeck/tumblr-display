""" A common interface for any view that will display a root model """
class AbstractRootView(object):
    """ Get current info describing the internal state of the model. Used by
    the Web Interface.
    @return a dictionary of information, caller is in charge of formatting"""
    def getInfo(self):
        raise NotImplementedError()
