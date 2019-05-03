#Grab the latest alpine image
FROM ubuntu:17.10

# Install python and pip
RUN apt update && apt install -y wget && apt install -y bzip2 && apt install -y tree && apt install -y libsm6 libxext6 && apt install -y git-core

RUN apt install -y python3

RUN apt install -y python3-pip

RUN apt-get install -y wget
RUN apt-get -y install cmake

RUN wget https://github.com/libgit2/libgit2/archive/v0.24.0.tar.gz && \
tar xzf v0.24.0.tar.gz && \
cd libgit2-0.24.0/ && \
cmake . && \
make && \
make install

RUN ldconfig
RUN pip3 install pygit2
RUN pip3 install psycopg2-binary

# Add requirements
COPY ./webapp/requirements.txt  /tmp/requirements.txt
WORKDIR /tmp

RUN pip3 install -r requirements.txt

# Add code
COPY ./webapp /opt/webapp/
WORKDIR /opt/webapp

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD ["gunicorn","app:app"] 

