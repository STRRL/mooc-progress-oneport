FROM python:2.7
COPY app /app
COPY build /build
COPY pip.conf /root/.pip/pip.conf
RUN ls /root/.pip
RUN pip install -U pip
RUN pip install -r /app/requirements.txt
RUN python /build/build.py
