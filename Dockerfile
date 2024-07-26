FROM python:3.12.2

WORKDIR /app

COPY ./requirements /app/requirements

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY . /app

RUN apt-get update && apt-get install -y wget unzip ** \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

CMD ["fastapi", "run", "main.py", "--port", "80"]