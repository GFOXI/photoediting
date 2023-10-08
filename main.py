import multiprocessing
import time

from PIL import Image, ImageFilter
def blur_image(img, save_name):
    img = Image.open(img)
    return img.filter(ImageFilter.BLUR).save(save_name)

def merge_image(imglist, save_name):

    images = [Image.open(x) for x in imglist]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im.save(save_name+".jpg")

def split_image(img, number, save_name):
    zdjecia = []
    img = Image.open(img)
    width, height = img.size
    unit = width // number
    for n in range(number):
        im1 = img.crop((unit * n, 0, unit * (n + 1), height))
        im1.save(save_name + str(n + 1) + ".jpg")
        zdjecia.append((save_name + str(n + 1) + ".jpg"))
    return zdjecia

if __name__ == '__main__':
    img = input("Podaj nazwe zdjecia z formatem: ")
    try:
        for number in range(1,8):
            zdj = split_image(img, number, "SplittedImg_single")
            p = []
            start = time.time()
            for i in range(number):
                p.append(multiprocessing.Process(target=blur_image(zdj[i],
            "blur_"+zdj[i])))
                p[i].start()
            for i in p:
                i.join()
            zdj2 = ["blur_"+img for img in zdj]
            end = time.time()
            print(number, end - start)
            merge_image(zdj2,"Final")
    except:
        print("Zdjęcie jest niepoprawne")
