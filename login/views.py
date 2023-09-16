from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import json
import login.files_creation as files_creation

times = 0


def login(request):
    if request.session.has_key('email'):
        del request.session['email']
    global times
    print('Login Page Opened!')
    times += 1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else: report_loc = 'signin/'
    return render(request, 'login.html', {'loc':report_loc,'error': ''})


def signin(request):
    print('Login Request Made!')
    print('Reading Data from JSON')
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
    global times
    times = times+1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else: report_loc = '../signin/'
    email = request.POST['email']
    password = request.POST['password']
    if email == "admin09801@gmail.com":
        if "Johnsons#3412" == password:
            request.session['email'] = email
            times = 0
            print('Logged in User, returning HTTP response')
            return redirect('user_table')
    if email in emails:
        if passwords[emails.index(email)] == password and flags[emails.index(email)] == "pass":
            request.session['email'] = email
            times = 0
            global check
            check = 1
            print('Logged in User, returning HTTP response')
            return redirect('dropbox_upload')
        else:
            print('Email != Password, returning HTTP response')
            return render(request, 'login.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. The Email and Password do not match.'})
    else:
        print('Account does not exist, returning HTTP response')
        return render(request, 'login.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. No such account exists. Consider signing up!'})


def dropbox_upload(request):
    if request.session.has_key('email'):
        if request.method == 'POST':
            jobNumber = request.POST.get('jobNumber')
            jobDescription = request.POST.get('jobDescription')
            address = request.POST.get('address')
            dateOfWorks = request.POST.get('dateOfWorks')
            duration = request.POST.get('duration')
            localHospital = request.POST.get('localHospital')

            if files_creation.main(jobNumber, jobDescription, address, dateOfWorks, duration, localHospital):
                status_message = "Uploaded successfully"  # Replace with actual status
                return JsonResponse({'status_message': status_message})
            else:
                status_message = "Uploading failed"  # Replace with actual status
                return JsonResponse({'status_message': status_message})

        return render(request, 'dropboxupload.html')
    else:
        return redirect('/')


def user_table(request):
    with open('static/user_data.json', 'r') as json_file:
        data = json.load(json_file)
    users = []

    for email, body_data in data['u_data'][0].items():
        users.append({
            'email': email,
            'password': body_data[0],
            'admin_flag': body_data[1]  # Initialize admin_flag as empty for now
        })

    return render(request, 'users_table.html', {'users': users})


def update_user(request, email):
    if request.method == 'POST':
        admin_flag = request.POST['admin_flag']
        # Update the 'users.json' file with the new admin flag
        with open('static/user_data.json', 'r') as json_file:
            data = json.load(json_file)
        data['u_data'][0][email][1] = admin_flag
        with open('static/user_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return redirect('user_table')  # Redirect back to the user table
    else:
        # Display a form to update the admin flag
        with open('static/user_data.json', 'r') as json_file:
            data = json.load(json_file)
        admin_flag = data['u_data'][0].get(email, '')[1]
        return render(request, 'update_user.html', {'email': email, 'admin_flag': admin_flag})


def delete_user(request, email):
    # Delete the user from the 'users.json' file
    with open('static/user_data.json', 'r') as json_file:
        data = json.load(json_file)
    if email in data['u_data'][0]:
        del data['u_data'][0][email]
        with open('static/user_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    return redirect('user_table')  # Redirect back to the user table

