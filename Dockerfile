FROM debian
MAINTAINER Artur Vaskovets
RUN apt update -y && apt install -y \
        apache2 \
        libapache2-mod-wsgi-py3 \
        python3-pip \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . /var/www/html/Pysible
RUN chown www-data:www-data -R /var/www/html/Pysible
RUN pip3 install -r /var/www/html/Pysible/requirements.txt
COPY 000-default.conf /etc/apache2/sites-available/
RUN systemctl restart apache2
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV FLASK_APP /var/www/html/Pysible/app.py
EXPOSE 80
WORKDIR /var/www/html/Pysible
COPY ./run.sh /
ENTRYPOINT ["/run.sh"]