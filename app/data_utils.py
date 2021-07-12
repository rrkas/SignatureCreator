import os
import string
from math import floor
from random import *

import requests

# location of this file
base_dir = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
output_dir = "output"
output_path = os.path.join(base_dir, output_dir)
print(output_path)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# image to show until signature is generated
blank_img_path = os.path.join(base_dir, "blank.jpg")


# configure background of components
def configure_bg(*components):
    for c in components:
        c["bg"] = "white"


# uustv fonts for signature generation
uustv_font_map = {
    "Art Lottery": "1.ttf",
    "Even Signed": "zql.ttf",
    "Business Visa": "8.ttf",
    "Bookmarks": "6.ttf",
    "Cheesy Sign": "bzcs.ttf",
    "Cursive": "lfc.ttf",
    "Row Bookmarks": "2.ttf",
    "Individuality Check": "3.ttf",
    "Cute Sign": "yqk.ttf",
}


# download image from uustv
def download_image(name, font_name=None, size=20, batch_id=None):
    font = (
        uustv_font_map[font_name or "zql.ttf"]
        if font_name
        else list(uustv_font_map.values())[1]
    )
    # print(name, font, size)
    start_url = "http://www.uustv.com/"
    if name == "":
        return None
    else:
        dict_paras = {
            "word": name,
            "sizes": str(size),
            "fonts": font,
            "fontcolor": "#000000",
        }
        result = requests.post(start_url, data=dict_paras)
        result.encoding = "utf-8"
        html = result.text
        image_path = (
            html.split('<div class="tu">')[1]
            .split("</div>")[0]
            .split('="')[1]
            .split('"')[0]
        )
        image_url = start_url + image_path
        response = requests.get(image_url).content
        name = slugify(name).lower()
        if batch_id:
            out_file_path = os.path.join(output_path, batch_id, "{}.gif".format(name))
        else:
            out_file_path = os.path.join(output_path, "{}.gif".format(name))
        with open(out_file_path, "wb") as f:
            f.write(response)
        return out_file_path


# crop the decoration around uustv image
def crop_image(image):
    print(image)


# get file size in user readable format
def pretty_file_size(filepath):
    bytes = os.path.getsize(filepath)
    if bytes < 1024:
        return str(bytes) + " b"
    bytes //= 1024
    if bytes < 1024:
        return str(bytes) + " Kb"
    bytes //= 1024
    if bytes < 1024:
        return str(bytes) + " Mb"
    bytes //= 1024
    if bytes < 1024:
        return str(bytes) + " Gb"


def count_names(filepath):
    c = 0
    try:
        with open(filepath) as f:
            lines = f.readlines()
            for l in lines:
                # print(slugify(l))
                if len(l) > 0:
                    c += 1
    except BaseException as e:
        print(e)
    return c


def slugify(name):
    size = floor(random() * 5) + 5
    chars = string.ascii_lowercase + string.digits
    name = "-".join(name.strip().split(" "))
    return name + "-" + "".join(choice(chars) for _ in range(size))
