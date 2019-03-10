#!/usr/bin/python
 
import serial
import time
import requests
import json
import urllib2
import math
import smbus  
from decimal import *
from subprocess import call
from twilio.rest import Client


# Authentification a l'API d'envoie de SMS

# Your Account SID from twilio.com/console
account_sid = "AC6c616a87937f8b4b9d421e8058ad4efb"
# Your Auth Token from twilio.com/console
auth_token  = "c1f767c37d9f4dbce7e95afbaf4340bd"

client = Client(account_sid, auth_token)

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

hasChute = False
chuteDelay = 0

# Fin authentification a l'API d'envoie de SMS

def deg2rad(x):
    return math.pi*float(x)/180

def getDistance(lat1,long1,lat2,long2):
    earthRadius = 6378137
    rlat1 = deg2rad(lat1)
    rlong1 = deg2rad(long1)
    rlat2 = deg2rad(lat2)
    rlong2 = deg2rad(long2)
    dlong = (rlong2 - rlong1)
    dlat = (rlat2 - rlat1)
    a = (math.sin(dlat)*math.sin(dlat)+math.cos(rlat1)*math.cos(rlat2)*(math.sin(dlong) * math.sin(dlong)))
    d = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    return earthRadius * d



def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
 
def getAdresse(lat, lng):
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + lat + ',' + lng + '&key=AIzaSyC4DCIF0yx1PIDU-Mwv__iXSUKQ7hUYWCw')
    data = r.json()
    return data['results'][0]['formatted_address']

 
 
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
 
test = 'AT'+'\r\n'
port.write(test.encode('utf-8')) 
rcv = port.read(100).decode() 

 
test2 = 'AT+CGNSPWR=1'+'\r\n'             # to power the GPS
port.write(test2.encode('utf-8')) 
rcv = port.read(100).decode() 

 
test3 = 'AT+CGNSIPR=115200'+'\r\n' # Set the baud rate of GPS
port.write(test3.encode('utf-8')) 
rcv = port.read(100).decode() 

 
test4 = 'AT+CGNSTST=1'+'\r\n'
port.write(test4.encode('utf-8')) # Send data received to UART
rcv = port.read(100).decode() 

test5 = 'AT+CGNSINF'+'\r\n'
port.write(test5.encode('utf-8'))       # Print the GPS information

rcv = port.read(200).decode() 

ck=1

def getDirection(latActuelle, longActuelle):
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+ latActuelle +',' + longActuelle +'&destination=69 Avenue Aristide Briand, 21000 Dijon&key=AIzaSyC4DCIF0yx1PIDU-Mwv__iXSUKQ7hUYWCw')
    data = r.json()
    

    dataEtape = data['routes'][0]['legs'][0]['steps'][0]  

    dataJson = {}
    print('#Adresse destination = ' + data['routes'][0]['legs'][0]['end_address'])
    print('#Distance restante = ' + data['routes'][0]['legs'][0]['distance']['text'])
    print('#Distance prochaine etape = ' + dataEtape['distance']['text'])
    print('#Temps restant = ' + data['routes'][0]['legs'][0]['duration']['text'])
    print('#Instruction = ' + dataEtape['html_instructions'])
    if 'maneuver' in dataEtape:      
        dataJson['maneuver'] = dataEtape['maneuver']
        print('#Maneuvre = ' + dataEtape['maneuver'])
    
    dataJson['html_instructions'] = dataEtape['html_instructions']
    dataJson['distanceFinEtape'] = dataEtape['distance']['text']
    dataJson['totalKM'] = data['routes'][0]['legs'][0]['distance']['text']
    dataJson['totalTemps'] = data['routes'][0]['legs'][0]['duration']['text']
    dataJson['AdresseArrivee'] = data['routes'][0]['legs'][0]['end_address']
    
    
    
    print('-----------')
    
    #requests.post('http://localhost/api/index.php', data = json.dumps(dataJson))
    
    #req = urllib2.Request('http://localhost/api/index.php')
    #req.add_header('Content-Type', 'application/json')
    #response = urllib2.urlopen(req, json.dumps(dataJson))
  
while ck==1:
   
    fd = port.read(200).decode('utf-8')        # Read the GPS data from UART
    #print (fd)
    #time.sleep(0.3)
    if '$GNRMC' in fd:        # To Extract Lattitude and 
        ps=fd.find('$GNRMC')        # Longitude
        dif=len(fd)-ps
        if dif > 50:
            data=fd[ps:(ps+50)]  
            ds=data.find('A')        # Check GPS is valid
            if ds > 0 and ds < 20:
                p=list(find(data, ","))
                lat=data[(p[2]+1):p[3]]
                lon=data[(p[4]+1):p[5]]

                s1=lat[2:len(lat)]
                s1=Decimal(s1)
                s1=s1/60
                s11=int(lat[0:2])
                s1 = s11+s1
 
                s2=lon[3:len(lon)]
                s2=Decimal(s2)
                s2=s2/60
                s22=int(lon[0:3])
                s2 = s22+s2                
            
                getDirection(str(s1), str(s2))
                
                print ('lattitude = ' + str(s1))
                print ('longitude = ' + str(s2))
                print ('////////////////////////////////////////////////////')
                
                ###### Gestion chute et SMS #######
                
                #Read Accelerometer raw value
                acc_x = read_raw_data(ACCEL_XOUT_H)
                
                #Full scale range +/- 250 degree/C as per sensitivity scale factor
                Ax = acc_x/16384.0

                
                if round(Ax,2) > 0.90 or round(Ax,2) < - 0.90:
                    print('Vehicule penche')
                    chuteDelay = chuteDelay + 1
                    if chuteDelay == 10:
                        adresse = getAdresse(str(s1), str(s2))
                        hasChute = True
                        message = client.messages.create(
                        to='+33695342896',
                        from_='+17653263657',
                        body='Moto accidentee a l\'adresse suivante : ' + adresse + '.Coordonnee : longitude = ' + str(s1) + ', latitude = ' + str(s2) + '.' )
                else:
                    chuteDelay = 0
                    hasChute = False
                    
                print ("\tAx=%.2f g" %Ax)
                time.sleep(1)


