#!/usr/bin/python3
import cv2
import numpy as np
import random
from error import ImageNotFoundError, BitplaneOverflowError
from message import Message
import graycode as gc


class BPCS(object):

    def __init__(self, img_path):
        self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if self.img is None:
            raise ImageNotFoundError("Sorry, no Image found")
        self.row, self.col = self.img.shape[0], self.img.shape[1]

    def hide(self, message, threshold=0.3):
        self.img = gc.image_grayCode(self.img)
        windowsize_r = 8
        windowsize_c = 8

        # print("lenmsg", len(message))

        msg_iterator = 0
        while(msg_iterator < len(message)):
            for row in range(0, self.row - windowsize_r + 1, windowsize_r):
                for col in range(0, self.col - windowsize_c + 1, windowsize_c):
                    temp_block = self.img[row:row +
                                          windowsize_r, col:col+windowsize_c]
                    channels_block = cv2.split(temp_block)

                    channels_bitplane = [self.to_bitplane(
                        block) for block in channels_block]
                    for i in range(len(channels_bitplane)):
                        itr_bitplane = 0
                        while(itr_bitplane < len(channels_bitplane[i]) and msg_iterator < len(message)):
                            if(self.calculate_complexity(channels_bitplane[i][itr_bitplane]) >= threshold):

                                channels_bitplane[i][itr_bitplane] = message[msg_iterator]
                                msg_iterator += 1
                                # if (msg_iterator < 5):
                                # print("put at", row, col, i, itr_bitplane)

                            itr_bitplane += 1

                    new_channels = [self.bitplane_to_channel(
                        bitplane) for bitplane in channels_bitplane]

                    temp_block = cv2.merge(new_channels)

                    self.img[row:row+windowsize_r,
                             col:col+windowsize_c] = temp_block

                if(msg_iterator >= len(message)):
                    break

            if(msg_iterator < len(message)):
                print(msg_iterator,len(message))

                raise BitplaneOverflowError(
                    "Carrier image don't have much bit plan with complexcity more than {} to store all message bit plane".format(threshold))
            if(msg_iterator >= len(message)):
                print(msg_iterator,len(message))
                break
        self.img = gc.image_inversegrayCode(self.img)
        return self.img


    def capacity(self,threshold=0.3):
        self.img = gc.image_grayCode(self.img)
        windowsize_r = 8
        windowsize_c = 8

            # print("lenmsg", len(message))

        count = 0

        for row in range(0, self.row - windowsize_r + 1, windowsize_r):
                for col in range(0, self.col - windowsize_c + 1, windowsize_c):
                    temp_block = self.img[row:row +
                                        windowsize_r, col:col+windowsize_c]
                    channels_block = cv2.split(temp_block)

                    channels_bitplane = [self.to_bitplane(
                            block) for block in channels_block]
                    for i in range(len(channels_bitplane)):
                            itr_bitplane = 0
                            while(itr_bitplane < len(channels_bitplane[i]) ):
                                if(self.calculate_complexity(channels_bitplane[i][itr_bitplane]) >= threshold):

                                    count=count+1

                                itr_bitplane += 1
        return np.floor(count*8*0.9)

    def show(self, threshold=0.3):
        self.img = gc.image_grayCode(self.img)
        windowsize_r = 8
        windowsize_c = 8

        msg_bitplane = []

        msg_iterator = 0
        for row in range(0, self.row - windowsize_r + 1, windowsize_r):
            for col in range(0, self.col - windowsize_c + 1, windowsize_c):
                temp_block = self.img[row:row +
                                      windowsize_r, col:col+windowsize_c]
                channels_block = cv2.split(temp_block)

                channels_bitplane = [self.to_bitplane(
                    block) for block in channels_block]

                i = 0
                for channel_bitplane in channels_bitplane:
                    j = 0
                    for bitplane in channel_bitplane:
                        if(self.calculate_complexity(bitplane) >= threshold):

                            msg_bitplane.append(bitplane)
                            msg_iterator += 1
                            if (msg_iterator < 5):
                                print("get at", row, col, i, j)
                        j += 1
                    i += 1

        return msg_bitplane

    def to_bitplane(self, img):
        result = []
        for i in reversed(range(8)):
            result.append((img / (2 ** i)).astype(int) % 2)
        return result

    def bitplane_to_channel(self, bitplane):
        result = (2 * (2 * (2 * (2 * (2 * (2 * (2 * bitplane[0] + bitplane[1])
                                           + bitplane[2]) + bitplane[3]) + bitplane[4])
                            + bitplane[5]) + bitplane[6]) + bitplane[7])
        return result

    def calculate_complexity(self, img):
        counter = 0
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                if(r != img.shape[0]-1):
                    if(img[r][c] != img[r+1][c]):
                        counter += 1
                if(c != img.shape[1]-1):
                    if(img[r][c] != img[r][c+1]):
                        counter += 1
        return counter / 112




if __name__ == '__main__':
    bpcs = BPCS('lena.bmp')
    print(bpcs.calculate_number_of_complex_bitplane(0.3))

    # message = [
    # 			np.array([[0, 0, 1, 0, 0, 0, 1, 1],
    # 					 [0, 0, 1, 0, 0, 0, 0, 0],
    # 					 [0, 1, 0, 0, 0, 0, 1, 0],
    # 					 [0, 1, 0, 1, 0, 0, 0, 0],
    # 					 [0, 1, 0, 0, 0, 0, 1, 1],
    # 					 [0, 1, 0, 1, 0, 0, 1, 1],
    # 					 [0, 0, 1, 0, 1, 1, 0, 1],
    # 					 [0, 1, 0, 1, 0, 0, 1, 1]]),
    # 			np.array([[0, 0, 1, 0, 0, 0, 1, 1],
    # 					 [0, 0, 1, 0, 1, 0, 0, 0],
    # 					 [0, 1, 0, 0, 0, 0, 1, 0],
    # 					 [0, 1, 0, 1, 0, 0, 0, 0],
    # 					 [0, 1, 0, 0, 1, 0, 1, 1],
    # 					 [0, 1, 0, 1, 0, 0, 1, 1],
    # 					 [0, 0, 1, 0, 1, 1, 0, 1],
    # 					 [0, 1, 0, 1, 0, 0, 1, 1]]),
    # 		  ]
    msg = Message("test/l.txt", threshold=0.3)
    message = msg.create_message()
    print(len(message))

    img_result = bpcs.hide(message)
    cv2.imshow('embd', img_result)
    cv2.waitKey(0)
    # img_result = bpcs.hide(message)
    # cv2.imwrite('testcase/result_img/hasil2.png', img_result)

    # bpcs2 = BPCS('testcase/result_img/hasil2.png')
    # print(bpcs2.show(randomize=True, key="secret")[0:2])
    # print(bpcs2.show()[0:2])

    # test psnr
    # print(psnr(cv2.imread('./testcase/original_img/Ape_Face_grayscale.png',-1), bpcs2.img))

    # bpcs = BPCS('watch.png')
    # m = Message('README.md')
    # m.to_binary()
    # m.to_plane_array()
    # threshold = 0.3
    # m.prepareMessageBlock(threshold)
    # img_result = bpcs.hide(m.plane_array)
    # cv2.imwrite('hasil1.png', img_result)
