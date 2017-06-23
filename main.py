#! /usr/bin/env python3
from tornado.ncss import Server
from template_language.parser import render_template

def index_handler(request):
    '''
    Handle the index page
    '''
    m = render_template('index.html', { 'title':'Index Page', 'user' : None,
                                        "tutorials" : []
                                        })
    request.write(m)

def tutorial_handler(request, tutorialId):
    '''
    Serve the Tutorial content
    '''
    request.write('tutorial content')

def tutorials_handler(request):
    '''
    Handle the tutorials page
    '''
    request.write('tutorials')

def flagged_handler(request):
    '''
    Handle the flagged tutorials page
    '''
    request.write('flagged')

def checker_handler(request):
    '''
    Handle the SVG Checker page
    '''
    request.write('SVG Checker')

def http404_handler(request):
    '''
    Handle a 404 page request
    '''
    request.write('You suck.')

# Initialise the server
server = Server(hostname='0.0.0.0', port=80)
# Add the URL listners here
server.register(r'/', index_handler)
server.register(r'/tutorials', tutorials_handler)
server.register(r'/flagged', flagged_handler)
server.register(r'/svgchecker', checker_handler)
server.register(r'/tutorial/([0-9]+)', tutorial_handler)
server.register(r'/.+', http404_handler)

# Run the server
server.run()
