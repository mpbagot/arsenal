#! /usr/bin/env python3
from tornado.ncss import Server
from template_language.parser import render_template
from svg_parser import SVGParser
from db import *

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
    method = request.request.method
    if method == 'GET':
        request.write(render_template('login_required.html', {'title':'Login', 'user':None, 'required':False, 'error':''}))
    elif method == 'POST':
        print('form returned')
        # login the user if everything is good
        # And return the cookie to be saved back to them
        username = request.get_field('name')
        password = request.get_field('pass')
        test_user = User(username, password)
        user = User.getByName(username)
        if user and user.password == test_user.password:
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect(r'/')
        else:
            error = 'User Not Found!' if not user else 'Password Incorrect!'
            request.write(render_template('login_required.html', {'title':'Login', 'user':None,
                                                'required':False, 'error':error}))

def signup_handler(request):
    '''
    Handle the signup of new users
    '''
    method = request.request.method
    if method == 'GET':
        request.write(render_template('signup.html', {'title':'Sign up', 'user':None, 'error':''}))
    elif method == 'POST':
        # Add the new user if everything checks out and log them in
        # then redirect to /
        password = request.get_field('pass')
        password_confirm = request.get_field('pass_confirm')
        username = request.get_field('name')
        class_password = request.get_field('class_pass')
        # Grab the user they want to be to check it doesn't already exist
        test_user = User.getByName(username)

        if not password == password_confirm:
            # Return passwords do not match error
            error = 'Passwords do NOT match!'
        elif not Class.getByPassword(class_password):
            # Class password invalid error
            error = 'Class password is invalid!'
        elif test_user:
            # User already exists error
            error = 'A user already exists with that name!'
        else:
            users_class = Class.getByPassword(class_password)
            is_teacher = users_class.id == 1
            user = User(username, password, current_class=users_class.id, is_teacher=is_teacher)
            user.save()
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect(r'/')
            return
        request.write(render_template('signup.html', {'title':'Sign up', 'user':None, 'error':error}))

def not_logged_in_handler(request):
    '''
    Handle the forced login page
    '''
    request.write(render_template('login_required.html', {'title':'Login', 'user':None, 'required':True, 'error':''}))

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
