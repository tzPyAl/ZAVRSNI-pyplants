from flask import current_app
from flask_login import current_user
from PIL import Image
import secrets
import os
import json
import glob
from random import randint


def read_latest_scrapped_data():
    list_of_scrapped = glob.glob('./scrapped_data/*.json')
    latest_scrap = max(list_of_scrapped, key=os.path.getctime)
    with open(latest_scrap, "r") as jsondata:
        data = json.load(jsondata)
    return data


def save_to_html(name, content):
    html_file = os.path.join('pyplant/templates', name + '.html')
    print(html_file)
    with open(html_file, 'w+') as file:
        file.write(content)


def save_img(form_image, save_dir, size_x, size_y):
    random_hex = secrets.token_hex(12)
    _, file_extension = os.path.splitext(
        form_image.filename)  # using "_" to drop the file name
    img_fn = random_hex + file_extension
    img_path = os.path.join(current_app.root_path, save_dir, img_fn)
    output_size = (size_x, size_y)  # simple resize image to 125x125 px
    temp_image = Image.open(form_image)
    temp_image.thumbnail(output_size)
    temp_image.save(img_path)
    # delete the old user image
    current_img_name, _ = os.path.splitext(current_user.image_file)
    if current_img_name != "default":
        old_img_path = os.path.join(
            current_app.root_path, save_dir, current_user.image_file)
        try:
            os.remove(old_img_path)
        except FileNotFoundError:
            pass  # if i find to way to fetch the old pot image filename, i can delete it here
    return img_fn


def generate_random_status():
    return randint(0, 8)
