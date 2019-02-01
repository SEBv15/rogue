FROM ubuntu:18.04

# Install system tools
RUN apt-get update && apt-get -y    install wget git \
                                    cmake python3 python3-dev libboost-all-dev \
                                    libbz2-dev python3-pip libzmq3-dev python3-pyqt5 \
                                    libreadline6-dev

# Install EPICS
RUN mkdir -p /usr/src/epics/base-3.15.5
WORKDIR /usr/src/epics/base-3.15.5
RUN wget -O base-3.15.5.tar.gz https://epics.anl.gov/download/base/base-3.15.5.tar.gz
RUN tar xzf base-3.15.5.tar.gz --strip 1
RUN make clean && make && make install
ENV EPICS_BASE /usr/src/epics/base-3.15.5

# PIP Packages
RUN pip3 install PyYAML Pyro4 parse click ipython pyzmq packaging matplotlib numpy pyepics

# Install Rogue
ARG branch
WORKDIR /usr/src
RUN git clone https://github.com/slaclab/rogue.git -b $branch
WORKDIR rogue
RUN mkdir build
WORKDIR build
RUN cmake .. -DROGUE_INSTALL=system
RUN make install