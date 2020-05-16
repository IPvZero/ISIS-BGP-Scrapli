from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir_scrapli.tasks import send_configs

def underlay(task):
    ipvzero = str(f"{task.host.hostname}")
    num = ipvzero[-2:]
    filled = num.zfill(2)
    loopback_ip = "10.10.10." + str(num)

    loopback_commands = ['interface loop0', 'ip address 10.10.10.' + str(num) + ' 255.255.255.255', 'ip router isis']
    deploy_loopback = task.run(send_configs, configs = loopback_commands)
    isis_commands = ['router isis','net 49.0001.0000.0000.00' + str(filled) + '.00']
    deploy_isis = task.run(send_configs, configs = isis_commands)
    for i in range(0,2):
        for j in range(0,4):
            interface_commands = [
                    "interface e" + str(i) + "/" + str(j),
                    "no shutdown",
                    "interface e" + str(i) + "/" + str(j) + ".1",
                    "encapsulation dot1q 10",
                    "ip unnumbered loopback0",
                    "ip router isis"
]
            deploy_interface = task.run(send_configs, configs = interface_commands)


    for i in range(1,27):
        john = str(i)
        if john.zfill(2) == str(num):
            continue
        bgp_commands = ['router bgp ' + str(task.host['asn']), 'neighbor 10.10.10.' + str(i) + ' remote-as ' + str(task.host['asn']),
                'neighbor 10.10.10.' + str(i) + ' update-source loopback0', 'neighbor 10.10.10.' + str(i) + ' password cisco',
                'neighbor 10.10.10.' + str(i) + ' timers 10 30']
        deploy_bgp = task.run(send_configs, configs = bgp_commands)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=underlay)
    print_result(result)

if __name__ == '__main__':
        main()
