# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
from my_app import monitor
import influxdb
# Create your views here.

client = influxdb.InfluxDBClient('10.190.80.36', 8086, 'cadvisor', 'cadvisor', 'cadvisor')
memorydata = []
def index(request):
    return render(request,"monitor.html")


def old(request):
    return render(request, "2monitor.html")


# def getotherdata(request, container_name, infotype):
#     global memorydata
#     isfirst = request.GET.get("firsttime","false")
#     if isfirst=="true":
#         data = monitor.getmemory(client, container_name, infotype)
#         return HttpResponse(json.dumps(data[-20:], ensure_ascii=False), content_type="application/json,charset=utf-8")
#     else:
#         if memorydata:
#             data = memorydata[0]
#             memorydata = memorydata[1:]
#             return HttpResponse(json.dumps(data, ensure_ascii=False),
#                                 content_type="application/json,charset=utf-8")
#         else:
#             memorydata = monitor.getmemory(client, container_name, infotype)
#             data = memorydata[0]
#             memorydata = memorydata[1:]
#             return HttpResponse(json.dumps(data, ensure_ascii=False),
#                                 content_type="application/json,charset=utf-8")

def getotherdata(request, container_namelist, infotype,isfirst):
    if isfirst=="true":
        alldata = {}
        for container_name in container_namelist:
            data = []
            shifttime = 90
            for i in range(30):
                onedata = monitor.getmemory2(client, container_name, infotype, shifttime)
                shifttime = shifttime - 1
                data.append(onedata)
            alldata[container_name] = data
        return HttpResponse(json.dumps(alldata, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        alldata = {}
        for container_name in container_namelist:
            data = monitor.getmemory2(client, container_name, infotype, 60)
            alldata[container_name] = data
        return HttpResponse(json.dumps(alldata, ensure_ascii=False), content_type="application/json,charset=utf-8")



def getdata(request):
    postBody = request.body
    post_data = json.loads(postBody)
    isfirst = post_data.get("firsttime", "false")
    infotype = post_data.get("infotype", "cpu")
    container_namelist = post_data.get("container_namelist", "cadvisor")
    # container_namelist = [str(i) for i in container_namelist]
    if infotype == "cpu":
        if isfirst == "true":
            alldata = {}
            for container_name in container_namelist:
                data = []
                shifttime = 90
                for i in range(30):
                    onedata = monitor.getcpu(client, container_name,  shifttime )
                    shifttime = shifttime - 1
                    data.append(onedata)
                alldata[container_name] = data
            return HttpResponse(json.dumps(alldata, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            alldata = {}
            for container_name in container_namelist:
                data = monitor.getcpu(client, container_name, 60)
                alldata[container_name] = data
            return HttpResponse(json.dumps(alldata, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return getotherdata(request, container_namelist, infotype,isfirst)





