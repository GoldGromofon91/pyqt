import subprocess
from ipaddress import ip_address


def host_range_ping(ip):
    try:
        ip_add = ip_address(ip)
    except ValueError:
        print('Некорректный IP')
    else:
        try:
            range_num = int(input('Введите диапазон: '))
        except:
            print('Не число')

    for i in range(range_num):
        proc_1 = subprocess.Popen(f'ping {ip_add} -c 3 -W 2', shell=True, stdout=subprocess.DEVNULL)
        proc_1.wait()
        print(f'{i + 1}. Host {ip_add} - reachable ' if not proc_1.poll() else f'{i + 1}. Host {ip_add} - unreachable')
        ip_add += 1
        continue


if __name__ == "__main__":
    choice = input(f'Введите ip адресс:\n')
    host_range_ping(ip=choice)
