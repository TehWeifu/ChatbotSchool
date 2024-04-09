# Installation (local Windows development)

1. Install Python 3.9.13
2. (Optional) Create a virtual environment
3. Install the required packages `pip install -r requirements.txt`
4. Download the Spanish model `es_core_news_md` with `python -m spacy download es_core_news_md`
5. Train the model with `rasa train`

# Deployment to AWS

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

# Useful commands

* Launch RASA server: `rasa run -m models --enable-api --cors "*" --debug`
