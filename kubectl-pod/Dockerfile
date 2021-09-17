FROM python:3.9-alpine
RUN apk update && apk add curl git
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.22.1/bin/linux/amd64/kubectl
RUN chmod u+x kubectl && mv kubectl /bin/kubectl
ADD config /root/.kube/config
#ADD bin/gcloud /usr/lib/google-cloud-sdk/bin/gcloud

ADD kubectl.py /
#COPY . /app
#WORKDIR /app
RUN pip3 install Flask
EXPOSE 5001
CMD [ "python3", "./kubectl.py" ]
#ENV FLASK_APP=kubectl.py
#CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5001"]
#CMD ["kubectl", "top", "nodes"]