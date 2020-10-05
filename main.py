import struct, hashlib
import binascii
import os
import random
from Crypto.Cipher import AES


def decrypt_file(key, in_file, out_file, chunksize=24 * 1024): #파일암호를 해독한다.
    with open(in_file,'rb') as file:
        origsize = struct.unpack('<Q', file.read(struct.calcsize('Q')))[0]
        iv = file.read(16) #파일의 가장 첫 부분을 iv로 사용합니다.
        decrytor = AES.new(key, AES.MODE_CBC, iv) # CBC mode 로 암호화를 진행
        try:
            with open(out_file,'wb') as outfile:
                while True:
                    chunk = file.read(chunksize)
                    if len(chunk) ==0:
                        break
                    outfile.write(decrytor.decrypt(chunk))
                outfile.truncate(origsize)
        except:
            print('암호가 잘못되었습니다.')

def encrypt_file(key, in_filename, out_filename=None, chunksize=65536):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = 'initialvector123' #iv 를 붙여줍니다.
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'r') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize)) #2진파일 8byte struct로 변환 ->PKCS5 패딩을 사용하기위
            outfile.write(iv.encode('utf-8'))
            while True:
                chunk = infile.read(chunksize) #padding을 넣기 위해 사이즈를 조사한다.
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0: #남는 크기만큼 padding을 더해준다.
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))




if __name__ == '__main__':

    file_name = input('파일 명을 입력하세요.')
    password = input('비밀번호를 입력하세요.')
    key = hashlib.sha256(str(password).encode('utf-8')).digest() #sha256으로 해쉬화 한다.
    print(key)
    print(binascii.hexlify(bytearray(key)))
    encrypt_file(key,file_name,out_filename='output') #암호화 되고 결과물은 output.enc로 저장된다.
    print('암호화 완')

    #해독
    dest_file = input('어떤 파일을 해독하시겠습니까?')
    password2 = input('비밀번호를 입력해 주세요.')
    key2 = hashlib.sha256(str(password2).encode('utf-8')).digest()
    decrypt_file(key2,in_file='output', out_file='real.txt')
    outfile = open('real.txt')








