# based on https://hub.docker.com/r/mliszcz/tango-cs/~/dockerfile/

FROM ubuntu:bionic

MAINTAINER Alexey Buzmakov


ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget python python-pip python-dev python-numpy python-pytango supervisor libtiff-dev && \
    rm -rf /var/lib/apt/lists/*

# ROBO-TOM

COPY requirements_docker.txt /var/www/drivers/requirements_docker.txt
WORKDIR /var/www/drivers/

RUN pip install -r requirements_docker.txt

# motor 
RUN wget http://files.ximc.ru/libximc/libximc-2.9.14-all.tar.gz && tar -zxvf libximc-2.9.14-all.tar.gz && \
    cd ximc-2.9.14/ximc/deb && dpkg -i libximc7_2.9.14-1_amd64.deb libximc7-dev_2.9.14-1_amd64.deb && apt-get install -f

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# detector
RUN wget http://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz && tar -zxvf XIMEA_Linux_SP.tgz && cd package
RUN ln -s /var/www/drivers/package/include /usr/include/m3api
RUN ln -s /var/www/drivers/package/api/X64/libm3api.so* /usr/lib/ &&\
 ln -s /var/www/drivers/package/api/X64/libm3api.so.2 /usr/lib/libm3api.so &&\
 ldconfig

COPY . /var/www/drivers/
RUN cp drivers_supervisord.conf /etc/supervisor/conf.d/

RUN python setup.py build_ext

WORKDIR /var/www/drivers/tango_ds

# EXPOSE 10000

CMD ./add_to_db.py && \
    supervisord -n
 
