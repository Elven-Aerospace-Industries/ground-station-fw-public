# Elven Aerospace Industries (TM) Ground Station Client
Free & open source ground station firmware and software for use with Elven Aerospace Industries (TM) model rocketry avionics products.

## Use as ground station
1. Run client.py
2. Connect the Elven Aerospace Industries (TM) Ground station dongle to the PC, and enter the serial port (e.g. /dev/ttyACM0) under the "Serial Port" section, and click "Connect"
3. Enter the radio frequency (in Hz) of the rocket flight computer under the "Radio Frequency" section, and click "Connect"
4. Telemetry data should be automatically displayed
5. Logs are saved to home directory on the PC (under the "Elven_Aerospace_Industries_Logs" directory), each session will generate a new timestamped subfolder in the "Elven_Aerospace_Industries_Logs" folder
6. All received telemetry will be saved to "telemetry.csv"

## Use as configurator
1. Run client.py
2. Connect the Elven Aerospace Industries (TM) flight computer to the PC, and enter the serial port (e.g. /dev/ttyACM0) under the "Serial Port" section, and click "Connect"
3. Click "Read Configs" to obtain the current configuration parameters
4. To change parameter values, tick "Write mode" and type the value into the text box, and click "Write Config". The flight computer will reboot
5. To reset all parameters back to factory values, do step 1 & 2, then slide the "Slide Right To Reset" slider to the right, and click "Factory Reset", keep in mind this will also erase all flight data stored on the flight computer. The flight computer will reboot

## Downloading flight data from the flight computer
1. Run client.py
2. Connect the Elven Aerospace Industries (TM) flight computer to the PC, and enter the serial port (e.g. /dev/ttyACM0) under the "Serial Port" section, and click "Connect"
3. Click "Download (Wired)" under the "Save Flight Data" section
4. The flight data will be saved to PC_HOME_DIRECTORY/Elven_Aerospace_Industries_Logs/TIMESTAMP/download.csv (the same logging subfolder mentioned in section 1 of this documentation)

## Ejection testing
Due to the complexity of ejection testing, and the variation between each flight computer, the steps are outlined in the datasheets of each Elven Aerospace Industries (TM) flight computers