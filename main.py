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
        client.publish("power/status",payload="online", qos=0, retain=True)
        client.publish("homeassistant/sensor/powercounter/ua/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"voltage","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Ua","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_ua","unit_of_measurement":"V","value_template":"{{ value_json.Ua }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/ub/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"voltage","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Ub","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_ub","unit_of_measurement":"V","value_template":"{{ value_json.Ub }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/uc/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"voltage","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Uc","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_uc","unit_of_measurement":"V","value_template":"{{ value_json.Uc }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/ia/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"current","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Ia","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_ia","unit_of_measurement":"A","value_template":"{{ value_json.Ia }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/ib/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"current","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Ib","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_ib","unit_of_measurement":"A","value_template":"{{ value_json.Ib }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/ic/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"current","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Ic","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_ic","unit_of_measurement":"A","value_template":"{{ value_json.Ic }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pa/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pa","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_pa","unit_of_measurement":"W","value_template":"{{ value_json.Pa }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pb/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pb","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_pb","unit_of_measurement":"W","value_template":"{{ value_json.Pb }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pc/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pc","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_pc","unit_of_measurement":"W","value_template":"{{ value_json.Pc }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/qa/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"reactive_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Qa","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_qa","unit_of_measurement":"var","value_template":"{{ value_json.Qa }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/qb/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"reactive_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Qb","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_qb","unit_of_measurement":"var","value_template":"{{ value_json.Qb }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/qc/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"reactive_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Qc","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_qc","unit_of_measurement":"var","value_template":"{{ value_json.Qc }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/sa/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"apparent_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Sa","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_sa","unit_of_measurement":"VA","value_template":"{{ value_json.Sa }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/sb/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"apparent_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Sb","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_sb","unit_of_measurement":"VA","value_template":"{{ value_json.Sb }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/sc/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"apparent_power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Sc","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_sc","unit_of_measurement":"VA","value_template":"{{ value_json.Sc }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/p/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"power","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter P","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_p","unit_of_measurement":"W","value_template":"{{ value_json.P }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pcd/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"energy","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pcd","state_class":"total_increasing","state_topic":"power/counter","unique_id":"p_counter_pcd","unit_of_measurement":"kWh","value_template":"{{ value_json.Pcd }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pca/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"energy","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pca","state_class":"total","state_topic":"power/counter","unique_id":"p_counter_pca","unit_of_measurement":"kWh","value_template":"{{ value_json.Pca }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pcb/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"energy","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pcb","state_class":"total","state_topic":"power/counter","unique_id":"p_counter_pcb","unit_of_measurement":"kWh","value_template":"{{ value_json.Pcb }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/pcc/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"energy","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Pcc","state_class":"total","state_topic":"power/counter","unique_id":"p_counter_pcc","unit_of_measurement":"kWh","value_template":"{{ value_json.Pcc }}"}', qos=1, retain=True)
        client.publish("homeassistant/sensor/powercounter/hz/config", '{"availability":[{"topic":"power/status"}],"device":{"identifiers":["mercury230"],"manufacturer":"Mercury","model":"Mercury230","name":"Counter"},"device_class":"frequency","enabled_by_default":true,"json_attributes_topic":"power/counter","name":"Counter Hz","state_class":"measurement","state_topic":"power/counter","unique_id":"p_counter_hz","unit_of_measurement":"Hz","value_template":"{{ value_json.Hz }}"}', qos=1, retain=True)
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
client.will_set("power/status", payload="offline", qos=0, retain=True)
#client.on_subscribe = on_subscribe
#client.on_message = on_message
client.connect_async(mqtt_ipaddress) #connect to broker
#client.publish("test22","OFF")#publish
client.loop_start()


def cycle_read():
    while r:
        mercury_234.connect_user()
#        mercury_234.connection_test()
        Ua = mercury_234.get_voltage_A()
        Ub = mercury_234.get_voltage_B()
        Uc = mercury_234.get_voltage_C()
        Ia = mercury_234.get_current_A()
        Ib = mercury_234.get_current_B()
        Ic = mercury_234.get_current_C()
        P = mercury_234.get_P()
        Pa = mercury_234.get_P_A()
        Pb = mercury_234.get_P_B()
        Pc = mercury_234.get_P_C()
        Qa = mercury_234.get_Q_A()
        Qb = mercury_234.get_Q_B()
        Qc = mercury_234.get_Q_C()
        Sa = mercury_234.get_S_A()
        Sb = mercury_234.get_S_B()
        Sc = mercury_234.get_S_C()
        Hz = mercury_234.get_frequency()
#        Tcase = mercury_234.get_temp()
        Pcd = mercury_234.get_active_energy_current_day()
        Pca, Pcb, Pcc = mercury_234.get_active_energy_current_abc()
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
#        json_string6 = '"Hz": "' + str(Hz) + '"'
        json_string6 = '"Pcd": "' + str(Pcd) + '", "Pca": "' + str(Pca) + '", "Pcb": "' + str(Pcb) + '", "Pcc": "' + str(Pcc) + '", "Hz": "' + str(Hz) + '"'
        json_string_end = '{' + json_string1 + ',' + json_string2 + ',' + json_string3 + ',' + json_string4 + ',' + json_string5 + ',' + json_string6 + '}'
#        json_object = json.loads(json_string)
#        print(json_string1)
#        print(json_string2)
        client.publish(mqtt_topic, json_string_end, 1)
        mercury_234.disconnect()
        time.sleep(4)

cycle_read()