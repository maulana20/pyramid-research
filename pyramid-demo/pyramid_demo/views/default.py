from pyramid.view import view_config

class Default:
    def __init__(self, request):
        self.request = request
    
    @view_config(route_name='home', renderer='pyramid_demo:templates/home/index.pt')
    def index(self):
        return { 'project': 'pyramid_demo' }

