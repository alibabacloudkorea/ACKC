#!/usr/bin/env python
#coding=utf-8
import sys
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcms.request.v20190101.DescribeSiteMonitorDataRequest import DescribeSiteMonitorDataRequest
import json


client = AcsClient('<accessKey>',
                   '<accessSecret>', 'cn-hangzhou')

# We monitored over the weekend (Sat and Sun)
def DescribeSiteMonitorData (taskId, metricName):
  request = DescribeSiteMonitorDataRequest()
  request.set_accept_format('json')
  request.set_MetricName(metricName)
  request.set_TaskId(taskId)
  request.set_StartTime("2021-03-06T00:00:00Z")
  request.set_EndTime("2021-03-07T23:59:59Z")
  response = client.do_action_with_exception(request)
  return response 



GaResponse = DescribeSiteMonitorData('ce8f0758-90ca-4436-8de0-e5bdac023b58', 'ResponseTime')
GaAvailability = DescribeSiteMonitorData('ce8f0758-90ca-4436-8de0-e5bdac023b58', 'Availability') 
InternetResponse = DescribeSiteMonitorData('d4ea0e26-a227-4006-8bad-0781556000b3', 'ResponseTime')
InternetAvailability = DescribeSiteMonitorData('d4ea0e26-a227-4006-8bad-0781556000b3', 'Availability')

#Response time
def getResponse(ResponseData):
  parse = json.loads(ResponseData)
  parseResponse = parse.get('Data')
  res = []
  for list in parseResponse:
    res.append(list.get('Average'))
  
  print(sum(res)/len(res))
  res = []


# Availability
def getAvailability(AvailabilityData):
  parse1 = json.loads(AvailabilityData)
  parseAvailability = parse1.get('Data')
  ava = []
  for list in parseAvailability:
    ava.append(list.get('Availability'))
  print(sum(ava)/len(ava))
  ava = []
  
# MaxResponse
def getMaxResponse(ResponseData):
  parse = json.loads(ResponseData)
  parseResponse = parse.get('Data')
  maximum = []
  for list in parseResponse:
    maximum.append(list.get('Average'))
  print(max(maximum))
  res = []

# MinResponse
def getMinResponse(ResponseData):
  parse = json.loads(ResponseData)
  parseResponse = parse.get('Data')
  minimum = []
  for list in parseResponse:
    minimum.append(list.get('Average'))
  print(min(minimum))
  res = []
  
# Get GA avg/max/min response time
getResponse(GaResponse)
getMaxResponse(GaResponse)
getMinResponse(GaResponse)

# Get Internet avg/max/min response time
getResponse(InternetResponse)
getMaxResponse(InternetResponse)
getMinResponse(InternetResponse)

# Get GA and Internet availablity
getAvailability(GaAvailability)
getAvailability(InternetAvailability)
