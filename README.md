# notifBot

If you use Ubuntu 20.04 you can go to ***Quick setup*** and run a script.


## Settings

First, create a Telegram bot.  
Talk to BotFather (https://t.me/botfather) and follow a few simple steps.
BotFather will provide you with a Telegram Bot Token.

Register on ozma.org and create an instance.


## Manually deploy

Clone the reposetory.

Duplicate [app/config_example.json](app/config_example.json) to the new app/config.json file on server by command:

```shell
cp app/config_example.json app/config.json
```

Update [app/config.json](app/config.json)

```shell
sudo nano app/config.json
```

More details in [app/README.md](app/README.md) inside /app folder.

Install docker-compose. 

This deployment uses docker-compose so that services are automatically managed.

Simply use:
```shell
sudo docker-compose up --build
```

Read full instractions here: https://docs.docker.com/engine/reference/commandline/run/.


## Quick setup For Ubuntu 20.04

### First run

```shell
cd ~ &&
sudo rm -rf notifBot/ &&
git clone https://github.com/itgrus/notifBot.git &&
cd ~/notifBot &&
sudo ./quick_ubuntu_20_lts_startup.sh 
```

Answer all questions.
Ask this data from ozma.io developers.

### Rerun

```shell
cd  ~/notifBot &&
git pull && 
sudo ./quick_ubuntu_20_lts_startup.sh -r 
```

### Check logs

```shell
cd  ~/notifBot &&
sudo docker-compose logs
```

### Stop

```shell
cd  ~/notifBot &&
sudo docker-compose down
```
