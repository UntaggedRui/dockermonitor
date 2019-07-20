#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/18/19 8:57 AM
# @Author  : 张瑞
# @Site    : 
# @File    : monitor.py
# @Software: PyCharm

import influxdb
import time
def getclient():
    client = influxdb.InfluxDBClient('10.190.80.36', 8086, 'cadvisor', 'cadvisor', 'cadvisor')
    return client

def getmemory(client,container_name,resourcename):
    sys_time1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 120))
    sys_time2 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 60))
    sql = "select * from {} where container_name = '{}' and time > '{}' and time < '{}'".format(resourcename,container_name,sys_time1,sys_time2)
    results = client.query(sql).get_points()
    results = list(results)
    # result = results[0]
    # result['value'] = result['value']*1.0/1024/1024
    # print(result)
    for result in results:
        result['value'] = result['value'] * 1.0 / 1024 / 1024
    return results

def getmemory2(client,container_name,resourcename,shifttime):
    sys_time1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - shifttime - 3))
    sys_time2 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - shifttime))
    sql = "select mean(value) from {} where container_name = '{}' and time > '{}' and time < '{}'".format(resourcename,
                                                                                                container_name,
                                                                                                sys_time1, sys_time2)
    results = client.query(sql).get_points()
    results = list(results)
    value = results[0]['mean'] * 1.0 / 1024 / 1024
    return {'time':sys_time1,'value':value}




def strtoTimestamp(timestr):
    formattime = timestr[0:19]
    stamp = timestr[20:23]
    timestamp = time.mktime(time.strptime(formattime,"%Y-%m-%dT%H:%M:%S"))
    timestamp = timestamp*1000+int(stamp)
    return timestamp


def getinterval(current, previous):
    cur = strtoTimestamp(current)
    prev = strtoTimestamp(previous)
    return int(cur-prev) * 1000000



def getcpu(client,container_name,shifttime):
    sys_time1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - shifttime-5 ))
    sys_time2 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - shifttime))
    sql = "select * from {} where container_name = '{}' and time > '{}' and time < '{}'"
    results = client.query(sql.format('cpu_usage_total', container_name, sys_time1, sys_time2)).get_points()
    results = list(results)
    begintime,beginvalue = results[0]['time'],results[0]['value']
    endtime, endvalue = results[-1]['time'], results[-1]['value']
    intervalNs = getinterval(endtime,begintime)
    if intervalNs:
        cpu_percent = 1.0 * (endvalue-beginvalue)/intervalNs
        return {'time':sys_time1,'value':cpu_percent}
    else:
        return {'time':sys_time1,'value':0.03}


if __name__ == '__main__':
    client = getclient()
    while True:
        time.sleep(1)
        print getmemory2(client,'cadvisor','memory_usage',60)
    # a = getmemory(client, 'cadvisor', 'memory_usage')

    # while True:
    #     print getcpu(client, 'cadvisor')
    #     time.sleep(1)
    # getmemory(client, 'cadvisor', 'rx_bytes')
    # getmemory(client, 'cadvisor', 'tx_bytes')
    # cadvisor_cpu = getcpu(client, 'cadvisor')
    # print("cadvisor:", cadvisor_cpu * 100)

    client.close()