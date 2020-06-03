import subprocess
import sys
import random
import struct
import string
import codecs
import binascii

def random_string(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def to_little_endian(hex_string):
    newword = ""
    count = 0
    couple = ""
    for letter in hex_string:
        couple += letter
        count += 1
        if(count % 2 == 0):
            newword += couple
            newword += " "
            couple = ""
    if(count % 2 == 1):
        couple = '0' + couple
        newword += couple

    return newword

def test_input_version():

    for i in range(20):
        
        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 200)
        print('version')
        print(a)
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

        ## Shell=False helps the process terminate
        process = subprocess.Popen(["./converter", "newinput.img", "testoutput.img"], shell=False)
    
        ## Get exit codes
        try:
            out, err = process.communicate(timeout = 15)
            errcode = process.returncode
            if("The programe has crashed" in str(errcode)):
                print(errcode)
            print(errcode)
        except TimeoutExpired:
            process.kill() 
            out, err = process.communicate()
            process.terminate()

def test_comment_size():

    for i in range(10):

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 10000)
        print("Comment size")
        print(a)
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


        ## Shell=False helps the process terminate
        process = subprocess.Popen(["./converter", "newinput.img", "newoutput.img"], shell=False)
    
        ## Get exit codes
        try:
            out, err = process.communicate(timeout = 15)
            errcode = process.returncode
            if("The programe has crashed" in str(errcode)):
                print(errcode)
            print(errcode)
        except TimeoutExpired:
            process.kill() 
            out, err = process.communicate()
            process.terminate()

def number_of_color():

    for i in range(20):

        file1 = open('testinput.img', 'rb')

        file2 = open('newinput.img', 'wb+')

        byte = file1.read(1)
        file2.write(byte)

        a = random.randint(0, 900)
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


    ## Shell=False helps the process terminate
        process = subprocess.Popen(["./converter", "newinput.img", "newoutput.img"], shell=False)
    
    ## Get exit codes
        try:
            out, err = process.communicate(timeout = 15)
            errcode = process.returncode
            if("The programe has crashed" in str(errcode)):
                print(errcode)
            print(errcode)
        except TimeoutExpired:
            process.kill() 
            out, err = process.communicate()
            process.terminate()

def test_Gilles():
    file1 = open('testinput.img', 'rb')

    file2 = open('newinput.img', 'wb+')

    byte = file1.read(1)
    file2.write(byte)

    print(byte)

    a = 105
    byte_to_write = a.to_bytes(2,'little')
    count = 0
    while byte:
        if(count == 1):
            byte = file1.read(1)
            file2.write(byte_to_write)
            count += 1 

        byte = file1.read(1)
        file2.write(byte) 
        count += 1
        print(byte)

def test_no_io():
    """test_input_version()"""
    """test_comment_size()"""
    number_of_color()
    """test_Gilles()"""

test_no_io()
