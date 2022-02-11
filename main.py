from time import sleep

from detector import detect_iss


def main():
    while True:
        detect_iss()
        sleep(60)


main()
