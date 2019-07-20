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





def getalldata(request):
    postBody = request.body
    post_data = json.loads(postBody)
    isfirst = post_data.get("firsttime", "false")
    container_namelist = post_data.get("container_namelist", ["cadvisor"])
    responedata = {}
    if isfirst == "true":
        # get cpudata
        cpudata = {}
        for container_name in container_namelist:
            data = []
            shifttime = 90
            for i in range(30):
                onedata = monitor.getcpu(client, container_name, shifttime)
                shifttime = shifttime - 1
                data.append(onedata)
            cpudata[container_name] = data
        responedata['cpudata'] = cpudata
        # get otherdata
        for datatype in ['memory_usage','rx_bytes','tx_bytes']:
            alldata = {}
            for container_name in container_namelist:
                data = []
                shifttime = 90
                for i in range(30):
                    onedata = monitor.getmemory2(client, container_name, datatype, shifttime)
                    shifttime = shifttime - 1
                    data.append(onedata)
                alldata[container_name] = data
            responedata[datatype] = alldata
    else:
        # get cpudata
        cpudata = {}
        for container_name in container_namelist:
            data = monitor.getcpu(client, container_name, 60)
            cpudata[container_name] = data
        responedata['cpudata'] = cpudata
        # get otherdata
        for datatype in ['memory_usage', 'rx_bytes', 'tx_bytes']:
            alldata = {}
            for container_name in container_namelist:
                data = monitor.getmemory2(client, container_name, datatype, 60)
                alldata[container_name] = data
            responedata[datatype] = alldata
    return HttpResponse(json.dumps(responedata, ensure_ascii=False), content_type="application/json,charset=utf-8")











