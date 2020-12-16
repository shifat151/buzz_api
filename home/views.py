from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import loginForm, registrationForm, fileUpload
import json, requests, datetime, os
import uuid, codecs
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find

media_root = settings.MEDIA_ROOT


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
            try:
                response = requests.post(login_url, headers=headers, data=json.dumps(payload))
            except:
                return render(request, 'home/login.html',
                              {'form': form, 'message': 'Something went wrong. Please try again'})
            else:
                json_data = json.loads(response.text)

            if response:
                request.session['token'] = json_data['token']
            else:
                return render(request, 'home/login.html', {'form': form, 'message': json_data['message']})

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
            filter_reg_data = filterDictionary(registration_data)

            registration_url = 'https://recruitment.fisdev.com/api/v0/recruiting-entities/'
            headers = {
                'content-type': 'application/json',
                'Authorization': 'Token ' + request.session['token']
            }

            try:
                response = requests.post(registration_url, headers=headers, data=json.dumps(filter_reg_data))
            except:
                return render(request, 'home/registration.html',
                              {'form': form, 'message': 'Something went wrong. Please try again'})
            else:
                json_data = json.loads(response.text)


            if response:
                # setting reg_id and creation_time in session in case of update the data
                request.session['regid'] = json_data['tsync_id']
                request.session['creation_time'] = json_data['on_spot_creation_time']
                request.session['cv_file_id'] = json_data['cv_file']['id']
            else:
                return render(request, 'home/registration.html', {'form': form, 'message': json_data['message']})

            return render(request, 'home/registration.html', {'form': form, 'reg_id': request.session['regid']})
        else:
            return render(request, 'home/registration.html', {'form': form})
    else:
        form = registrationForm()
        return render(request, 'home/registration.html', {'form': form})


def upload_cv(request):
    if request.method == 'POST':
        form = fileUpload(request.POST, request.FILES)
        if form.is_valid():
            cv = request.FILES['cv']
            fs = FileSystemStorage()
            filename = fs.save(str(uuid.uuid4()) + cv.name, cv)
            # uploaded_file_url = fs.url(filename)
            # uploaded_file_url = staticfiles_storage.url(filename)
            cv_file = os.path.join(media_root, filename)
            files = {'file': open(cv_file, 'rb')}

            if 'cv_file_id' in request.session:
                cv_url = 'https://recruitment.fisdev.com/api/file-object/{}/'.format(request.session['cv_file_id'])
            else:
                return redirect('registration')
            headers = {
                # 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                'Authorization': 'Token ' + request.session['token']
            }
            try:
                response = requests.put(cv_url, headers=headers, files=files)
            except:
                return render(request, 'home/file_upload.html',
                              {'form': form, 'message': 'Something went wrong. Please try again'})
            else:
                json_data = json.loads(response.text)

            if response:
                context={'form': form, 'message':'File uploaded successfully'}
            else:
                return render(request, 'home/registration.html', {'form': form, 'message': json_data['message']})

            # with open(cv_file,'rb') as fopen:
            #     q = fopen.read()
            #     print(q.decode('latin-1'))

            return render(request, 'home/file_upload.html', context)
        else:
            return render(request, 'home/file_upload.html', {'form': form})
    else:
        form = fileUpload()
        return render(request, 'home/file_upload.html', {'form': form})
