from django.shortcuts import render
from django.http import JsonResponse
from .getSerial import SerialPort
import json

serialPort = SerialPort()
port_list = serialPort.getPortList()
# Create your views here.
def index(request):
    list = []
    for port in port_list:
        name = port[0]
        isOpen = serialPort.isOpen(name)
        if not isOpen and serialPort.openByOther(name):
            continue
        list.append({name:isOpen})
    return render(request, 'webChart/index.html', {'list': list})

def jsonData(request):
    func = request.GET['func']
    name = request.GET['name']
    if func == "open":
        serialPort.create(name)
        return JsonResponse({'flag':True})
    elif func == "close":
        serialPort.port_close(name)
        return JsonResponse({'flag':True})
    elif func == "read":
        msg = serialPort.read_data(name)
        return JsonResponse({'flag':True, 'msg': msg})
    elif func == "checkOpen":
        result = serialPort.getOpenList()
        return JsonResponse({'flag':True, 'openList':result['open'], 'occupy':result['occupy']})
    return JsonResponse({'flag':False})
