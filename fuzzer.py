import subprocess
import sys
import random
import struct
import string
import codecs
import binascii
import os
import time

def random_string(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

""" 
lunch converter with the modified image
if there is a crash, rename the input ("type_of_test") in order to save it
"""
def lunch_process(type_of_test):

    crash = 0
    
    process = subprocess.Popen(["./converter", "newinput.img", "testoutput.img"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        for line in process.stdout: 
            if "*** The program has crashed ***" in str(line):
                crash = 1
                print(line)
           
    except TimeoutExpired:
        process.kill() 
        out, err = process.communicate()
        process.terminate()

    if crash :
        os.rename('newinput.img', type_of_test)
    
    return crash


""" tests image version"""
def test_image_version(input):

    print("test_image_version")

    timeout = time.time() + 60
    bug = 0

    while not bug:

        """ build a new input with the modified image version"""       
        file = open('newinput.img', 'wb+')

        a = random.randint(0, 1000)
        byte_to_write = a.to_bytes(2,'little')

        for i in range(0, 9):
            """ change the image version input[1] """
            if i == 1 :
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()

        """ lunch the converter and, if there is a crash, stop the test """        
        if lunch_process('bad_version.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


""" tests width and height of the image """
def test_width_height(input):

    print("test_width_height")

    timeout = time.time() + 60
    bug = 0
    count = 0
    while not bug:
 
        """ build a new input with the modified height and width of the image"""       
        file = open('newinput.img', 'wb+')

        byte_to_write = count.to_bytes(4,byteorder='big')

        for i in range(0, 9):
            if i == 3:
                """ change the width and the height of the image input[3] """
                file.write(b'\x02')
                file.write(byte_to_write)
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()
        count += 1

        """ lunch the converter and, if there is a crash, stop the test """         
        if lunch_process('bad_width_height.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


""" tests height of the image """
def test_height(input):

    print("test_height")

    timeout = time.time() + 60
    bug = 0
    count = 0
    while not bug:
        
        """ build a new input with the modified height of the image """
        file = open('newinput.img', 'wb+')

        byte_to_write = count.to_bytes(4,byteorder='big')

        for i in range(0, 9):
            """ change the comment input[3] """
            if i == 3:
                file.write(b'\x02')
                """ keep the same width """
                file.write(b'\x02\x00\x00\x00') 
                """ change the height """
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()
        count += 1

        """ lunch the converter and, if there is a crash, stop the test """    
        if lunch_process('bad_height.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


""" tests the size and the content of the comment """
def test_comment_size(input):

    print("test_comment_size")

    timeout = time.time() + 60
    bug = 0

    while not bug:

        """ build a new input with the modified comment """
        file = open('newinput.img', 'wb+')

        a = random.randint(0, 10000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)


        for i in range(0, 9):
            """ change the comment input[6] """
            if i == 6:
                file.write(b'\x0c') 
                file.write(hex_string)
                file.write(b'\x00')
            else:
                file.write(input[i])

        file.close()

        """ lunch the converter and, if there is a crash, stop the test """
        if lunch_process('bad_comment_size.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


""" tests the size and the content of the name """
def test_name_size(input):

    print("test_name_size")

    timeout = time.time() + 30
    bug = 0

    while not bug:

        """ build a new input with the modified author name """
        file = open('newinput.img', 'wb+')

        a = random.randint(0, 1000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)

        for i in range(0, 9):
            """ change the author name input[2] """
            if i == 2:
                file.write(b'\x01')
                file.write(hex_string)
                file.write(b'\x00')
            else:
                file.write(input[i])

        file.close()

        """ lunch the converter and, if there is a crash, stop the test """
        if lunch_process('bad_name_size.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


""" tests the image pixels """
def test_image(input):

    print("test_image_pixels")

    timeout = time.time() + 10
    bug = 0

    while not bug:

        """ build a new input with the modified pixels """
        file = open('newinput.img', 'wb+')

        random_comment_1 = random_string(2)
        random_comment_2 = random_string(2)
        hex_string_1 = str.encode(random_comment_1)
        hex_string_2 = str.encode(random_comment_2)

        for i in range(0, 9):
            """ change the image pixels input[7] and input[8] """
            if i == 7:
                file.write(hex_string_1)
            elif i == 8:
                file.write(hex_string_2)
            else:
                file.write(input[i])

        file.close()

        """ lunch the converter and, if there is a crash, stop the test """
        if lunch_process('bad_image_table.img'):
            bug = 1

        """ if no bugs found during one minute then stop the test """
        if time.time() > timeout:
            print("Test has reached the timeout")
            break


"""
produce an input that do not produce any crashes
a[0] = AB CD (magic number)
a[1] = 64 00 (version)
a[2] = 01 52 61 6D 69 6E 00 (author name "Ramin")
a[3] = 02 02 00 00 00 02 00 00 00 (width = 2, height = 2)
a[4] = 0A 02 00 00 00 (the size of the color table)
a[5] = OB 00 00 00 00 FF FF FF 00 (the color table)
a[6] = 0C 48 65 6C 6C 6F 00 (comment "Hello")
a[7] = 00 01 (the 4 pixels of the image)
a[8] = 01 00

"""
def testinput():

    a = [b'\xab\xcd', b'd\x00', b'\x01\x52\x61\x6d\x69\x6e\x00', b'\x02\x02\x00\x00\x00\x02\x00\x00\x00', b'\x0a\x02\x00\x00\x00', b'\x0b\x00\x00\x00\x00\xff\xff\xff\x00', b'\x0c\x48\x65\x6c\x6c\x6f\x00', b'\x00\x01', b'\x01\x00']
    return a

"""main function that lunches different tests"""
def fuzzer():

    input = testinput()       # an input image that do not provoque any crashes

    test_image_version(input) # tests the number of the image version
    test_width_height(input)  # tests the width and the height of the image
    test_height(input)         # tests the heights of the image
    test_comment_size(input)  # tests the size and the content of the comment
    test_name_size(input)     # tests the size and the content of the name
    test_image(input)         # tests the image pixels 


fuzzer()
