#/usr/local/bin/python
import requests
import datetime
import random
import time
import sys
print ("Iniciando...")
#payload = (('key1', 'value1'), ('key1', 'value2'))
#r = requests.get('https://api.github.com/events')
idDevice=sys.argv[1]
count=0
while True:
    currentTime=str(datetime.datetime.utcnow())
    power=random.randint(50, 60)

    payload="""
    <sunspecdata v="1.0">
    <d id="1234" t=\" """ + currentTime + """ \">
    <m id="power" x="1">
    <p id="watts" t=\" """ + currentTime + """ \">""" + str(power) + """</p>
    </m>
    </d>
    </sunspecdata>"""

    payload = '''
    <SunSpecData v="1.0">
    <d id=\"'''+idDevice+'''\" t=\"''' + currentTime +  '''\">
    <m id="potenciometro" x="0">
    <p id="consumo" t=\"''' + currentTime + '''\">''' + str(power) + '''</p>
    </m>
    </d>
    </SunSpecData>
    '''
    print "bytes: ", len(payload)

    print(payload)
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    #r = requests.post('http://httpbin.org/post', data=payload, headers=headers).text
    #r = requests.post('http://192.168.100.112:10000/celeste/logger/upload/verbose', data=payload, headers=headers)
    t1=time.clock()
    
    r = requests.post('http://ee435cba.ngrok.io/celeste/logger/upload/verbose', data=payload, headers=headers)
    t2=time.clock()
    print 'time: ', t2-t1
    print 'Response content:'
    print(r.content)
    print 'Status code: %d' % (r.status_code)
    time.sleep(.8)
    count+=1
    if count >= 1000:
        break
print 'total de paquetes subiods: ', count
