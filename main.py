#! /usr/bin/env python3
from tornado.ncss import Server
from template_language.parser import render_template
from parser import SVGParser

def isLoggedIn(function):
    def decorated_function(request):
        user_id = request.get_secure_cookie('user_id')
        if user_id and User.get(int(user_id)):
            return function(request)
        global not_logged_in_handler
        print('redirecting to login')
        return not_logged_in_handler(request)
    return decorated_function

def get_login_user(request):
    user_id = request.get_secure_cookie('user_id')
    return User.get(int(user_id))

@isLoggedIn
def index_handler(request):
    '''
    Handle the index page
    '''
    user = get_login_user(request)
    html = render_template('index.html', { 'title':'Index Page', 'user' : user,
                                        "tutorials" : []
                                        })
    request.write(html)

@isLoggedIn
def tutorial_handler(request, tutorialId=1):
    '''
    Serve the Tutorial content
    '''
    tutorial = Tutorial.get(int(tutorialId))
    user = get_login_user(request)
    html = render_template('tutorial.html', { 'title':tutorial.title, 'user' : user,
                                        "tutorial" : tutorial
                                        })
    request.write(html)

@isLoggedIn
def tutorials_handler(request):
    '''
    Handle the tutorials page
    '''
    user = get_login_user(request)
    html = render_template('tutorials.html', { 'title':'Tutorial Index', 'user' : user,
                                        "units" : []
                                        })
    request.write(html)

@isLoggedIn
def flagged_handler(request):
    '''
    Handle the flagged tutorials page
    '''
    user = get_login_user(request)
    html = render_template('flagged.html', { 'title':'Flagged Tutorials', 'user' : user,
                                             'flag_tutors' : user.getFlaggedTutorials()
                                            })
    request.write(html)

@isLoggedIn
def checker_handler(request):
    '''
    Handle the SVG Checker page
    '''
    user = get_login_user(request)
    html = render_template('checker.html', { 'title':'SVG Checker', 'user' : user})
    request.write(html)

@isLoggedIn
def upload_handler(request):
    '''
    Handle the AJAX post request
    '''
    method = request.request.method
    if method != "POST":
        request.redirect('/svgchecker')
    elif method == "POST":
        user = get_login_user(request)
        fileTuple = request.get_file('laser_img')
        fileData = fileTuple[-1].decode()
        fileName = str(user.id)+'.svg'
        with open('static/img/tmp_upload/'+fileName, 'wb') as f:
            f.write(fileData.encode())
        parser = SVGParser(fileData)
        parser.evaluate()
        request.write(render_template('result.html', {'title': 'SVG Scan Results', 'user' : user,
                                      'result' : parser.result, 'image' : 'static/img/tmp_upload/'+fileName}))

def login_handler(request):
    '''
    Handle the login page.
    '''
    request.write(render_template('login_required.html', {'title':'Login', 'user':None, 'required':False}))

def signup_handler(request):
    '''
    Handle the signup of new users
    '''
    request.write(render_template('signup.html', {'title':'Sign up', 'user':None}))

def not_logged_in_handler(request):
    '''
    Handle the forced login page
    '''
    request.write(render_template('login_required.html', {'title':'Login', 'user':None, 'required':True}))

@isLoggedIn
def http404_handler(request):
    '''
    Handle a 404 page request
    '''
    user = get_login_user(request)
    html = render_template('404.html', {'title':'Error 404', 'user' : user})
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
server.register(r'/signup', signup_handler)
server.register(r'/.+', http404_handler)

# Run the server
server.run()
