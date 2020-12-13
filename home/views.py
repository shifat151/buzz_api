from django.shortcuts import render, redirect
from .forms import loginForm, registrationForm
import json, requests, datetime
import uuid


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            payload = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password']
            }
            login_url = 'https://recruitment.fisdev.com/api/login/'
            headers = {
                'content-type': 'application/json'
            }

            r = requests.post(login_url, headers=headers, data=json.dumps(payload))
            json_data = json.loads(r.text)
            request.session['token'] = json_data['token']
            print(request.session['token'])
            return redirect('registration')
        else:
            return render(request, 'home/login.html', {'form': form})


    else:
        form = loginForm()
        return render(request, 'home/login.html', {'form': form})


def filterDictionary(registration_data):
    for key in registration_data.copy():
        if registration_data[key] == '':
            del registration_data[key]
    return registration_data

def registration(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            # create tsync_id if it does not exist in session
            if 'regid' in request.session:
                reg_id = request.session['regid']
            else:
                reg_id = str(uuid.uuid4())
            # change on_spot_creation_time to now if it does not exist in session.
            if 'creation_time' in request.session:
                on_spot_creation_time = request.session['creation_time']
            else:
                on_spot_creation_time = int(datetime.datetime.now().timestamp())
            # change on_spot_update_time
            on_spot_update_time = int(datetime.datetime.now().timestamp())

            registration_data = {
                'tsync_id': reg_id,
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'full_address': form.cleaned_data['full_address'],
                'name_of_university': form.cleaned_data['name_of_university'],
                'graduation_year': form.cleaned_data['graduation_year'],
                'cgpa': form.cleaned_data['cgpa'],
                'experience_in_months': form.cleaned_data['experience_in_months'],
                'current_work_place_name': form.cleaned_data['current_work_place_name'],
                'applying_in': form.cleaned_data['applying_in'],
                'expected_salary': form.cleaned_data['expected_salary'],
                'field_buzz_reference': form.cleaned_data['field_buzz_reference'],
                'github_project_url': form.cleaned_data['github_project_url'],
                'cv_file': {
                    'tsync_id': str(uuid.uuid4())
                },
                'on_spot_update_time': on_spot_update_time,
                'on_spot_creation_time': on_spot_creation_time
            }
            # delete a dictionary item if the subsequent form filed is left empty
            filter_reg_data=filterDictionary(registration_data)

            registration_url = 'https://recruitment.fisdev.com/api/v0/recruiting-entities/'
            headers = {
                'content-type': 'application/json',
                'Authorization': 'Token ' + request.session['token']
            }
            r = requests.post(registration_url, headers=headers, data=json.dumps(filter_reg_data))
            json_data = json.loads(r.text)
            print(r.text)
            # setting reg_id and creation_time in session in case of update the data
            request.session['regid'] = json_data['tsync_id']
            request.session['creation_time'] = json_data['on_spot_creation_time']
            request.session['cv_file_id']=json_data['cv_file']['id']

            return render(request, 'home/registration.html', {'form': form})
        else:
            return render(request, 'home/registration.html', {'form': form})
    else:
        form = registrationForm()
        return render(request, 'home/registration.html', {'form': form})
