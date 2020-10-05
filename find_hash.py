import hashlib
import binascii

#for 문을 돌면서 brute-force 방식으로 처음 16비트가 0000으로 시작하는 패스워드를 찾게 만들었습니다.
#결과 값 ->b'0000' 88484 b'0000' 172608 b'0000' 269926 ... 등등 있습니다.

if __name__ == '__main__':
    password=0
    max=100000000
    for password in range(max) :
        key = hashlib.sha256(str(password).encode('utf-8')).digest()
        read_key = binascii.hexlify(bytearray(key))
        if(read_key.decode()[0:4]=="0000"):
            print(read_key[0:4],password)
        password +=1