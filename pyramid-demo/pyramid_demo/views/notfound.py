from pyramid.view import notfound_view_config

@notfound_view_config(renderer='pyramid_demo:templates/components/404.pt')
def notfound_view(request):
    request.response.status = 404
    return {}
