from Firebase_Client_Library import firebase_client
import sys


def main(argv):
    x= firebase_client()
    x.putvalue(argv[1],argv[2])

if __name__ == '__main__':
    main(sys.argv[:])

