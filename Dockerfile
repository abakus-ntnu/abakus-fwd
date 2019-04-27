FROM python:3.6-slim

WORKDIR /app

RUN apt-get update && apt-get install -y texlive-latex-base curl
RUN curl -sSLf https://github.com/openfaas-incubator/of-watchdog/releases/download/0.4.6/of-watchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

ADD ./req.txt /app
RUN pip install -r ./req.txt
ADD . /app

ENV mode="http"
ENV cgi_headers="true"
ENV upstream_url="http://127.0.0.1:5000"
ENV write_debug="true"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

ENV fprocess="python server.py"
CMD ["fwatchdog"]
