# docker build -t test/python36 .
# docker run -it --rm --name python -v /Users/shinichi/GitHub/nLogAggregation:/mycode test/python36 /bin/bash

FROM python:3.6
RUN pip install schedule
RUN mkdir /mycode