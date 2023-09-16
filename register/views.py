from django.shortcuts import render, HttpResponse, redirect
from django.urls import resolve
import json

times = 0
def register(request):
    global times
    print('Register Page Opened!')
    times += 1
    current_url = request.path
    print(current_url)
    print(0)
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    return render(request, 'register.html', {'loc':report_loc,'error': ''})
def signup(request):
    print('Register Request Made!')
    print('Reading Data from JSON')
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    json2 = open('static/user_data.json',)
    data = json.load(json2) 
    l1 = data['u_data'][0]
    emails = list(l1.keys())
    body_data = list(l1.values())
    passwords = []
    flags = []
    for password, flag in body_data:
        passwords.append(password)
        flags.append(flag)
    json2.close() 
    print('Read data from JSON')
    email = request.POST['email']
    password = request.POST['password']
    password1 = request.POST['password1']
    usernames = []
    if email not in emails:
        if password == password1:
            emails.append(email)
            passwords.append(password)
            flags.append("block")

            d4 = {emails[len(emails)-1]: [passwords[len(emails)-1], flags[len(emails)-1]]}
            for x in range(len(emails)-1):
                d4 = dict(list(d4.items()) + list({emails[x]:[passwords[x],flags[x]]}.items()))
            json_object = '{"u_data": ['+json.dumps(d4, indent = 4)+']}'
            a = open('static/user_data.json', 'w')
            a.write(json_object)
            a.close()
            times = 0
            print('Registered new user, returning HTTP response')
            return redirect('/')
        else:
            print('Passwords do not match, returning HTTP response')
            return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. The Passwords do not match.'})
    else:
        print('The Username or Email ID is already taken, returning HTTP response')
        return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. The Username or Email ID is already taken.'})