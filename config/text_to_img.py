# Returns the generated_image as byte array or returns 'None'
import random
import io
from PIL import Image, ImageDraw, ImageFont

def get_random_image(font_path: str, text:str):
    try:
        return generate_image(text, font_path)
    except Exception as e:
        print(f"unexpected error happened :", e)
        return None


def generate_image(text: str, font_path: str, font_size:int=50):
    width, height = calculate_image_size(text, font_size, font_path)
    image = Image.new("RGB", (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(text, font=font)
    text_height = font_size
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, fill="black", font=font)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    return img_byte_arr.read()


def calculate_image_size(text:str, font_size: int, font_path:str):
    font = ImageFont.truetype(font_path, font_size)
    text_width = int(font.getlength(text))
    # Add some padding to avoid text getting too close to edges
    padding = 100
    image_width = text_width + padding
    image_height = font_size + padding

    return image_width, image_height

'''
if __name__ == '__main__':
    font_path="/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/BPtypewriteStrikethrough.ttf"
    image_data = get_random_image(font_path, 'hello')
    print(image_data)
'''
