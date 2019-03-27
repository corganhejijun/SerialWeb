from django.shortcuts import render
from django.http import JsonResponse
from .getSerial import SerialPort
import json

serialPort = SerialPort()
port_list = serialPort.getPortList()

def getOpenList():
    list = []
    for port in port_list:
        name = port[0]
        opened = not serialPort.ready2Open(name)
        if opened and not serialPort.openByMe(name):
            continue
        list.append({name:opened})
    return list

# Create your views here.
def index(request):
    return render(request, 'webChart/index.html', {'list': getOpenList()})

def onePage(request):
    return render(request, 'webChart/onePage.html', {'list': getOpenList()})

def fourPage(request):
    return render(request, 'webChart/fourPage.html', {'list': getOpenList()})

def chart(request):
    return render(request, 'webChart/chart.html')

def jsonData(request):
    func = request.GET['func']
    if func == "open":
        name = request.GET['name']
        serialPort.create(name)
        return JsonResponse({'flag':True})
    elif func == "close":
        name = request.GET['name']
        serialPort.port_close(name)
        return JsonResponse({'flag':True})
    elif func == "read":
        name = request.GET['name']
        nameList = name.split(",")
        msg = serialPort.read_data(nameList)
        return JsonResponse({'flag':True, 'msg': msg})
    elif func == "checkOpen":
        result = serialPort.getOpenList()
        return JsonResponse({'flag':True, 'openList':result['open'], 'occupy':result['occupy']})
    return JsonResponse({'flag':False})
