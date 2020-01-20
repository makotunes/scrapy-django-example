#!/bin/bash

#DIR=/usr/src/app/mysite/nutrition/migrations

if [[ -d /usr/src/app/mysite/nutrition/migrations ]]; then
    ./uwsgi.sh
else
    ./setup.sh
    ./uwsgi.sh
fi
