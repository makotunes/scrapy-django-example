#!/bin/sh

#set -eu
#trap catch ERR
#function catch {
#    ./uwsgi.sh
#}


until python mysite/manage.py makemigrations nutrition
do
  sleep 2
done

#sleep 10s

until python mysite/manage.py migrate
do
  sleep 2
done

#UN="root"
UN=${DJANGO_ADMIN_USERNAME}
#PW="initpass"
PW=${DJANGO_ADMIN_PASSWORD}
#EM="root@example.co.jp"
EM=${DJANGO_ADMIN_EMAIL}

expect -c "
spawn python mysite/manage.py createsuperuser

set timeout 2

expect \"Username (leave blank to use 'root'):\"
send \"${UN}\n\"

expect \"Email address:\"
send \"${EM}\n\"

expect \"Password:\"
send \"${PW}\n\"

expect \"Password (again):\"
send \"${PW}\n\"

expect \"Password (again):\"
exit 0
"

#./uwsgi.sh




