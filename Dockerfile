FROM python:latest
MAINTAINER Sam Hotchkiss <kanakadas.y@gmail.com>

COPY . /src/
WORKDIR /src/
RUN pip install --requirement onosHealthCheck/requirements.txt
WORKDIR /src/states
EXPOSE 8101, 22, 8194
ENTRYPOINT ["python", "/src/onosHealthCheck/onosHealthCheck.py"]
