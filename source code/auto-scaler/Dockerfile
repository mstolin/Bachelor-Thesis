FROM python:3

LABEL maintainer="marcel.pascal.stolin@ipa.fraunhofer.de"

WORKDIR /usr/src/auto_scaler

# Copy the python module
COPY setup.py .
COPY src src/

# Update and install packages
RUN pip3 install -e .

ENTRYPOINT [ "python3", "src/run.py" ]