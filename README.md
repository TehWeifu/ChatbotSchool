# CIPFP Mislata Chatbot

Chatbot for the CIPFP Mislata. This project is based on RASA and uses the Spanish model `es_core_news_md` from spaCy.
Developed by [JulianBSL](https://github.com/TehWeifu) for MIA 2024.

## Installation (local Windows development)

1. Install Python 3.9.13
2. (Optional) Create a virtual environment and activate it
3. Install the required packages `pip install -r requirements.txt`
4. Download the Spanish model `es_core_news_md` with `python -m spacy download es_core_news_md`
5. Train the model (not tracked in VCS) with `rasa train`

## Deployment to AWS

Note: Free tier EC2 instance won't work. Use a t2.medium instance at least.

`sudo yum update -y`

`sudo yum groupinstall "Development Tools" -y`  
`sudo yum install openssl-devel bzip2-devel libffi-devel zlib-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel -y`

`cd /opt`  
`sudo wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz`

`sudo tar xzf Python-3.9.13.tgz`  
`cd Python-3.9.13`  
`sudo ./configure --enable-optimizations`  
`sudo make altinstall`

`sudo /usr/local/bin/python3.9 -m ensurepip`  
`sudo /usr/local/bin/python3.9 -m pip install --upgrade pip`

`sudo /usr/local/bin/pip3.9 install virtualenv`

`cd /path/to/your/project`  
`/usr/local/bin/python3.9 -m virtualenv venv`

`source venv/bin/activate`

Apache configuration:  
`sudo yum update`  
`sudo yum install httpd`  
`sudo systemctl start httpd`  
`sudo systemctl enable httpd`  
`sudo cp webchat.html /var/www/html/`

## Useful commands

Configs:

* Activate the virtual environment: `source venv/bin/activate`
* Deactivate the virtual environment: `deactivate`

RASA:

* Shell: `rasa shell`
* Interactive training: `rasa interactive`
* Train the model: `rasa train`
* Start the action server: `rasa run actions`
* Launch RASA server: `rasa run -m models --enable-api --cors "*" --debug`
