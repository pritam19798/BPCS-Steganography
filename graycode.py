
import cv2
def grayCode(n):
    return n ^ (n >> 1)

def inversegrayCode(n):
    inv = 0;
    while(n):
        inv = inv ^ n;
        n = n >> 1;
    return inv;


def image_grayCode(image):
    row,col,channel=image.shape
    for r in range(row):
        for c in range(col):
            for ch in range(channel):
                image[r][c][ch]=grayCode(image[r][c][ch])

    return image


def image_inversegrayCode(image):
    row,col,channel=image.shape
    for r in range(row):
        for c in range(col):
            for ch in range(channel):
                image[r][c][ch]=inversegrayCode(image[r][c][ch])

    return image

