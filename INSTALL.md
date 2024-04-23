# Subparse - Installation Guide (Ubuntu)


## Update And Upgrade System 
---

```
sudo apt update && sudo apt upgrade -y
```

## Vim 
--- 
```
sudo apt install vim
```

## Git
---
```
sudo apt install git
```

## Clone Repository
---
```
git clone https://github.com/jstrosch/subparse.git
```

## NPM
---
```
sudo apt install npm
```

## Install Python3 Pip
```
sudo apt install python3-pip
```

## Install Python3 TK
```
sudo apt install python3-tk
```

## Docker Installation
---
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

## Update The System Again
---

```
sudo apt update 
```

## Install Docker
---

```
sudo apt install docker-ce -y
```

## Docker Check 
---

Check to make sure that docker process is running and enabled for boot when the system starts.
```
sudo systemctl status docker
```

To allow for the use of docker without using sudo for docker activities, add your username to the Docker Group.
Note: The docker group grants privileges equivalent to the root user. For details on how this impacts security in your system, see Docker Daemon Attack Surface.. (https://docs.docker.com/engine/security/#docker-daemon-attack-surface)

```
sudo usermod -aG docker ${USER}
```

## Modify Hosts Systemctl File
---
```
sudo vim /etc/sysctl.conf
```

At the bottom of the file append the line 

```
vm.max_map_count=262144
```

To save the file:  `:wq`

<br/>

---
## ! Reboot The System !
---

<br/>

## Install Docker-Compose 
---
```
sudo apt install docker-compose 
```
## Update Pip
---
update pip to the newest version

```
python3.8 -m pip install --upgrade pip
```

## Install Python Requirements
--- 
navigate into the `parser` folder and run the command below to install the requirements

```
python3.8 -m pip install -r requirements.txt
```

## Install Vue Requirements
--- 
navigate into the `viewer` folder and run the command below to install the requirements

NOTE: There will be some deprecated warnings, it is okay to ignore them

```
npm install --legacy-peer-deps
```

## DONE
---
After this the system should be ready to build the containers and run the program.

## Building the container(s) 
---
At the root of the project run the command below 

```
docker-compose up -d --build
```

## View The Site
---

```
http://localhost:8080
```