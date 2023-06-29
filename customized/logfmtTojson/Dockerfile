FROM python@sha256:2efb4fc6eb1266531d9ac17714c165102bd264ecb8d16cdf6f49bf7c50552ffa
WORKDIR /config
ENV PYTHONUNBUFFERED=1
COPY script.py /config
RUN pip install python-logging-loki
RUN pip install httplib2
CMD [ "python", "-u","/config/script.py", "&"]