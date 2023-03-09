#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import argparse
# import serial
import struct
import time
#import json
import configparser
import paho.mqtt.client as mqtt
from mercury230 import Mercury230
#import db_connector as db
# from bitstring import BitArray

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
#addr = struct.pack('B', address)
ipaddress = config["counter"]["ipaddress"]
ipport = config["counter"]["ipport"]
mqtt_ipaddress = config["mqtt"]["ipaddress"]
#mqtt_port = config["mqtt"]["port"]
mqtt_user = config["mqtt"]["user"]
mqtt_pass = config["mqtt"]["pass"]
mqtt_topic = config["mqtt"]["topic"]
r = True
mercury_234 = Mercury230(address, ipaddress, ipport)
#ser = open_port(self.ipaddress1, self.ipport1)
#ser.timeout = 0.1

def on_connect(client, userdata, flags, rc):
    if rc == 0:
#        client.loop_start()
#        client.loop_start()
        print("connected OK Returned code=", rc)
#        logging.info("connected OK Returned code=" + str(rc))
#        client.subscribe("gate1/reply", qos=1)
    else:
        print("Bad connection Returned code=", rc)
#        logging.info("Bad connection Returned code=" + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
#        client.loop_stop()
        print ("Unexpected MQTT disconnection. Will auto-reconnect")

#def on_subscribe(client, userdata, mid, granted_qos):
#    print("I've subscribed with QoS: {}".format(
#    granted_qos[0]))

#def on_message(client, userdata, msg):
#    global pingerror
#    print("Message received. Topic: {}. Payload: {}".format(
#        msg.topic,
#        str(msg.payload)))
#    if str(msg.payload) == "b'tx-end'":
#        bot.send_message(message_chat_id, 'Сигнал отправлен')
#    if str(msg.payload) == "b'ping-ok'":
#        pingerror = 0

client = mqtt.Client("counter") #create new instance
client.username_pw_set(mqtt_user, mqtt_pass)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_subscribe = on_subscribe
#client.on_message = on_message
client.connect_async(mqtt_ipaddress) #connect to broker
#client.publish("test22","OFF")#publish
client.loop_start()


def cycle_read():
    Ua = 0
    Ub = 0
    Uc = 0
    fooUa = True
    fooUb = True
    fooUc = True
    Ia = 0
    Ib = 0
    Ic = 0
    fooIa = True
    fooIb = True
    fooIc = True
    Pa = 0
    Pb = 0
    Pc = 0
    fooPa = True
    fooPb = True
    fooPc = True
    Qa = 0
    Qb = 0
    Qc = 0
    fooQa = True
    fooQb = True
    fooQc = True
    Sa = 0
    Sb = 0
    Sc = 0
    fooSa = True
    fooSb = True
    fooSc = True
    P = 0
    Pcd = 0
    Hz = 0
    fooP = True
    fooPcd = True
    fooHz = True
    while r == True:
        mercury_234.connect_user()
#        mercury_234.connection_test()
        lUa = mercury_234.get_voltage_A()
        lUb = mercury_234.get_voltage_B()
        lUc = mercury_234.get_voltage_C()
        lIa = mercury_234.get_current_A()
        lIb = mercury_234.get_current_B()
        lIc = mercury_234.get_current_C()
        lP = mercury_234.get_P()
        lPa = mercury_234.get_P_A()
        lPb = mercury_234.get_P_B()
        lPc = mercury_234.get_P_C()
        lQa = mercury_234.get_Q_A()
        lQb = mercury_234.get_Q_B()
        lQc = mercury_234.get_Q_C()
        lSa = mercury_234.get_S_A()
        lSb = mercury_234.get_S_B()
        lSc = mercury_234.get_S_C()
        lHz = mercury_234.get_frequency()
