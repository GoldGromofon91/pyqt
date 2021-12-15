import subprocess
from ipaddress import ip_address

from tabulate import tabulate


def host_range_ping(ip):
    dict_inst = {
        'reachable': [],
        'unreachable': [],
        'code': []
    }
    try:
        ip_add = ip_address(ip)
    except ValueError:
        raise Exception('Некорректный IP')
    else:
        try:
            range_num = int(input('Введите диапазон: '))
        except:
            raise Exception('Не число')

    for i in range(range_num):
        proc_1 = subprocess.Popen(f'ping {ip_add} -c 1 -W 2', shell=True, stdout=subprocess.DEVNULL)
        proc_1.wait()
        if not proc_1.poll():
            dict_inst['reachable'].append(ip_add)
            dict_inst['unreachable'].append('-')
        else:
            dict_inst['unreachable'].append(ip_add)

        dict_inst['code'].append(proc_1.poll())
        ip_add += 1
        continue

    print(tabulate(dict_inst, headers='keys', tablefmt="grid"))


if __name__ == "__main__":
    choice = input(f'Введите ip адресс:\n')
    host_range_ping(ip=choice)
