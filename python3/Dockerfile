FROM centos
EXPOSE 3031 3032 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN yum install -y epel-release
RUN yum install -y expect wget bzip2 unzip vim git mysql-devel gcc-c++ make git psmisc net-tools gcc

RUN wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
#RUN bash Anaconda3-4.2.0-Linux-x86_64.sh

COPY conda.sh /usr/src/app/
RUN bash conda.sh


#COPY requirements.txt /usr/src/app/
#COPY ./ /usr/src/app/
COPY requirements.txt /usr/src/app/
#COPY mkdir mysite


ENV PATH="/root/anaconda3/bin:$PATH"
RUN /root/anaconda3/bin/pip install --upgrade pip
RUN /root/anaconda3/bin/pip install --no-cache-dir -r requirements.txt

#RUN /root/anaconda3/bin/pip install --upgrade django==1.9
COPY ./mysite/ ./mysite/
COPY entrypoint.sh /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
