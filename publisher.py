import time
from gpiozero import CPUTemperature
import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


Broker = "192.168.0.130"
sub_topic_accel = "cpu/data"    # receive messages on this topic
sub_topic_accel = "accel/instructions"    # receive messages on this topic
sub_topic_lat = "latitude/instructions"    # receive messages on this topic
sub_topic_lon = "longitude/instructions"    # receive messages on this topic
sub_topic_time = "time/instructions"    # receive messages on this topic

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
    client.subscribe(sub_topic_accel)
    client.subscribe(sub_topic_lat)
    client.subscribe(sub_topic_lon)
    client.subscribe(sub_topic_time)

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
    accel_x,accel_y,accel_z= read_acceleration()
    temperature, cpu_use = cpu_data()
    client.publish("cpu/memory", str(cpu_use),qos=2,retain=True)
    client.publish("cpu/temp", str(temperature),qos=2,retain=True)
    client.publish("monto/solar/sensors/accel_x", str(accel_x),qos=2,retain=True)
    client.publish("monto/solar/sensors/accel_y", str(accel_y),qos=2,retain=True)
    client.publish("monto/solar/sensors/accel_z", str(accel_z),qos=2,retain=True)
    time.sleep(2)