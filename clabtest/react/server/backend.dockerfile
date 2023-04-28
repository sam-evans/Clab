FROM python:3.11

# Create an application directory
RUN mkdir -p /app

# The /app directory should act as the main application directory
WORKDIR /app

# add and install requirements
COPY requirements.txt .
COPY package.json .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get install npm -y

# Expose $PORT on container.
# We use a varibale here as the port is something that can differ on the environment.
COPY . /app

EXPOSE $PORT

CMD ["npm", "start"]