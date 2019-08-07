import matplotlib.pyplot as plt
import matplotlib.image as img
import image
import random


def run():
    # image = img.imread('./samples/people.jpg')
    image = img.imread('./samples/me.jpg')
    # image = img.imread('./samples/landmark.jpg')

    print('copying image...')
    image = image.copy()

    dirty_percent = 100
    pixels = image.shape[0] * image.shape[1]
    dirty = round(pixels * (dirty_percent * 2 / 100))
    print('dirtying image ({}% - total pixels: {} - pixels to dirty: {})...'.format(dirty_percent, pixels, dirty))
    for i in range(dirty):
        dirty_image(image)

    print('getting horizontal bad points...')
    bad_points_h = get_points(image, [0, 0, 0], 'h')

    print('getting vertical bad points...')
    bad_points_v = get_points(image, [0, 0, 0], 'v')

    print('plotting dirty image...')
    fig = plt.figure(2)
    plt.imshow(image)

    print('horizontal interpolating...')
    for bp in bad_points_h:
        qty = bp[2]
        if bp[3] != '' or qty == image.shape[1] - 1:
            continue

        y = bp[0]
        x_1 = bp[1] - 1
        x_2 = bp[1] + qty

        y_1 = image[y][x_1]
        y_2 = image[y][x_2]
        interpolation = inter(x_1, y_1, x_2, y_2, qty)
        for i in range(len(interpolation)):
            image[y][x_1 + 1 + i] = interpolation[i]

    for bp in bad_points_h:
        type_oper = bp[3]
        if type_oper == '':
            continue

        qty = bp[2]
        y = bp[0]
        x_1 = bp[1] - 1
        x_2 = bp[1] + qty

        if type_oper == 'extra_neg':
            x_2 += 1
            x_1 = x_2 - 1
        elif type_oper == 'extra_pos':
            x_1 -= 1
            x_2 = x_1 + 1

        y_1 = image[y][x_1]
        y_2 = image[y][x_2]
        interpolation = inter(x_1, y_1, x_2, y_2, qty, type_oper)
        for i in range(len(interpolation)):
            if type_oper == 'extra_neg':
                image[y][x_1 - 1 - i] = interpolation[i]
            elif type_oper == 'extra_pos':
                image[y][x_2 + 1 + i] = interpolation[i]

    print('vertical interpolating...')
    for bp in bad_points_v:
        if bp[3] != '':
            continue

        qty = bp[2]
        y = bp[1]
        x_1 = bp[0] - 1
        x_2 = bp[0] + qty
        y_1 = image[x_1][y]
        y_2 = image[x_2][y]
        interpolation = inter(x_1, y_1, x_2, y_2, qty)
        for i in range(len(interpolation)):
            rgb_h = image[x_1 + 1 + i][y]
            rgb_v = interpolation[i]
            image[x_1 + 1 + i][y] = [(rgb_h[0] + rgb_v[0])/2,
                                     (rgb_h[1] + rgb_v[1])/2, (rgb_h[2] + rgb_v[2])/2]

    for bp in bad_points_v:
        type_oper = bp[3]
        qty = bp[2]
        if type_oper == '':
            continue

        y = bp[1]
        x_1 = bp[0] - 1
        x_2 = bp[0] + qty

        if type_oper == 'extra_neg':
            x_2 += 1
            x_1 = x_2 - 1
        elif type_oper == 'extra_pos':
            x_1 -= 1
            x_2 = x_1 + 1

        y_1 = image[x_1][y]
        y_2 = image[x_2][y]
        interpolation = inter(x_1, y_1, x_2, y_2, qty, type_oper)
        for i in range(len(interpolation)):
            if type_oper == 'extra_neg':
                rgb_h = image[x_1 - 1 - i][y]
                rgb_v = interpolation[i]
                image[x_1 - 1 - i][y] = [(rgb_h[0] + rgb_v[0])/2,
                                         (rgb_h[1] + rgb_v[1])/2, (rgb_h[2] + rgb_v[2])/2]
            elif type_oper == 'extra_pos':
                rgb_h = image[x_2 + 1 + i][y]
                rgb_v = interpolation[i]
                image[x_2 + 1 + i][y] = [(rgb_h[0] + rgb_v[0])/2,
                                         (rgb_h[1] + rgb_v[1])/2, (rgb_h[2] + rgb_v[2])/2]

    print('plotting vertical + horizontal interpolated image...')
    fig = plt.figure(3)
    plt.imshow(image)
    plt.show()


def inter(x_1, y_1, x_2, y_2, qty, type_oper='interp'):
    factor = [0]*3
    factor[0] = int(round((int(y_2[0])-int(y_1[0])) / (x_2 - x_1)))
    factor[1] = int(round((int(y_2[1])-int(y_1[1])) / (x_2 - x_1)))
    factor[2] = int(round((int(y_2[2])-int(y_1[2])) / (x_2 - x_1)))
    arr = [None]*qty
    for i in range(qty):
        x = i + x_1 + 1
        if type_oper == 'extra_pos':
            x = i + x_2 + 1
        if type_oper == 'extra_neg':
            x = x_1 - 1 - i

        rgb_h = [0] * 3
        rgb_h[0] = int(y_1[0]) + factor[0] * (x - x_1)
        rgb_h[1] = int(y_1[1]) + factor[1] * (x - x_1)
        rgb_h[2] = int(y_1[2]) + factor[2] * (x - x_1)
        arr[i] = fix_rgb(rgb_h)
    return arr


def fix_rgb(rgb):
    rgb[0] = fix_rgb_color(rgb[0])
    rgb[1] = fix_rgb_color(rgb[1])
    rgb[2] = fix_rgb_color(rgb[2])
    return rgb


def fix_rgb_color(color):
    if color > 255:
        color = 255
    if color < 0:
        color = 0
    return color


def dirty_image(img):
    """dirty image"""
    x, y = random.randint(0, img.shape[0]-1), random.randint(0, img.shape[1]-1)
    img[x, y, :] = 0


def get_points(img, rgb, direction):
    points = []
    point = None
    width = img.shape[1]
    height = img.shape[0]

    qty = 0
    if direction == 'h':
        for y in range(height):
            for x in range(width):
                point, qty = process_point(img, y, x, rgb, points, point,
                              width, height, direction, qty)
    else:
        for x in range(width):
            for y in range(height):
                point, qty = process_point(img, y, x, rgb, points, point,
                              width, height, direction, qty)

    return points


def process_point(img, y, x, rgb, points, point, width, height, direction, qty):
    if (img[y][x] == rgb).all():
        qty += 1
        if point is None:
            point = [y, x]
        if (direction == 'h' and x == width - 1) or (direction == 'v' and y == height - 1):
            point.append(qty)
            point.append('extra_pos')
            points.append(point)
            point = None
            qty = 0
    elif point is not None:
        point.append(qty)
        if point[0] == 0:
            point.append('extra_neg')
        else:
            point.append('')
        points.append(point)
        point = None
        qty = 0

    return point, qty

run()
