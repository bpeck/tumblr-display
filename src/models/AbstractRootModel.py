""" A common interface that any model that will be put up on display must implement """
class AbstractRootModel(object):
    def getName(self):
        raise NotImplementedError()

    """ All root models have some root path,
    e.g. name of tumblr account, url of imgur album """
    def getRootPath(self):
        raise NotImplementedError()

    """ Get current info describing the internal state of the model. Used
    by the Web Interface 
    @return a dictionary of information, caller is in charge of formatting"""
    def getInfo(self):
        raise NotImplementedError()

    """ Get the name of the file that contains the html template for this
    model's info
    @return a string that is a path relative to the Web Interface's templates dir"""
    def getInfoTemplatePath(self):
        raise NotImplementedError()
