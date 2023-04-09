import numpy as np
from PIL import Image, ImageDraw


def prepare_ava(image):
    img = Image.open(image)
    x, y = img.size
    if x > y and x > 300:
        first = (x - y) // 2
        img = img.crop([first, 0, x - first, y])
        img = img.resize((300, 300))
    elif x > y and 300 - x <= 100:
        first = (x - y) // 2
        img = img.crop([first, 0, x - first, y])
    elif y > x and y > 300:
        first = (y - x) // 2
        img = img.crop([0, first, x, y - first])
        img = img.resize((300, 300))
    elif y > x and 300 - y <= 100:
        first = (y - x) // 2
        img = img.crop([0, first, x, y - first])

    print(img.size)
    height, width = img.size
    lum_img = Image.new('L', [height, width], 0)

    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (height, width)], 0, 360,
                  fill=255, outline="white")
    img_arr = np.array(img)
    lum_img_arr = np.array(lum_img)
    final_img_arr = np.dstack((img_arr, lum_img_arr))
    first = Image.fromarray(final_img_arr)
    first.save('test_1.png', format='png')


