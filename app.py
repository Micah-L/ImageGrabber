from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, send_from_directory
import os

### Utility functions ###
def get_image_urls_in_page(url):
    print(f"URL passed: {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    img_elems = driver.find_elements_by_tag_name("img")
    return [img.get_attribute("src") for img in img_elems]
###

app = Flask(__name__)

### Flask Routing ###
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')                 

@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/<path:url>')
def do_thing(url):
    print(f"Getting images from: {url}")
    images = get_image_urls_in_page(url)
    return render_template("show_images.html", num_images = len(images), images = images)