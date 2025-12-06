# Do not run this code directly, instead insert it into client.py

from time import sleep
from groundStationClientBackend import backend
be = backend()




        def connectSerial():
            be.serial_port_number = self.serialPort_lineEdit.text()
            be.connectSerial()
            while 1:
                app.processEvents()
                be.recvSerial()
                # Printing to serial console
                if (len(be.print_queue) > 0):
                    self.serialConsoleOutputTextEdit.append(be.print_queue[0])
                    print(be.print_queue[0])
                    be.print_queue.pop(0)
                # Updating status
                self.serialPortStatusLable.setText(be.serial_status)
                self.groundRadioStatusLable.setText(be.radio_status)
                self.rssiLCD.display(be.rssi)
                self.barometricAltitudeLCD.display(be.barometric_alt)
                self.totalAccelerationLCD.display(be.total_acceleration)
                self.uptimeLCD.display(be.uptime)
                self.stateLCD.display(be.state)
                self.mainAdcLCD.display(be.m_chute_adc)
                self.drogueAdcLCD.display(be.d_chute_adc)
                self.GPSlatLCD.display(be.GPSlat)
                self.GPSlongLCD.display(be.GPSlong)
                self.packetAgeLCD.display(be.packet_age)
                self.maxAltitudeLCD.display(be.maxAlt)
                self.maxAccelerationLCD.display(be.maxAcceleration)
                # Update configurator
                if (self.writeConfigCheckbox.checkState() == 0):
                    self.launch_t_alt_lineEdit.setText(be.config_launch_t_alt)
                    self.launch_t_gee_lineEdit.setText(be.config_launch_t_gee)
                    self.DC_2_delay_lineEdit.setText(be.config_DC_2_delay)
                    self.DC_1_delay_lineEdit.setText(be.config_DC_1_delay)
                    self.radioFreq_lineEdit.setText(be.config_radioFreq)
                    self.mainChuteAlt_lineEdit.setText(be.config_mainChuteAlt)
                    self.ctest_lineEdit.setText(be.config_ctest)
                    self.apogee_delay_lineEdit.setText(be.config_apogee_delay)
        self.serialPortConnectButton.clicked.connect(connectSerial)

        def sendmsg():
            be.sendSerial(self.serialConsoleInput_lineEdit.text())
        self.serialConsoleSend.clicked.connect(sendmsg)

        def connectRadio():
            be.sendSerial(self.groundRadioFreq_lineEdit.text())
        self.groundRadioConnectButton.clicked.connect(connectRadio)

        def readConfig():
            be.sendSerial("read-config  ")
        self.readConfigButton.clicked.connect(readConfig)

        def writeConfig():
            try:
                if not(self.launch_t_gee_lineEdit.text() == ""):
                    str(float(self.launch_t_gee_lineEdit.text().replace(" ", "")))
                if not(self.launch_t_alt_lineEdit.text() == ""):
                    str(float(self.launch_t_alt_lineEdit.text().replace(" ", "")))
                if not(self.DC_1_delay_lineEdit.text() == ""):
                    str(float(self.DC_1_delay_lineEdit.text().replace(" ", "")))
                if not(self.DC_2_delay_lineEdit.text() == ""):
                    str(float(self.DC_2_delay_lineEdit.text().replace(" ", "")))
                if not(self.radioFreq_lineEdit.text() == ""):
                    str(float(self.radioFreq_lineEdit.text().replace(" ", "")))
                if not(self.mainChuteAlt_lineEdit.text() == ""):
                    str(float(self.mainChuteAlt_lineEdit.text().replace(" ", "")))
                if not(self.ctest_lineEdit.text() == ""):
                    str(float(self.ctest_lineEdit.text().replace(" ", "")))
                if not(self.apogee_delay_lineEdit.text() == ""):
                    str(float(self.apogee_delay_lineEdit.text().replace(" ", "")))

                if not(self.launch_t_gee_lineEdit.text() == ""):
                    be.sendSerial("write-flash config launch_t_gee=" + str(float(self.launch_t_gee_lineEdit.text().replace(" ", ""))) + '\n')  # converted to float so as to add the .00 at the end of the number
                    sleep(0.1)
                if not(self.launch_t_alt_lineEdit.text() == ""):
                    be.sendSerial("write-flash config launch_t_alt=" + str(float(self.launch_t_alt_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.DC_1_delay_lineEdit.text() == ""):
                    be.sendSerial("write-flash config DC_1_delay=" + str(float(self.DC_1_delay_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.DC_2_delay_lineEdit.text() == ""):
                    be.sendSerial("write-flash config DC_2_delay=" + str(float(self.DC_2_delay_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.radioFreq_lineEdit.text() == ""):
                    be.sendSerial("write-flash config radioFreq=" + str(float(self.radioFreq_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.mainChuteAlt_lineEdit.text() == ""):
                    be.sendSerial("write-flash config mainChuteAlt=" + str(float(self.mainChuteAlt_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.ctest_lineEdit.text() == ""):
                    be.sendSerial("write-flash config ctest=" + str(float(self.ctest_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                if not(self.apogee_delay_lineEdit.text() == ""):
                    be.sendSerial("write-flash config apogee_delay=" + str(float(self.apogee_delay_lineEdit.text().replace(" ", ""))) + '\n')
                    sleep(0.1)
                sleep(1)
                be.sendSerial("reboot  ")
                Dialog.setWindowTitle("Config written, please close and re-open the ground station client")
                be.print_queue.append("Config written, please close and re-open the ground station client")
            except ValueError:
                be.print_queue.append("Error setting config, all configs must be a number")
        self.writeConfigButton.clicked.connect(writeConfig)

        def ejectionTest():
            if not(self.mainArmCheckBox.checkState() == 0) and not(self.drogueArmCheckBox.checkState() == 0):
                be.print_queue.append("Can only fire one channel at a time")
            elif not(self.mainArmCheckBox.checkState() == 0):
                be.sendSerial("FIRE_2_TWO")
            elif not(self.drogueArmCheckBox.checkState() == 0):
                be.sendSerial("FIRE_1_ONE")
        self.ejectionFireButton.clicked.connect(ejectionTest)

        def factoryReset():
            if (self.factoryReset_horizontalScrollBar.value() > 80):
                Dialog.setWindowTitle("Reverting to factory settings, do not disconnect the flight computer, this can take 15 seconds")
                be.print_queue.append("Reverting to factory settings, do not disconnect the flight computer, this can take 15 seconds")
                be.sendSerial("rm config ")
                sleep(5)
                be.sendSerial("rm flight ")
                sleep(5)
                be.sendSerial("reboot  ")
                Dialog.setWindowTitle("Reverted to factory settings, please close and re-open the ground station client")
                be.print_queue.append("Reverted to factory settings, please close and re-open the ground station client")
            else:
                be.print_queue.append("Factory reset will DELETE all configs and flights on the flight computer, slide the bar to the right to confirm")
        self.factoryResetButton.clicked.connect(factoryReset)
