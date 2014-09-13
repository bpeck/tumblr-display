import sys, traceback

from UI.MainScreen import MainScreen

from web import Backend as WebInterface
from controllers.RootModelCommands import GetInfoCommand, SetModelTypeCommand

from models.BlogModel import BlogModel
from views.BlogView import BlogView
from controllers.BlogCrawlController import BlogCrawlController

model_map = {
    'tumblr' : [BlogModel, BlogView, BlogCrawlController]
}

class AppController(object):
    def __init__(self, app):
        self.app = app

    def setRoot(self, model, view, controller):
        self.model = model
        self.view = view
        self.controller = controller

        current_main_screen = self.app.screen_manager.getScreen('MainScreen')
        if current_main_screen:
            self.app.screen_manager.removeScreen(current_main_screen)

        try:
            new_main_screen = MainScreen()
            new_main_screen.view = self.view
            new_main_screen.onDisplayChange(self.app.screen_manager.display_screen)
            new_main_screen.insertDrawable(self.view)
            new_main_screen.addController(self.controller)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            self.app.done = True
        else:
            self.app.screen_manager.pushScreen(new_main_screen)
            self.handleCommand(GetInfoCommand())

    def handleKeyboardEvent(self, e):
        if self.controller:
            self.controller.handleKeyboardEvent(e)

    def handleMouseEvent(self, e):
        if self.controller:
            self.controller.handleMouseEvent(e)
            
    def handleCommand(self, command):
        # if it's a special command the app controller cares about, consume it here
        if isinstance(command, GetInfoCommand):
            print 'recv get info command'
            info = self.model.getInfo()
            info.update(self.view.getInfo())
            info.update(self.controller.getInfo())
            WebInterface.info_queue.put((self.model.getInfoTemplatePath(), info))

            # TODO: clear info queue if there is stale data hanging around?
        elif isinstance(command, SetModelTypeCommand):
            model_type = command.args[0]
            root_path = command.args[1]

            model_class, view_class, controller_class = None, None, None
            try:
                model_class, view_class, controller_class = model_map[model_type]
                model = model_class(root_path)
                view = view_class(model)
                controller = controller_class(view)
            except Exception:
                print "Failed to change model to [%s, %s]" % (model_type, root_path)
                return

            self.setRoot(model, view, controller)
        else:
            # otherwise, pass it down to the current root controller
            self.controller.handleCommand(command)