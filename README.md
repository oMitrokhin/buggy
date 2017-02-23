1. git clone git@bitbucket.org:true-datura/buggydesk.git
2. cd buggydesk
3. virtualenv -p python3 .env
4. . .env/bin/activate
5. pip install -r requirements/dev.txt
6. bower install
7. export FLASK_APP=autoapp.py
8. export FLASK_DEBUG=1
9. flask db init
10. flask db migrate
11. flask db upgrade
12. flask run