import time
import os
from gpiozero import CPUTemperature
import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import microstacknode.hardware.gps.l80gps 
from microstacknode.hardware.accelerometer.mma8452q import MMA8452Q
gps = microstacknode.hardware.gps.l80gps.L80GPS()

Broker = "192.168.0.130"
sub_topic_cpu_temp = "cpu/temp"    # receive messages on this topic
sub_topic_cpu_mem = "cpu/memory"    # receive messages on this topic
sub_topic_lat = "gps/latitude"    # receive messages on this topic
sub_topic_lon = "gps/longitude"    # receive messages on this topic
sub_topic_accelx = "accelerometre/axe_x"    # receive messages on this topic
sub_topic_accely = "accelerometre/axe_y"    # receive messages on this topic
sub_topic_accelz = "accelerometre/axe_z"    # receive messages on this topic

pub_topic = "sensor/data"       # send messages to this topic

dataFile = "gather_Data/data/"+time.strftime("%d-%m-%Y")+".txt"

############### sensehat inputs ##################

def read_acceleration():

    f = open(dataFile,"r")
    lines = f.readlines()
    result=[]
    for i in lines:
        i = i.split(',')[1] # read the second member after ',' which is accel_x;accel_y;accel_z
        accel_x = i.split(';')[0] # read the first member before the ';' which accel_x
        accel_y = i.split(';')[1]
        accel_z = i.split(';')[2]
    f.close
    print("x=",accel_x)
    print("y=",accel_y)
    print("z=",accel_z)
    
    return accel_x,accel_y,accel_z
############### read CPU temprature ############ 
def cpu_data():
    
    cpu = CPUTemperature()
    temperature = cpu.temperature
    cpu_use = psutil.cpu_percent()
    print("temperature cpu = ",temperature)
    print("cpu usage percent = " , cpu_use)
    return temperature,cpu_use
    
############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic_accelx)
    client.subscribe(sub_topic_accely)
    client.subscribe(sub_topic_accelz)
    client.subscribe(sub_topic_lat)
    client.subscribe(sub_topic_lon)
    client.subscribe(sub_topic_cpu_temp)
    client.subscribe(sub_topic_cpu_mem)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)
    display_sensehat(message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    exist = os.path.isfile(dataFile)
    if exist:
        accel_x,accel_y,accel_z= read_acceleration()
        temperature, cpu_use = cpu_data()
        client.publish(sub_topic_cpu_mem , str(cpu_use),qos=2,retain=True)
        client.publish(sub_topic_cpu_temp , str(temperature),qos=2,retain=True)
        client.publish(sub_topic_accelx, str(accel_x),qos=2,retain=True)
        client.publish(sub_topic_accely, str(accel_y),qos=2,retain=True)
        client.publish(sub_topic_accelz, str(accel_z),qos=2,retain=True)
        time.sleep(2)
    else:
        data = gps.get_gprmc()
        lat = data.get("latitude")
        long = data.get("longitude")
        print("latitude,longitude",lat,long)
        temperature, cpu_use = cpu_data()
        client.publish(sub_topic_cpu_mem , str(cpu_use),qos=2,retain=True)
        client.publish(sub_topic_cpu_temp, str(temperature),qos=2,retain=True)
        client.publish(sub_topic_lat, str(lat),qos=2,retain=True)
        client.publish(sub_topic_lon, str(long),qos=2,retain=True)
        
        time.sleep(2)
        