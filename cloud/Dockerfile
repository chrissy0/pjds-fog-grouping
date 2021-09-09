FROM python:3.9-slim-buster
ADD cloud.py /
COPY . /app
WORKDIR /app
RUN pip3 install Flask
EXPOSE 5000
CMD [ "python3", "./cloud.py" ]