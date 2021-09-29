FROM python:3.9-slim-buster
ADD cluster.py /
RUN pip3 install Flask
RUN pip3 install apscheduler
RUN pip3 install requests
RUN pip3 install numpy
EXPOSE 5000
CMD [ "python3", "./cluster.py" ]