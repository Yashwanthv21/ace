import json

from channels import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from datetime import datetime

from reports.forms import UserEditForm
from reports.models import Data, UsersImei


def receive_data(request):
    try:
        name = imei = sstr = devTime = hum = temp = None

        if 'Name' in request.GET and request.GET['Name']:
            name = request.GET['Name']
        if 'IMEI' in request.GET and request.GET['IMEI']:
            imei = request.GET['IMEI']
        if 'Sstr' in request.GET and request.GET['Sstr']:
            sstr = request.GET['Sstr']
        if 'DevTime' in request.GET and request.GET['DevTime']:
            devTime = datetime.strptime(request.GET['DevTime'], '%d/%m/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        if 'Temp' in request.GET and request.GET['Temp']:
            temp = request.GET['Temp']
        if 'Hum' in request.GET and request.GET['Hum']:
            hum = request.GET['Hum']
        data = Data(name=name, imei=imei, s_str=sstr, dev_time=devTime, humidity=hum, temperature=temp)
        data.save()
        d = {'sstr': sstr, 'tem': temp, 'hum': hum}
        Group('chat-' + imei).send({'text': json.dumps(d)})
        return HttpResponse("success")
    except Exception as e:
        return HttpResponse(str(e))

@login_required(login_url='/login/')
def dashboard(request):
    imei_table = UsersImei.objects.all()
    if not request.user.is_superuser:
        imei_table = imei_table.filter(user_id=request.user.id)
    return render(request, 'reports/dashboard.html', {'imei_table': imei_table})

@login_required(login_url='/login/')
def view_device(request,id):
    imei_table_row = ''
    try:
        if request.user.is_superuser:
            imei_table_row = UsersImei.objects.get(id=id)
        elif not request.user.is_superuser:
            imei_table_row = UsersImei.objects.get(id=id, user_id=request.user.id)

    # Query the model
        table = Data.objects.filter(imei=imei_table_row.imei_numbers)
        return render(request, 'reports/view.html', {'table' : table, 'device' : imei_table_row})
    except:
        return render(request, 'reports/base.html')

@login_required(login_url='/login/')
def profile(request):

    edit_form = UserEditForm(instance=request.user)
    return render(request, 'reports/profile.html', {'form': edit_form})
