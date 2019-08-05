import matplotlib.pyplot as plt
import matplotlib.image as img
import image
import random

def run():
    image = img.imread('./samples/people.jpg')
    # image = img.imread('./samples/landmark.jpg')

    print('copying image...')
    image = image.copy()

    dirty_percent = 30
    pixels = image.shape[0] * image.shape[1]
    dirty = round(pixels * (dirty_percent * 2 / 100))
    print('dirtying image ({}% - total pixels: {} - pixels to dirty: {})...'.format(dirty_percent, pixels, dirty))
    for i in range(dirty):
        dirty_image(image)  

    print('getting horizontal bad points...')
    bad_points_h = get_points(image, [0,0,0], 'h')

    print('getting vertical bad points...')
    bad_points_v = get_points(image, [0,0,0], 'v')
            
    print('plotting dirty image...')
    fig = plt.figure(2)
    plt.imshow(image)

    print('horizontal interpolating...')
    for bp in bad_points_h:
        qty = bp[2]
        y = bp[0]
        x_1 = bp[1] - 1
        x_2 = bp[1] + qty
        y_1 = image[y][x_1]
        y_2 = image[y][x_2]
        interpolation = inter(x_1, y_1, x_2, y_2)
        for i in range(len(interpolation)):
            image[y][x_1 + 1 + i] = interpolation[i]

    print('vertical interpolating...')
    for bp in bad_points_v:
        qty = bp[2]
        y = bp[1]
        x_1 = bp[0] - 1
        x_2 = bp[0] + qty
        y_1 = image[x_1][y]
        y_2 = image[x_2][y]
        interpolation = inter(x_1, y_1, x_2, y_2)
        for i in range(len(interpolation)):
            rgb_h = image[x_1 + 1 + i][y]
            rgb_v = interpolation[i]
            image[x_1 + 1 + i][y] = [(rgb_h[0] + rgb_v[0])/2,(rgb_h[1] + rgb_v[1])/2,(rgb_h[2] + rgb_v[2])/2]

    print('plotting vertical + horizontal interpolated image...')
    fig = plt.figure(3)
    plt.imshow(image)
    plt.show()

def inter(start_point, start_value, end_point, end_value):
    qty = end_point - start_point - 1
    arr = [None]*qty
    for i in range(qty):
        x = i + start_point + 1
        rgb_h = [0] * 3
        rgb_h[0] = int(round(int(start_value[0]) + (int(end_value[0])-int(start_value[0])) / (end_point - start_point) * (x - start_point)))
        rgb_h[1] = int(round(int(start_value[1]) + (int(end_value[1])-int(start_value[1])) / (end_point - start_point) * (x - start_point)))
        rgb_h[2] = int(round(int(start_value[2]) + (int(end_value[2])-int(start_value[2])) / (end_point - start_point) * (x - start_point)))
        arr[i] = rgb_h
    return arr
    
    
def dirty_image(img):
    """dirty image"""
    x,y = random.randint(0,img.shape[0]-1), random.randint(0,img.shape[1]-1)
    img[x,y,:] = 0

def get_points(img, rgb, direction):
    points = []
    point = None
    width = img.shape[0]
    height = img.shape[1]

    if direction == 'h':
        for y in range(width):
            for x in range(height):
                if (img[y][x] == rgb).all():
                    if point is None:
                        point = [y,x]
                elif point is not None:
                    qty = x - point[1]
                    point.append(qty)
                    points.append(point)
                    point = None
                ##if x == height TODO
    else:
        for x in range(height):
            for y in range(width):
                if (img[y][x] == rgb).all():
                    if point is None:
                        point = [y,x]
                elif point is not None:
                    qty = y - point[0]
                    point.append(qty)
                    points.append(point)
                    point = None
                ##if x == height TODO            

    return points


run()
