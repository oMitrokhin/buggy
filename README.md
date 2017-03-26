# Buggy

Another lightweight flask-based blog engine.

## Getting started:

### Prerequisites

You need to be installed ```bower```.

### Installation

Clone this repo:  
```sh
git clone https://github.com/true-datura/buggy
```
Cd in cloned directory:  
```sh
cd buggy
```
Create virtualenv, activate it, and install requirements:
```sh
virtualenv -p python3 .env
. .env/bin/activate
pip install -r requirements/dev.txt
```
Install js packages:
```sh
bower install
```
Set up flask environment variables:
```sh
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
```
Create database:
```sh
flask db init
flask db migrate
flask db upgrade
```
Run dev server:
```sh
flask run
```
### Other
You can create superuser by command:
```
flask createadmin
```
To enable Disqus comments edit this lines in `buggy/settings.py`:
```python
DISQUS_SHORTNAME = '<your_shortname'
ENABLE_DISQUS = True
```
