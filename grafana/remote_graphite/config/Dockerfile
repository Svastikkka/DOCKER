FROM golang:latest
WORKDIR /app
COPY . .
RUN chmod 4777 -R graphite-remote-adapter
CMD [ "./graphite-remote-adapter", "--graphite.read.url='http://graphite:8080'", "--graphite.write.carbon-address=graphite:2003", "--log.level=debug", "--graphite.write.carbon-transport=tcp" ]
