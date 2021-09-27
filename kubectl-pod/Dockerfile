FROM python:3.9-alpine
RUN apk update && apk add curl git
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.22.1/bin/linux/amd64/kubectl
RUN chmod u+x kubectl && mv kubectl /bin/kubectl

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-358.0.0-linux-x86_64.tar.gz --output gcloud.tar.gz
RUN tar -xf gcloud.tar.gz && rm gcloud.tar.gz && ./google-cloud-sdk/install.sh -q
COPY x.json .
RUN ./google-cloud-sdk/bin/gcloud auth activate-service-account ansible-sa@pjds-fog-grouping-326209.iam.gserviceaccount.com --key-file=x.json --project=pjds-fog-grouping-326209

ENV cluster pjds-cluster-1
ENV zone europe-west2-c

RUN pip3 install Flask
EXPOSE 5001

ADD kubectl.py /
CMD ./google-cloud-sdk/bin/gcloud config set compute/zone ${zone} && ./google-cloud-sdk/bin/gcloud container clusters get-credentials ${cluster} --zone ${zone} && python3 kubectl.py ${cluster} ${zone}
