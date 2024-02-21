from bottle import get, static_file

@get('/static/style.css')
def static_css():
    return static_file('style.css', root='app/static')