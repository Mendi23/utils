
# client setup
sudo apt install xfce4 xfce4-goodies -y
sudo apt install tightvncserver -y

vncserver # create password < 8 chars
vncserver -kill :<num> # <session number>

echo '#!/bin/bash' > ~/.vnc/xstartup
echo 'xrdb $HOME/.Xresources' >> ~/.vnc/xstartup
echo 'startxfce4 &' >> ~/.vnc/xstartup
sudo chmod +x ~/.vnc/xstartup

# host setup
wget https://www.realvnc.com/download/file/viewer.files/VNC-Viewer-6.21.406-Linux-x86.deb
sudo dpkg -i VNC*.deb
sudo apt --fix-broken install

# run client
vncserver

# run host
ssh -L 5901:localhost:5901 [-i <ssh-key>] <user>@<hostname>
vncviewer localhost:5901