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


def registration(request):

    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            if 'regid' in request.session:
                reg_id = request.session['regid']
            else:
                reg_id = str(uuid.uuid4())

            if 'creation_time' in request.session:
                on_spot_creation_time = request.session['creation_time']
            else:
                on_spot_creation_time = int(datetime.datetime.now().timestamp())
            on_spot_update_time = int(datetime.datetime.now().timestamp())
            # print(on_spot_creation_time)

            # payload = {
            #     'time': on_spot_update_time
            # }
            # data = json.dumps(payload)
            # print(data)

            # CVID = {
            #     'tsync_id': str(uuid.uuid4())
            # }
            # payload = {
            #     'cv_file': CVID
            # }
            # print(json.dumps(payload))
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
                'cv_file':{
                    'tsync_id': str(uuid.uuid4())
                },
                'on_spot_update_time': on_spot_update_time,
                'on_spot_creation_time': on_spot_creation_time
            }

            registration_url = 'https://recruitment.fisdev.com/api/v0/recruiting-entities/'
            # print(request.session['token'])
            headers = {
                'content-type': 'application/json',
                'Authorization': 'Token ' + request.session['token']
            }
            r = requests.post(registration_url, headers=headers, data=json.dumps(registration_data))
            json_data = json.loads(r.text)
            request.session['regid'] = json_data['tsync_id']
            request.session['rcreation_time'] = json_data['on_spot_creation_time']
            print(r.text)
            return render(request, 'home/registration.html', {'form': form})
        else:
            return render(request, 'home/registration.html', {'form': form})
    else:
        form = registrationForm()
        return render(request, 'home/registration.html', {'form': form})