#        Tcase = mercury_234.get_temp()
        lPcd = mercury_234.get_active_energy_current_day()
        if lUa != 'crc_false' and abs(lUa - Ua) < 30:
                Ua = lUa
                fooUa = False
        else:
            if fooUa:
                Ua = lUa
                fooUa = False
            fooUa = True
            time.sleep(5)
        if lUb != 'crc_false' and abs(lUb - Ub) < 30:
                Ub = lUb
                fooUb = False
        else:
            if fooUb:
                Ub = lUb
                fooUb = False
            fooUb = True
            time.sleep(5)
        if lUc != 'crc_false' and abs(lUc - Uc) < 30:
                Uc = lUc
                fooUc = False
        else:
            if fooUc:
                Uc = lUc
                fooUc = False
            fooUc = True
            time.sleep(5)

        if lIa != 'crc_false' and abs(lIa - Ia) < 5:
                Ia = lIa
                fooIa = False
        else:
            if fooIa:
                Ia = lIa
                fooIa = False
            fooIa = True
        if lIb != 'crc_false' and abs(lIb - Ib) < 5:
                Ib = lIb
                fooIb = False
        else:
            if fooIb:
                Ib = lIb
                fooIb = False
            fooIb = True
        if lIc != 'crc_false' and abs(lIc - Ic) < 5:
                Ic = lIc
                fooIc = False
        else:
            if fooIc:
                Ic = lIc
                fooIc = False
            fooIc = True

        if lPa != 'crc_false' and abs(lPa - Pa) < 200:
                Pa = lPa
                fooPa = False
        else:
            if fooPa:
                Pa = lPa
                fooPa = False
            fooPa = True
        if lPb != 'crc_false' and abs(lPb - Pb) < 200:
                Pb = lPb
                fooPb = False
        else:
            if fooPb:
                Pb = lPb
                fooPb = False
            fooPb = True
        if lPc != 'crc_false' and abs(lPc - Pc) < 200:
                Pc = lPc
                fooPc = False
        else:
            if fooPc:
                Pc = lPc
                fooPc = False
            fooPc = True            

        if lQa != 'crc_false' and abs(lQa - Qa) < 200:
                Qa = lQa
                fooQa = False
        else:
            if fooQa:
                Qa = lQa
                fooQa = False
            fooQa = True
        if lQb != 'crc_false' and abs(lQb - Qb) < 200:
                Qb = lQb
                fooQb = False
        else:
            if fooQb:
                Qb = lQb
                fooQb = False
            fooQb = True
        if lQc != 'crc_false' and abs(lQc - Qc) < 200:
                Qc = lQc
                fooQc = False
        else:
            if fooQc:
                Qc = lQc
                fooQc = False
            fooQc = True            

        if lSa != 'crc_false' and abs(lSa - Sa) < 200:
                Sa = lSa
                fooSa = False
        else:
            if fooSa:
                Sa = lSa
                fooSa = False
            fooSa = True
        if lSb != 'crc_false' and abs(lSb - Sb) < 200:
                Sb = lSb
                fooSb = False
        else:
            if fooSb:
                Sb = lSb
                fooSb = False
            fooSb = True
        if lSc != 'crc_false' and abs(lSc - Sc) < 200:
                Sc = lSc
                fooSc = False
        else:
            if fooSc:
                Sc = lSc
                fooSc = False
            fooSc = True            

        if lP != 'crc_false' and abs(lP - P) < 1000:
                P = lP
                fooP = False
        else:
            if fooP:
                P = lP
                fooP = False
            fooP = True  
        if lPcd != 'crc_false' and abs(lPcd - Pcd) < 10:
                Pcd = lPcd
                fooPcd = False
        else:
            if fooPcd:
                Pcd = lPcd
                fooPcd = False
            fooPcd = True 
        if lHz != 'crc_false' and abs(lHz - Hz) < 1:
                Hz = lHz
                fooHz = False
        else:
            if fooHz:
                Hz = lHz
                fooHz = False
            fooHz = True 
#        print("Ua : ", Ua, ", Ub : ", Ub, ", Uc : ", Uc)
#        print("Ua : ", Ua)
#        print("Ia : ", Ia, ", Ib : ", Ib, ", Ic : ", Ic)
#        print("Pa : ", Pa, ", Pb : ", Pb, ", Pc : ", Pc)
#        print("Qa : ", Qa, ", Qb : ", Qb, ", Qc : ", Qc)
#        print("Sa : ", Sa, ", Sb : ", Sb, ", Sc : ", Sc)
#        print("Hz : ", Hz, ", Tcase : ", Tcase)
        # print("summPa,Pb,Pc :", mercury_234.get_active_energy_phases())
        # print(mercury_234.get_active_energy_current_day())
#        db.insert_data_data('data', Ua, Ub, Uc, Ia, Ib, Ic, P, Pa, Pb, Pc, Qa, Qb, Qc, Sa, Sb, Sc, Tcase)
        json_string1 = '"Ua": "' + str(Ua) + '", "Ub": "' + str(Ub) + '", "Uc": "' + str(Uc) + '"'
        json_string2 = '"Ia": "' + str(Ia) + '", "Ib": "' + str(Ib) + '", "Ic": "' + str(Ic) + '"'
        json_string3 = '"P": "' + str(P) + '", "Pa": "' + str(Pa) + '", "Pb": "' + str(Pb) + '", "Pc": "' + str(Pc) + '"'
        json_string4 = '"Qa": "' + str(Qa) + '", "Qb": "' + str(Qb) + '", "Qc": "' + str(Qc) + '"'
        json_string5 = '"Sa": "' + str(Sa) + '", "Sb": "' + str(Sb) + '", "Sc": "' + str(Sc) + '"'
        json_string6 = '"Hz": "' + str(Hz) + '"'
        json_string7 = '"Pcd": "' + str(Pcd) + '"'
        json_string_end = '{' + json_string1 + ',' + json_string2 + ',' + json_string3 + ',' + json_string4 + ',' + json_string5 + ',' + json_string6 + ',' + json_string7 + '}'
#        json_object = json.loads(json_string)
#        print(json_string1)
#        print(json_string2)
        client.publish(mqtt_topic, json_string_end, 1)
        mercury_234.disconnect()
        time.sleep(4)

cycle_read()