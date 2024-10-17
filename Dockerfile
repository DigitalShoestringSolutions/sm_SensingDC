# ----------------------------------------------------------------------
#
#    Dockerfile script -- This file is part of the Sensing Data Collection 
#    Service Module distribution. It contains all the commands needed to 
#    assemble an image of the solution on a Raspberry Pi
#
#    Copyright (C) 2022  Shoestring and University of Cambridge
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ----------------------------------------------------------------------

# The python:3.11.2 base image is usually preferred, but (rpi-)lgpio can't be installed from it.
# From this ubuntu base image, (rpi-)lgpio can.
FROM ubuntu:23.04
RUN apt update
RUN apt install -y python3-pip # ubuntu base image lacks pip

# Install standard pip dependencies from requirements file. 
COPY ./requirements.txt /
# --break-system-packages is required with the ubuntu base image. 
# It doesn't actually install globally (check your pip list after running this) but this option does avert the PEP668 error.
RUN pip install -r requirements.txt --break-system-packages

# Manually bust the cache. Nothing below this line will be cached.
ADD http://date.jsontest.com /etc/builddate

# Install user pip dependencies from requirements file.
COPY ./config/requirements.txt /user_requirements.txt
RUN pip install -r user_requirements.txt --break-system-packages

# Add both code/ and config/ to the Docker container. 
# Files inside believe they are in the same directory and can import each other freely.
WORKDIR /app
# ADDing ./code could be above the cache bust - but marginal optimisation not worth the times I have to prune everything when I want to rebuild ./code.
ADD ./code /app
ADD ./config /app

CMD ["python3", "/app/main.py"]
