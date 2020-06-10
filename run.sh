#!/bin/bash

cd /var/www/html/Pysible/ #flask only works from app folder
flask init_app
/usr/sbin/apache2ctl -D FOREGROUND