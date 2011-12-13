import subprocess
import sys
import os

descriptors = list()
om_path = "/opt/dell/srvadmin/bin/omreport"
ambient_index = "0"

def System_Board_Consumption(name):
    global om_path
    global ambient_index
    p1 = subprocess.Popen([om_path,"chassis","temps","pwrmonitoring"],stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep","Reading"],stdin=p1.stdout,stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["head","-n","1"],stdin=p2.stdout,stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["awk","{print $3}"],stdin=p3.stdout,stdout=subprocess.PIPE)
    temp = (p4.communicate()[0]).rstrip(os.linesep)
    return float(temp)
    
def System_Board_Ambient(name):
    global om_path
    p1 = subprocess.Popen([om_path,"chassis","temps","Index="+ambient_index],stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep","Reading"],stdin=p1.stdout,stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["awk","{print $3}"],stdin=p2.stdout,stdout=subprocess.PIPE)
    temp = (p3.communicate()[0]).rstrip(os.linesep)
    return float(temp)
    
def metric_init(params):
    global descriptors
    global om_path
    global ambient_index
    
    if 'om_path' in params:
        om_path = params['om_path']

    if 'ambient_index' in params:
        ambient_index = params['ambient_index']
    
    d1 = {'name': 'System_Board_Ambient',
        'call_back': System_Board_Ambient,
        'time_max': 90,
        'value_type': 'float',
        'units': 'Celsius',
        'slope': 'both',
        'format': '%.1f',
        'description': 'System board ambient temperature probe',
        'groups': 'hardware'}

    d2 = {'name': 'System_Board_Consumption',
        'call_back': System_Board_Consumption,
        'time_max': 90,
        'value_type': 'float',
        'units': 'Watt',
        'slope': 'both',
        'format': '%.1f',
        'description': 'System board system power consumption level',
        'groups': 'hardware'}

    descriptors = [d1,d2]
    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

#This code is for debugging and unit testing    
if __name__ == '__main__':
    params = {'ambient_index': '0',
        'om_path': '/opt/dell/srvadmin/bin/omreport'}
    metric_init(params)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'],  v)
