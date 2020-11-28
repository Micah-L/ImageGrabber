from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, shutil
from flask import Flask, escape, request, render_template, redirect, send_from_directory
import os

def get_image_urls_in_page(url):
    print(f"URL passed: {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    img_elems = driver.find_elements_by_tag_name("img")
    return [img.get_attribute("src") for img in img_elems]

def download_image(image_url):
    size = None
    filename = None
    if image_url:
        filename = image_url.split("?")[0].split("/")[-1]

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                size = f.tell()
            print('Image sucessfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retreived', filename)
    else:
        print('Image Couldn\'t be retreived', image_url)
    return filename, size
def download_images_from_url(url):
    print(f"URL passed: {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    img_elems = driver.find_elements_by_tag_name("img")
    img_urls = [img.get_attribute("src") for img in img_elems]
    images = dict()
    for img in img_urls:
        filename, size = download_image(img)
        images[filename] = size
    return sorted(images.items(), key=lambda item: item[1], reverse=True)    

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')                 
@app.route('/<path:url>')
def do_thing(url):
    print(f"Getting images from: {url}")
    images = get_image_urls_in_page(url)
    return render_template("show_images.html", num_images = len(images), images = images)