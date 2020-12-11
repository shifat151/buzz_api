from django.shortcuts import render
from . forms import loginForm
import json, requests

# Create your views here.
def login(request):
    if request.method=='POST':
        form = loginForm(request.POST)
        if form.is_valid():
            payload={
                'username':form.cleaned_data['username'],
                'password':form.cleaned_data['password']
            }
            data = json.dumps(payload)
            login_url='https://recruitment.fisdev.com/api/login/'
            headers={
                'content-type': 'application/json'
            }
            r = requests.post(login_url,headers=headers ,data=json.dumps(payload))
            json_data=json.loads(r.text)
            request.session['token']=json_data['token']
            return render(request, 'home/login.html', {'form': form})
        else:
            return render(request, 'home/login.html', {'form': form})


    else:
        form = loginForm()
        return render(request, 'home/login.html', {'form':form})