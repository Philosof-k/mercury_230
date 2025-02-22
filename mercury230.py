#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from bitstring import BitArray

#ser = open_port(self.ipaddress1, self.ipport1)
#ser.timeout = 0.1

class Mercury230:
    def __init__(self, address, ipaddress, ipport):
        self.addr = struct.pack('B', address)
        self.ipaddress1 = ipaddress
        self.ipport1 = ipport
#        ser = self.open_port(self.ipaddress1, self.ipport1)
#        ser.timeout = 0.1

    def open_port(self, ipaddress1, ipport1):
#        ser = serial.Serial(f"{port1}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        ser = serial.serial_for_url("socket://" + ipaddress1 + ":" + ipport1)
        return ser

    def test_hex_to_bin(self):
        # a = addr
        a = b"\x80\x00\x40\xE7\x29\x00\x40\xE7\x29\x00\x00\x00\x00\x00\x00\x00\x0f"
        mybyte = bytes(a)
        d = self.crc16(mybyte)
        binary_string = "{:08b}".format(int(mybyte.hex(), 16))
        bd = list(binary_string)

        print(bd, d)

    def crc16(self, data):
        crc = 0xFFFF
        l = len(data)
        i = 0
        while i < l:
            j = 0
            crc = crc ^ data[i]
            while j < 8:
                if (crc & 0x1):
                    mask = 0xA001
                else:
                    mask = 0x00
                crc = ((crc >> 1) & 0x7FFF) ^ mask
                j += 1
            i += 1
        if crc < 0:
            crc -= 256
        result = data + chr(crc % 256).encode('latin-1') + chr(crc // 256).encode('latin-1')
        return result

    def connection_test(self):
        chunk = self.addr
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        print(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        print ('Connected:', ser.isOpen())
        ser.write(chunk)
#        time.sleep(100 / 1000)
#        bytesToRead = ser.inWaiting()
        dat = ser.read(4)
        print(dat)

    def search_counter(self):
        # addr = self.addr
        chunk = b'\x00'
        chunk += b'\x08'
        chunk += b'\x05'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        dat = ser.read_all()
        zdat = list(dat)
        lengzdat = len(zdat)
        a1 = zdat[lengzdat - 3]
        # rs485addr = int(a1, 16)
        rs485addr = a1
        # print(a1)
        # print(rs485addr)
        return rs485addr, zdat

    def disconnect(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x02'  # код запроса
        chunk = self.crc16(chunk)
        # print("transmited : ",chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
#        time.sleep(100 / 1000)
        # print("disconnect")
        return "ok"

    def connect_user(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x01'  # код запроса
        chunk += b'\x01'  # код уровня доступа
        chunk += b'\x01'  # 1 символ пароля
        chunk += b'\x01'  # 2 символ пароля
        chunk += b'\x01'  # 3 символ пароля
        chunk += b'\x01'  # 4 символ пароля
        chunk += b'\x01'  # 5 символ пароля
        chunk += b'\x01'  # 6 символ пароля
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
#        time.sleep(100 / 1000)
        # print("connect")

    def connect_admin(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x01'  # код запроса
        chunk += b'\x02'  # код уровня доступа
        chunk += b'\x02'  # 1 символ пароля
        chunk += b'\x02'  # 2 символ пароля
        chunk += b'\x02'  # 3 символ пароля
        chunk += b'\x02'  # 4 символ пароля
        chunk += b'\x02'  # 5 символ пароля
        chunk += b'\x02'  # 6 символ пароля
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
#        time.sleep(100 / 1000)
        # print("connect")

    def get_FW_version(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        zver = list(ver)
        lengzver = len(zver)
        a1 = zver[lengzver - 3]
        a2 = zver[lengzver - 4]
        a3 = zver[lengzver - 5]
        ver1 = int(a1)
        ver2 = int(a2)
        ver3 = int(a3)
        version = str(ver3) + "." + str(ver2) + "." + str(ver1)
        # print(zver)
        # print(version)
        return version

    def get_active_energy_current_day(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\x40'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        print(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(19)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-16])[-1:]
            b2 = (outa[:-17])[-1:]
            b3 = (outa[:-14])[-1:]
            b4 = (outa[:-15])[-1:]
            bs = b1 + b2 + b3 + b4
            Pint = int.from_bytes(bs, "big")
            if Pint == 0:
                return "error"
            P = Pint / 1000
            return P
        time.sleep(5)
        return "crc_false"

    def get_active_energy_current_abc(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\x60'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        print(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(15)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            ba1 = (outa[:-12])[-1:]
            ba2 = (outa[:-13])[-1:]
            ba3 = (outa[:-10])[-1:]
            ba4 = (outa[:-11])[-1:]
            bas = ba1 + ba2 + ba3 + ba4
            Paint = int.from_bytes(bas, "big")
            bb1 = (outa[:-8])[-1:]
            bb2 = (outa[:-9])[-1:]
            bb3 = (outa[:-6])[-1:]
            bb4 = (outa[:-7])[-1:]
            bbs = bb1 + bb2 + bb3 + bb4
            Pbint = int.from_bytes(bbs, "big")
            bc1 = (outa[:-4])[-1:]
            bc2 = (outa[:-5])[-1:]
            bc3 = (outa[:-2])[-1:]
            bc4 = (outa[:-3])[-1:]
            bcs = bc1 + bc2 + bc3 + bc4
            Pcint = int.from_bytes(bcs, "big")
#            if Pint == 0:
#                return "error"
            Pa = Paint / 1000
            Pb = Pbint / 1000
            Pc = Pcint / 1000
            return Pa, Pb, Pc
        time.sleep(5)
        return "crc_false"

    def get_active_energy_last_day(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\xD0'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        za = list(ver)
        # print(za)
        lengza = len(za)
        a0 = za[lengza - 15]
        a1 = za[lengza - 16]
        a2 = za[lengza - 17]
        a3 = za[lengza - 18]
        A = format(a3, 'x') + format(a2, 'x') + format(a0, 'x') + format(a1, 'x')
        P = int(A, 16) / 1000
        return P

    def get_active_energy_phases(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\x60'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        za = list(ver)
        # print(za)
        lengza = len(za)
        a0 = za[lengza - 11]
        a1 = za[lengza - 12]
        a2 = za[lengza - 13]
        a3 = za[lengza - 14]
        A = format(a2, 'x') + format(a3, 'x') + format(a0, 'x') + format(a1, 'x')
        PA = int(A, 16) / 1000
        b0 = za[lengza - 7]
        b1 = za[lengza - 8]
        b2 = za[lengza - 9]
        b3 = za[lengza - 10]
        B = format(b2, 'x') + format(b3, 'x') + format(b0, 'x') + format(b1, 'x')
        PB = int(B, 16) / 1000
        c0 = za[lengza - 3]
        c1 = za[lengza - 4]
        c2 = za[lengza - 5]
        c3 = za[lengza - 6]
        C = format(c2, 'x') + format(c3, 'x') + format(c0, 'x') + format(c1, 'x')
        PC = int(C, 16) / 1000
        return PA, PB, PC

    def get_parametres(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x01'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        zver = list(ver)
        lengzver = len(zver)
        isp1 = zver[lengzver - 3]
        isp2 = zver[lengzver - 4]
        isp3 = zver[lengzver - 5]
        isp4 = zver[lengzver - 6]
        isp5 = zver[lengzver - 7]
        isp6 = zver[lengzver - 8]
        ver1 = zver[lengzver - 9]
        ver2 = zver[lengzver - 10]
        ver3 = zver[lengzver - 11]
        var1 = int(isp1)
        var2 = int(isp2)
        var3 = int(isp3)
        var4 = int(isp4)
        var5 = int(isp5)
        var6 = int(isp6)
        vers1 = int(ver1)
        vers2 = int(ver2)
        vers3 = int(ver3)
        # version = str(ver3) + "." + str(ver2) + "." + str(ver1)
        # print(zver)
        # print(version)
        return zver

    def get_time(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x04'  # код запроса
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        tim = ser.read_all()
        return tim

    def get_fw_crc(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x26'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        fw_crc = ser.read_all()
        return fw_crc

    def get_porog(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x21'  # № параметра
        chunk += b'\x03'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        porog = ser.read_all()
        # print(porog)
        return porog

    def get_sn(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(1)
        sn = ser.read_all()
        sn = list(sn)
        lengsn = len(sn)
        a1 = sn[lengsn - 6]
        a2 = sn[lengsn - 7]
        a3 = sn[lengsn - 8]
        a4 = sn[lengsn - 9]
        a5 = sn[lengsn - 5]
        a6 = sn[lengsn - 4]
        a7 = sn[lengsn - 3]
        sn1 = int(a1)
        sn2 = int(a2)
        sn3 = int(a3)
        sn4 = int(a4)
        sn = str(sn4) + str(sn3) + str(sn2) + str(sn1)
        md1 = int(a5)
        md2 = int(a6)
        md3 = int(a7)
        manufacture_date = str(md1) + "." + str(md2) + "." + str(md3)
        return sn, manufacture_date

    def get_temp(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x70'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        temp = ser.read(6)
        if temp[-2:] == self.crc16(temp[:-2])[-2:]:
#            print ('Check CRC:', temp[-2:] == self.crc16(temp[:-2])[-2:])
            za = list(temp)
            temp = int(za[2]) / 10
            return temp
        return "crc_false"

    def get_caseopen(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x04'  # код запроса
        chunk += b'\x12'  # № параметра
        chunk += b'\x00'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        open = ser.read_all()
        open = list(open)
        lengopen = len(open)
        clYY = open[lengopen - 3]
        clYY = format(clYY, 'x')
        clMM = open[lengopen - 4]
        clMM = format(clMM, 'x')
        clDD = open[lengopen - 5]
        clDD = format(clDD, 'x')
        clhh = open[lengopen - 6]
        clhh = format(clhh, 'x')
        clmm = open[lengopen - 7]
        clmm = format(clmm, 'x')
        clss = open[lengopen - 8]
        clss = format(clss, 'x')
        openYY = open[lengopen - 9]
        openYY = format(openYY, 'x')
        openMM = open[lengopen - 10]
        openMM = format(openMM, 'x')
        openDD = open[lengopen - 11]
        openDD = format(openDD, 'x')
        openhh = open[lengopen - 12]
        openhh = format(openhh, 'x')
        openmm = open[lengopen - 13]
        openmm = format(openmm, 'x')
        openss = open[lengopen - 14]
        openss = format(openss, 'x')

        return "case opened : ", openhh, openmm, openss, openYY, openMM, openDD, "\rn", "case closed : ", clhh, clmm, clss, clYY, clMM, clDD

    def get_frequency(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x40'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            frequencyint = int.from_bytes(bs, "big")
            if frequencyint == 1330:
                return "error"
            frequency = frequencyint / 100
            return frequency
        time.sleep(5)
        return "crc_false"

    # for mercury 234
#    def get_aux_fast(self):
#        chunk = self.addr  # сетевой адрес
#        chunk += b'\x08'
#        chunk += b'\x16'
#        chunk += b'\xA0'
#        chunk = self.crc16(chunk)
#        ser = self.open_port(self.ipaddress1, self.ipport1)
#        ser.write(chunk)
#        time.sleep(100 / 1000)
#        outdata = ser.read_all()
#        print(outdata)

        # return outdata

    # запрос напряжения
    def get_voltage_A(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x11'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Vint = int.from_bytes(bs, "big")
            if Vint == 1330:
                return "error"
            voltage_A = Vint / 100
            return voltage_A
        time.sleep(5)
        return "crc_false"

    def get_voltage_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x12'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Vint = int.from_bytes(bs, "big")
            if Vint == 1330:
                return "error"
            voltage_B = Vint / 100
            return voltage_B
        time.sleep(5)
        return "crc_false"

    def get_voltage_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x13'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Vint = int.from_bytes(bs, "big")
            if Vint == 1330:
                return "error"
            voltage_C = Vint / 100
            return voltage_C
        time.sleep(5)
        return "crc_false"

    def get_current_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x21'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Iint = int.from_bytes(bs, "big")
            if Iint == 1330:
                return "error"
            current_A = Iint / 1000
            return current_A
        time.sleep(5)
        return "crc_false"

    def get_current_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x22'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Iint = int.from_bytes(bs, "big")
            if Iint == 1330:
                return "error"
            current_B = Iint / 1000
            return current_B
        time.sleep(5)
        return "crc_false"

    def get_current_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x23'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-2])[-1:]
            b2 = (outa[:-3])[-1:]
            bs = b1 + b2
            Iint = int.from_bytes(bs, "big")
            if Iint == 1330:
                return "error"
            current_C = Iint / 1000
            return current_C
        time.sleep(5)
        return "crc_false"

    def get_P(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            Pint = int.from_bytes(bs, "big")
            if Pint == 1330:
                return "error"
            P = Pint / 100
            return P
        time.sleep(5)
        return "crc_false"

    def get_P_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x01'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            PAint = int.from_bytes(bs, "big")
            if PAint == 1330:
                return "error"
            PA = PAint / 100
            return PA
        time.sleep(5)
        return "crc_false"

    def get_P_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x02'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            PBint = int.from_bytes(bs, "big")
            if PBint == 1330:
                return "error"
            PB = PBint / 100
            return PB
        time.sleep(5)
        return "crc_false"

    def get_P_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            PCint = int.from_bytes(bs, "big")
            if PCint == 1330:
                return "error"
            PC = PCint / 100
            return PC
        time.sleep(5)
        return "crc_false"

    def get_Q(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x04'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            Qint = int.from_bytes(bs, "big")
            if Qint == 1330:
                return "error"
            Q = Qint / 100
            return Q
        time.sleep(5)
        return "crc_false"

    def get_Q_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x05'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            QAint = int.from_bytes(bs, "big")
            if QAint == 1330:
                return "error"
            QA = QAint / 100
            return QA
        time.sleep(5)
        return "crc_false"

    def get_Q_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x06'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            QBint = int.from_bytes(bs, "big")
            if QBint == 1330:
                return "error"
            QB = QBint / 100
            return QB
        time.sleep(5)
        return "crc_false"

    def get_Q_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x07'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            QCint = int.from_bytes(bs, "big")
            if QCint == 1330:
                return "error"
            QC = QCint / 100
            return QC
        time.sleep(5)
        return "crc_false"

    def get_S(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x08'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            Sint = int.from_bytes(bs, "big")
            if Sint == 1330:
                return "error"
            S = Sint / 100
            return S
        time.sleep(5)
        return "crc_false"

    def get_S_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x09'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            SAint = int.from_bytes(bs, "big")
            if SAint == 1330:
                return "error"
            SA = SAint / 100
            return SA
        time.sleep(5)
        return "crc_false"

    def get_S_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x0a'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            SBint = int.from_bytes(bs, "big")
            if SBint == 1330:
                return "error"
            SB = SBint / 100
            return SB
        time.sleep(5)
        return "crc_false"

    def get_S_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x0b'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.3
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
        if outa[-2:] == self.crc16(outa[:-2])[-2:]:
            b1 = (outa[:-4])[-1:]
            b1int = int.from_bytes(b1, "big") & 0b00111111
            b1 = b1int.to_bytes(1, 'big')
            b2 = (outa[:-2])[-1:]
            b3 = (outa[:-3])[-1:]
            bs = b1 + b2 + b3
            SCint = int.from_bytes(bs, "big")
            if SCint == 1330:
                return "error"
            SC = SCint / 100
            return SC
        time.sleep(5)
        return "crc_false"

# merc = Mercury230(address, port)
# m230a = Mercury230(91, 'COM3')
# m230a.connect_user()
# print(m230a.get_Q_A())
# print("Серийный номер : ", m230a.get_sn()[0])
# print("Дата изготовления : ", m230a.get_sn()[1])
# # print(m230a.get_FW_version())
# m230a.disconnect()
