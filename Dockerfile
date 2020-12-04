FROM python:3.8
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN apt-get update -y

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# Install Chrome
#RUN apt-get update && apt-get install -y \
#	apt-transport-https \
#	ca-certificates \
#	curl \
#	gnupg \
#	hicolor-icon-theme \
#	libcanberra-gtk* \
#	libgl1-mesa-dri \
#	libgl1-mesa-glx \
#	libpangox-1.0-0 \
#	libpulse0 \
#	libv4l-0 \
#	fonts-symbola \
#	--no-install-recommends \
#	&& curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#	&& echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
#	&& apt-get update && apt-get install -y \
#	google-chrome-stable \
#	--no-install-recommends \
#	&& apt-get purge --auto-remove -y curl \
#	&& rm -rf /var/lib/apt/lists/*
    
 

# RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
# RUN apt-get install -y --fix-missing wget
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install ./google-chrome-stable_current_amd64.deb --fix-missing -y; apt-get -fy install

# RUN apt-get install -y --fix-missing chromium-browser
# RUN alias google-chrome="chromium"

RUN google-chrome --version

RUN pip install pipenv
RUN pip install -r requirements.txt
RUN pipenv install --deploy --system
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app