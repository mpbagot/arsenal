#! /usr/bin/env python3
from tornado.ncss import Server
from template_language.parser import render_template
from parser import SVGParser

def index_handler(request):
    '''
    Handle the index page
    '''
    html = render_template('index.html', { 'title':'Index Page', 'user' : None,
                                        "tutorials" : []
                                        })
    request.write(html)

def tutorial_handler(request, tutorialId):
    '''
    Serve the Tutorial content
    '''
    tutorial = None
    html = render_template('tutorial.html', { 'title':tutorial.title, 'user' : None,
                                        "tutorial" : None
                                        })
    request.write(html)

def tutorials_handler(request):
    '''
    Handle the tutorials page
    '''
    html = render_template('tutorials.html', { 'title':'Tutorial Index', 'user' : None,
                                        "units" : []
                                        })
    request.write(html)

def flagged_handler(request):
    '''
    Handle the flagged tutorials page
    '''
    html = render_template('flagged.html', { 'title':'Flagged Tutorials', 'user' : None,
                                             'flag_tutors' : user.getFlaggedTutorials()
                                            })
    request.write(html)

def checker_handler(request):
    '''
    Handle the SVG Checker page
    '''
    html = render_template('checker.html', { 'title':'SVG Checker', 'user' : None})
    request.write(html)

def upload_handler(request):
    '''
    Handle the AJAX post request
    '''
    method = request.request.method
    if method != "POST":
        request.redirect('/svgchecker')
    elif method == "POST":
        user = None
        # if user is None:
        #     request.write(render_template('login_required.html', {'title': 'Please Login', 'user' : None, 'required' : True}))
        #     return
        fileTuple = request.get_file('laser_img')
        print(fileTuple)
        fileData = fileTuple[-1]
        fileName = fileTuple[0]#+'.svg'
        with open('static/img/tmp_upload/'+fileName, 'wb') as f:
            f.write(fileData)
        fileData = fileData.decode()
        parser = SVGParser(fileData)
        parser.evaluate()
        request.write(render_template('result.html', {'title': 'SVG Scan Results', 'user' : None,
                                      'result' : parser.result, 'image' : 'static/img/tmp_upload/'+fileName}))

def login_handler(request):
    '''
    Handle the login page.
    '''
    request.write(render_template('login_required.html', {'title':'Login', 'user':None, 'required':False}))

def http404_handler(request):
    '''
    Handle a 404 page request
    '''
    html = render_template('404.html', {'title':'Error 404', 'user' : None})
    request.write(html)

# Initialise the server
server = Server(hostname='0.0.0.0', port=80)
# Add the URL listners here
server.register(r'/', index_handler)
server.register(r'/tutorials', tutorials_handler)
server.register(r'/flagged', flagged_handler)
server.register(r'/svgchecker', checker_handler)
server.register(r'/tutorial/([0-9]+)', tutorial_handler)
server.register(r'/upload', upload_handler)
server.register(r'/login', login_handler)
server.register(r'/.+', http404_handler)

# Run the server
server.run()
