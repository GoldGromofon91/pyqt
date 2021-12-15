import subprocess
from ipaddress import ip_address


def host_ping(choice):
    if choice == 1:
        ip = ['google.com', 'ya.ru', 'gb.ru']
    elif choice == 2:
        u_ip = input('Введите ip через пробел: ').split()
        try:
            ip = [ip_address(el) for el in u_ip]
        except ValueError:
            print('Not IP')

    for idx,el in enumerate(ip,1):
        proc_1 = subprocess.Popen(f'ping {el} -c 3 -W 2',shell=True,stdout=subprocess.DEVNULL)
        proc_1.wait()
        print(f'{idx}. Host {el} - reachable 'if not proc_1.poll() else f'{idx}. Host {el} - unreachable')


if __name__ == "__main__":
    try:
        choice = int(input('Select\n1-Standart hostname\n2-You ip adress:\n'))
    except ValueError:
        print('ВЫберите вариант')
    host_ping(choice=choice)