import serial
import serial.tools.list_ports
from datetime import *
import pathlib
import os
import time

class backend:
    def __init__(self):
        self.serial_port_number = ""
        self.serial_port_obj = serial.Serial()
        self.print_queue = []
        self.serial_status = "Not connected"
        self.radio_status = "Not connected"
        self.rssi = 0.0
        self.barometric_alt = 0.0
        self.total_acceleration = 0.0
        self.uptime = 0
        self.state = 0
        self.d_chute_adc = 0
        self.m_chute_adc = 0
        self.GPSlat = 0.0
        self.GPSlong = 0.0
        self.packet_timestamp = 0.0
        self.packet_age = 0.0
        self.config_launch_t_gee = ""
        self.config_launch_t_alt = ""
        self.config_DC_1_delay = ""
        self.config_DC_2_delay = ""
        self.config_radioFreq = ""
        self.config_mainChuteAlt = ""
        self.config_ctest = ""
        self.config_apogee_delay = ""
        self.maxAlt = 0.0
        self.maxAcceleration = 0.0
        self.masterLogPath = str(pathlib.Path.home()) + "/Elven_Aerospace_Industries_Logs"
        self.sessionLogPath = self.masterLogPath + "/" + str(datetime.today().strftime('%Y-%m-%d_%H:%M:%S'))
        self.sessionLogPathTelemetry = self.sessionLogPath + "/telemetry.csv"
        self.sessionLogPathDownload = self.sessionLogPath + "/download.csv"
        self.downloadInProgress = False
        self.lastDownloadTime = 0

        print(self.masterLogPath)
        print(self.sessionLogPath)
        print(self.sessionLogPathTelemetry)
        print(self.sessionLogPathDownload)

        if not(os.path.exists(self.masterLogPath)):
            os.mkdir(self.masterLogPath)
        
        if not(os.path.exists(self.sessionLogPath)):
            os.mkdir(self.sessionLogPath)
        
        self.telemetryFileObject = open(self.sessionLogPathTelemetry, "w+")
        print("Recorded on the Elven Aerospace Industries Ground Station Client App", file=self.telemetryFileObject)
        print("uptime,alt,ax,ay,az,acx,acy,acz,lat,lng", file=self.telemetryFileObject)
        self.telemetryFileObject.flush()

        self.downloadFileObject = open(self.sessionLogPathDownload, "w+")

    def connectSerial(self):
        print("Connect to serial port: ", self.serial_port_number)
        self.serial_port_obj.baudrate = 115200
        self.serial_port_obj.port = self.serial_port_number

        try:
            self.serial_port_obj.open()
            self.print_queue.append("Ground Station Client: Serial connected")
            self.serial_status = "Connected"
        except:
            self.print_queue.append("Ground Station Client: Serial connection failed")
            ports = serial.tools.list_ports.comports()
            self.print_queue.append("Ground Station Client: Available serial ports on this PC")
            for port in ports:
                self.print_queue.append("Ground Station Client: " + str(port))

    def recvSerial(self):
        if (self.downloadInProgress == False):
            try:
                if (float(self.barometric_alt) > float(self.maxAlt)):
                    print("test")
                    self.maxAlt = self.barometric_alt
                if (float(self.total_acceleration) > float(self.maxAcceleration)):
                    self.maxAcceleration = self.total_acceleration
                if (self.packet_timestamp == 0):
                    self.packet_age = 0        
                else:
                    self.packet_age = time.time() - self.packet_timestamp
                while self.serial_port_obj.in_waiting:
                    data = str(self.serial_port_obj.readline().decode('utf-8'))
                    self.print_queue.append("APP_RECV: " + data)
                    # Data parsers
                    if ("Radio frequency set to" in data):
                        self.radio_status = "Waiting on FC"
                    elif ("RECV" in data):

                        print(data.replace("RECV:", ""), end="", file=self.telemetryFileObject)
                        self.telemetryFileObject.flush()

                        self.packet_timestamp = time.time()

                        self.radio_status = "Connected"

                        dataList = data.split(",")
                        self.barometric_alt = dataList[1]
                        
                        accleration_x = float(dataList[5]) ** 2
                        accleration_y = float(dataList[6]) ** 2
                        accleration_z = float(dataList[7]) ** 2
                        self.total_acceleration = (accleration_x + accleration_y + accleration_z) ** 0.5
                        
                        self.uptime = int(dataList[0].replace("RECV:", ""))
                        self.state = int(dataList[12])
                        self.d_chute_adc = int(dataList[10])
                        self.m_chute_adc = int(dataList[11])
                        self.GPSlat = float(dataList[8])
                        self.GPSlong = float(dataList[9])

                    elif ("RSSI" in data):
                        self.rssi = int(data.split(":")[1])

                    elif ("launch_t_gee" in data):
                        self.config_launch_t_gee = str(data.split("=")[1])
                    elif ("launch_t_alt" in data):
                        self.config_launch_t_alt = str(data.split("=")[1])
                    elif ("DC_1_delay" in data):
                        self.config_DC_1_delay = str(data.split("=")[1])
                    elif ("DC_2_delay" in data):
                        self.config_DC_2_delay = str(data.split("=")[1])
                    elif ("radioFreq" in data):
                        self.config_radioFreq = str(data.split("=")[1])
                    elif ("mainChuteAlt" in data):
                        self.config_mainChuteAlt = str(data.split("=")[1])
                    elif ("ctest" in data):
                        self.config_ctest = str(data.split("=")[1])
                    elif ("apogee_delay" in data):
                        self.config_apogee_delay = str(data.split("=")[1])
            except:
                pass
        else:
            while self.serial_port_obj.in_waiting:
                self.lastDownloadTime = time.time()
                data = str(self.serial_port_obj.readline().decode('utf-8'))
                print(data, end="", file=self.downloadFileObject)
                self.downloadFileObject.flush()
                self.print_queue.append("Downloaded: " + data)
            if (time.time() - self.lastDownloadTime > 5):
                self.downloadInProgress = False

    def sendSerial(self, msg):
        try:
            self.print_queue.append("APP_SEND: " + msg)
            self.serial_port_obj.write(bytes(msg, 'utf-8'))
        except serial.serialutil.PortNotOpenError:
            self.print_queue.append("Ground Station Client: Serial port not connected")
            ports = serial.tools.list_ports.comports()
            self.print_queue.append("Ground Station Client: Available serial ports on this PC")
            for port in ports:
                self.print_queue.append("Ground Station Client: " + str(port))