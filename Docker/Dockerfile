####################################################################################
#### Use base image to compile AlsavoCtrl
####################################################################################
FROM debian AS build

#### Install build dependencies for AlsavoCtrl
RUN apt-get update && \
        apt-get install -y cmake && \
        apt-get install -y make && \
        apt-get install -y g++ && \
        apt-get install -y git
		
#### Copy AlsavoCtrl files to image
RUN git clone https://github.com/strandborg/AlsavoCtrl.git

WORKDIR /AlsavoCtrl

#### Build AlsavoCtrl
RUN mkdir build

WORKDIR /AlsavoCtrl/build

RUN cmake ..
RUN make

####################################################################################
#### Build final image
####################################################################################
FROM debian

#### Define variables
ENV mqtt_server=None
ENV mqtt_server_port=1883
ENV mqtt_server_user=None
ENV mqtt_server_password=None
ENV alsavo_password=pass
ENV alsavo_serial=xxxx
ENV publish_interval=300
ENV log_size=1000

#### Copy files
RUN mkdir app

COPY --from=build \
    ./AlsavoCtrl/build/AlsavoCtrl \
    ./app/
COPY /mqpublish.py /app/mqpublish.py
COPY /app.sh /app/app.sh

RUN chmod u+x /app/app.sh

#### Install dependencies
RUN apt-get update && \
        apt install -y python3-pip && \
	    apt install -y python3-paho-mqtt

#### Set app.sh as image main process
CMD /app/app.sh
