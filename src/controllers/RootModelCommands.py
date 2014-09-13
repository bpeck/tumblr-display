
""" Command objects encapsulate requests from the App Controller or Web Interface to affect
a model. Controllers for root models are in charge of implementing reactions to these actions. """
class Command(object):
    def __init__(self):
        self._desc = 'generic command'
        self._args = []
    @property
    def desc(self):
        return self._desc
    @property
    def args(self):
        return self._args

class GetInfoCommand(Command):
    def __init__(self):
        super(GetInfoCommand, self).__init__()
        self._desc = 'Get Info on App State'

class NextCommand(Command):
    def __init__(self):
        super(NextCommand, self).__init__()
        self._desc = 'Next'

class PrevCommand(Command):
    def __init__(self):
        super(PrevCommand, self).__init__()
        self._desc = 'Prev'

class PauseCommand(Command):
    def __init__(self):
        super(PauseCommand, self).__init__()
        self._desc = 'Pause'

class SetModelRootCommand(Command):
    def __init__(self, model_root):
        super(SetModelRootCommand, self).__init__()
        self._desc = 'Set Model Root'
        self._args = [model_root]

class SetModelTypeCommand(Command):
    def __init__(self, model_type, model_root):
        super(SetModelTypeCommand, self).__init__()
        self._desc = 'Set Model Type'
        self._args = [model_type, model_root]