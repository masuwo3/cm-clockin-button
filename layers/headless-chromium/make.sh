#!/bin/bash

mkdir -p python/bin/

# download headless-chrome
if [ ! -f python/bin/headless-chromium ]; then
    curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
    unzip headless-chromium.zip -d python/bin/
    rm headless-chromium.zip
fi

# download webdriver
if [ ! -f python/bin/chromedriver ]; then
    curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
    unzip chromedriver.zip -d python/bin/
    rm chromedriver.zip
fi