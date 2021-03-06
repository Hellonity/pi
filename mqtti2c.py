import smbus
import time
import board
import busio
import json
import paho.mqtt.client as mqtt

def on_message(client, userdata, message) :
    print("Received message:{} on topic {}".format(message.payload, message.topic))



client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
print(client.connect("test.mosquitto.org",port=8884))
# msg = input()
# msg_info = client.publish("IC.embedded/HAGI/test",msg)
#msg_info is result of publish()

client.subscribe("IC.embedded/HAGI/#")
client.on_message = on_message
client.loop_start()

# Create library object using our Bus I2C port
#i2c = busio.I2C(board.SCL, board.SDA)
bus = smbus.SMBus(1)

# Initialize communication with the sensor, using the default 16 samples per conversion.
# This is the best accuracy but a little slower at reacting to changes.
# The first sample will be meaningless
while True:

    #bus.write_byte(0x40,0x03)
    obj = bus.read_i2c_block_data(0x40,0x03,2)
    raw = bus.read_i2c_block_data(0x40,0x01,2)
    #print(obj)
    #print(raw)
    int_obj=int.from_bytes(obj,'big')
    int_raw=int.from_bytes(raw,'big')
    obj_temp=int_obj*0.03125/4
    die_temp=int_raw*0.03125/4
    #print(temp)
    #print(die)

    data = {
        "temperature":{
            "die": die_temp,
            "object": obj_temp
        }
    }


    json_string = json.dumps(data)

    client.publish("IC.embedded/HAGI/test",json_string)

    time.sleep(5.0)
