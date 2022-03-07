FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /my_blog
WORKDIR /my_blog

RUN apt-get update -y
RUN /usr/local/bin/python -m pip install --upgrade pip 

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["run.py"]