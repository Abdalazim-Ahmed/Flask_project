
import os
import secrets
from . import app
from PIL import Image

def save_image(image, path, out_size=None):
    random_hex = secrets.token_hex(8)
    _, img_ext = os.path.splitext(image.filename)
    img_name = random_hex + img_ext
    img_path = os.path.join(app.root_path, path, img_name)
    i = Image.open(image)
    if out_size:
     i.thumbnail(out_size)
     i.save(img_path)
    return img_name
