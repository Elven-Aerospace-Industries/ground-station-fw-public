# Development setup

## qt5 setup
```
sudo apt install qttools5-dev-tools
pip3 install pyqt5 --break-system-packages
```
## Using the designer
If the designer doesn't open using the normal method, use the following command
```
qtchooser -run-tool=designer -qt=5
```
Convert design to python using
```
pyuic5 -x client.ui -o client.py
```
## Programming
When using while loops, put the following in the loop to prevent freezing (only for while loops that consume very little time each cycle)
```
app.processEvents()
```