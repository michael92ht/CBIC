import os

a = [3, 0, 4, 6, 1, 7, 2, 8, 5]


def images_from_folder(image_folder):
    for f in os.listdir(image_folder):
        num = int(f.split('.')[0])
        bit = 0
        if num/100 == 0:
            if num % 100 / 10 == 0:
                bit = 2
            else:
                bit = 1
        newname = "0" * bit + f
        os.rename(os.path.join(image_folder, f), os.path.join(image_folder, newname))

    for f in os.listdir(image_folder):
        bb = f.split('.')[0]
        num = int(f.split('.')[0])
        if num/100 == 4:
            os.remove(os.path.join(image_folder, f))
        elif num/100 > 4:
            newname = str(num - 100) + r".jpg"
            os.rename(os.path.join(image_folder, f), os.path.join(image_folder, newname))
    for f in os.listdir(image_folder):
        num = int(f.split('.')[0])
        newname = "a" + str(a[num/100] * 100 + num % 100) + r".jpg"
        os.rename(os.path.join(image_folder, f), os.path.join(image_folder, newname))
    for f in os.listdir(image_folder):
        newname = f[1:]
        os.rename(os.path.join(image_folder, f), os.path.join(image_folder, newname))
    print "done!"


if __name__ == "__main__":
    image_folder = r"D:\ICBC\dataset"
    images_from_folder(image_folder)

