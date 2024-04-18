import os
file_path = "python.txt"
import time

chaitanya = '5901234123466'
debdatta = "5901234123467"
alex = '5901234123457'
test = "SCMCNT"


def read_file(file_path):
    file = open("python.txt", "r")
    content = file.read()
    # print(content)
    return content

def main():
    code = read_file(file_path)
    print(code)
    if code == str(chaitanya):
        print(chaitanya)
        print("chaitnya")

    if code == str(alex):
        print(alex)
        print("alex")

    if code == str(debdatta):
        print(debdatta)
        print("alex")
        
    if code == str(test):
        print("tested")
    time.sleep(5)
    with open('python.txt', 'w') as file:
        pass
    file.close

if __name__ == "__main__":
    while True:
        main()
    