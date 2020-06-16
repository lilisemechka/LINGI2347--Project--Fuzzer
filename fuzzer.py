import subprocess
import sys
import random
import struct
import string
import codecs
import binascii
import os

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

def test_input_version():

    print("test_input_version")

    bug = 1

    while bug:
        
        file1 = open('testinput.img', 'rb')
        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 10000)
        byte_to_write = a.to_bytes(2,'little')
        count = 0
        while byte:
            if(count == 1):
                byte = file1.read(1)
                file2.write(byte_to_write)
                count += 1 
            else:
                byte = file1.read(1)
                file2.write(byte) 
                count += 1

        file1.close()
        file2.close()

        
        if(lunch_process('bad_version.img')):
            break

def test_comment_size():

    print("test_comment_size")

    bug = 1

    while bug:

        file1 = open('testinput.img', 'rb')
        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 10000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)
        while byte:
            if(byte == b'\x0c'):
                byte = file1.read(1)
                file2.write(hex_string)
                while byte != b'\x00':
                    byte = file1.read(1)
                file2.write(byte)
            else:
                byte = file1.read(1)
                file2.write(byte)

        file1.close()
        file2.close()

        if(lunch_process('bad_comment_size.img')):
            break

def number_of_color():

    print("number_of_color")

    for i in range(20):

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 300)
        byte_to_write = a.to_bytes(5,'little')
        while byte:
            if(byte == b'\x0a'):
                file2.write(byte)
                byte = file1.read(4)
                file2.write(byte_to_write)
            else:
                byte = file1.read(1)
                file2.write(byte)


        file1.close()
        file2.close()

        if(lunch_process('bad_number_of_color.img')):
            break

def test_name_size():

    print("test_name_size")

    bug = 1

    while bug:

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 1000)
        random_comment = random_string(a)
        hex_string = str.encode(random_comment)
        while byte:
            if(byte == b'\x01'):
                byte = file1.read(1)
                file2.write(hex_string)
                while byte != b'\x00':
                    byte = file1.read(1)
                file2.write(byte)
            else:
                byte = file1.read(1)
                file2.write(byte)

        file1.close()
        file2.close()

        if(lunch_process('bad_name_size.img')):
            break

def test_color_table():

    print("test_color_table")

    bug = 1

    while bug:

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 50)
        random_comment = random_string(a*8)
        hex_string = str.encode(random_comment)
        while byte:
            if(byte == b'\x0b'):
                byte = file1.read(1)
                file2.write(hex_string)
                while byte != b'\x00':
                    byte = file1.read(1)
                file2.write(byte)
            else:
                byte = file1.read(1)
                file2.write(byte)

        file1.close()
        file2.close()


        if(lunch_process('bad_color_table.img')):
            break

def test_width_height():

    for i in range(10):

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        random_comment_a = random_string(8)
        hex_string_a = str.encode(random_comment_a)
        a = random.randint(0, 2)
        random_comment_b = random_string(8)
        hex_string_b = str.encode(random_comment_b)
        while byte:
            if(byte == b'\x02'):
                byte = file1.read(8)
                file2.write(hex_string_a)
                byte = file1.read(8)
                file2.write(hex_string_b)
                byte = file1.read(8)
                file2.write(byte)
            else:
                byte = file1.read(1)
                file2.write(byte)

        file1.close()
        file2.close()


        if(lunch_process('bad_color_table.img')):
            break


def test_no_io():
    test_input_version() # works and return the failure
    test_comment_size()  # works and return the failure
    test_color_table()   # works and return the failure
    test_name_size()     # crashed very rarely Author: 09Ng *** The program has crashed *** mettre bcp de fois for 
    
    """test_width_height()""" # do not return the failure
    """number_of_color()""" # do not return the failure

test_no_io()
