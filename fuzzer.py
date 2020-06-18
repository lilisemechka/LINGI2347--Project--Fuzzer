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

def lunch_process(type_of_test):

    crash = 0
    
    process = subprocess.Popen(["./converter", "newinput.img", "testoutput.img"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    error_string = ""
    try:
        for line in process.stdout: 
            if "*** The program has crashed ***" in str(line):
                crash = 1
                print(line)
           
    except TimeoutExpired:
        process.kill() 
        out, err = process.communicate()
        process.terminate()

    if(crash == 1):
        os.rename('newinput.img', type_of_test)
    
    return crash


def test_input_version(input):

    print("test_input_version")

    timeout = time.time() + 60
    bug = 0

    while not bug:
        
        file = open('newinput.img', 'wb+')

        a = random.randint(0, 1000)
        byte_to_write = a.to_bytes(2,'little')

        for i in range(0, 9):
            if(i == 1):
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()

        
        if lunch_process('bad_version.img'):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break

def test_width_heigh(input):

    print("test_width_heigh")

    timeout = time.time() + 60
    bug = 0
    count = 0
    while not bug:
        
        file = open('newinput.img', 'wb+')

        byte_to_write = count.to_bytes(4,byteorder='big')

        for i in range(0, 9):
            if(i == 3):
                file.write(b'\x02')
                file.write(byte_to_write)
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()
        count += 1

        
        if lunch_process('bad_width_heigh.img'):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break

def test_width(input):

    print("test_width")

    timeout = time.time() + 60
    bug = 0
    count = 0
    while not bug:
        
        file = open('newinput.img', 'wb+')

        byte_to_write = count.to_bytes(4,byteorder='big')

        for i in range(0, 9):
            if(i == 3):
                file.write(b'\x02')
                file.write(b'\x02\x00\x00\x00')
                file.write(byte_to_write)
            else:
                file.write(input[i])

        file.close()
        count += 1

        
        if lunch_process('bad_width.img'):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break


def test_comment_size(input):

    print("test_comment_size")

    timeout = time.time() + 60
    bug = 0

    while not bug:

        file = open('newinput.img', 'wb+')

        a = random.randint(0, 10000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)

        for i in range(0, 9):
            if(i == 6):
                file.write(b'\x0c')
                file.write(hex_string)
                file.write(b'\x00')
            else:
                file.write(input[i])

        file.close()

        if(lunch_process('bad_comment_size.img')):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break


def test_name_size(input):

    print("test_name_size")

    timeout = time.time() + 30
    bug = 0

    while not bug:

        file = open('newinput.img', 'wb+')

        a = random.randint(0, 1000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)

        for i in range(0, 9):
            if(i == 2):
                file.write(b'\x01')
                file.write(hex_string)
                file.write(b'\x00')
            else:
                file.write(input[i])

        file.close()

        if(lunch_process('bad_name_size.img')):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break


def test_image_table(input):

    print("test_image_table")

    timeout = time.time() + 10
    bug = 0

    while not bug:

        file = open('newinput.img', 'wb+')

        random_comment_1 = random_string(2)
        random_comment_2 = random_string(2)
        hex_string_1 = str.encode(random_comment_1)
        hex_string_2 = str.encode(random_comment_2)

        for i in range(0, 9):
            if(i == 7):
                file.write(hex_string_1)
            elif(i == 8):
                file.write(hex_string_2)
            else:
                file.write(input[i])

        file.close()


        if(lunch_process('bad_image_table.img')):
            bug = 1

        if time.time() > timeout:
            print("Test has reached the timeout")
            break

def testinput():

    a = [b'\xab\xcd', b'd\x00', b'\x01\x52\x61\x6d\x69\x6e\x00', b'\x02\x02\x00\x00\x00\x02\x00\x00\x00', b'\x0a\x02\x00\x00\x00', b'\x0b\x00\x00\x00\x00\xff\xff\xff\x00', b'\x0c\x48\x65\x6c\x6c\x6f\x00', b'\x00\x01', b'\x01\x00']
    return a



def fuzzer():

    input = testinput()

    test_width_heigh(input)
    test_width(input)
    test_input_version(input) # works and return the failure
    test_comment_size(input)  # works and return the failure
    test_image_table(input)   # works and return the failure
    test_name_size(input)     # works and return the failure


fuzzer()
