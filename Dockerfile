FROM ubuntu:latest
LABEL authors="fritz"

ENTRYPOINT ["top", "-b"]