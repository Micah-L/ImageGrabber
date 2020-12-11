from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, send_from_directory
import os

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--use-gl=swiftshader')
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"')
options.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

### Utility functions ###
def get_image_urls_in_page(url):
    print(f"URL passed: {url}")
    global driver
    driver.get(url, cookies = cookies)
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
    if url[:4].lower() == 'http':
        pass
    else:
        url = "http://" + url

    images = get_image_urls_in_page(url)
    return render_template("show_images.html", num_images = len(images), images = images)

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 8080))
    app.run(HOST, PORT, debug=True) 
    