# Docker file to create NIC Charts


FROM alpine:latest

RUN apk add --no-cache gcc git python3 python3-dev py3-pip make py3-numpy py3-matplotlib py3-pillow py3-scipy
RUN apk add --no-cache build-base cairo-dev cairo cairo-tools jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip3 install wheel
RUN pip3 install cairosvg networkx pygal

# python-pygal_maps_world python-pycountry python-pypdf2 python-scipy


ENV HOME=/home/nic_network

WORKDIR $HOME
ADD CHANGELOG.md $HOME
ADD LICENSE $HOME
ADD MANIFEST.in $HOME
ADD Makefile $HOME
ADD NICNetwork/* $HOME/NICNetwork/
ADD README.md $HOME
ADD draw_charts.py $HOME
ADD setup.cfg $HOME
ADD setup.py $HOME

ENV IGNORE_VENV=1

# RUN python3 -m venv venv

# RUN /usr/bin/python3 setup.py clean
# RUN /usr/bin/python3 setup.py build
# RUN /usr/bin/python3 setup.py install

RUN make install

ENTRYPOINT ["/usr/bin/python3", "draw_charts.py", "-p",  "/work"]
