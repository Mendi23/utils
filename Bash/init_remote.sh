
# host setup
sudo chmod 600 <ssh key>
mkdir mount_dir

# client setup
sudo apt update
mkdir mount_dir

# connect host
export uip=<user>@<hostname>
ssh [-i <ssh-key>] $uip
sudo sshfs $uip:/home/<user>/mount_dir <local mount_dir> -o IdentityFile=<ssh key> -o allow_other -o nonempty

# disconnect host
sudo umount -f <local mount_dir>

# client vnc setup
sudo apt install xfce4 xfce4-goodies -y
sudo apt install tightvncserver -y

vncserver # create password < 8 chars
vncserver -kill :<num> # <session number>

echo '#!/bin/bash' > ~/.vnc/xstartup
echo 'xrdb $HOME/.Xresources' >> ~/.vnc/xstartup
echo 'startxfce4 &' >> ~/.vnc/xstartup
sudo chmod +x ~/.vnc/xstartup

# host vnc setup
wget https://www.realvnc.com/download/file/viewer.files/VNC-Viewer-6.21.406-Linux-x86.deb
sudo dpkg -i VNC*.deb
sudo apt --fix-broken install

# run client vnc
vncserver

# run host vnc
ssh -L 5901:localhost:5901 [-i <ssh-key>] $uip
vncviewer localhost:5901