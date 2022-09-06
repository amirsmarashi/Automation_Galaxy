#########################################
'''
Module: get_bgp.py
Author: Amir Marashi
Contact: amirsmarashi@gmail.com
Do: Import this module in order to -
Obtain information pertaining to BGP -
State, and routes.
'''
#########################################
from netmiko import ConnectHandler
from getpass import getpass
from colorama import init, Fore
import json
import re

def get_bgp():
    init(autoreset=True)
    username = input('Enter your username:')
    password = getpass()
    vrf_name = input('Enter the vrf table name:')

    with open('border_devices.json') as dev_file:
        devices = json.load(dev_file)

        for device in devices:
            device['username'] = username
            device['password'] = password

            print('*'*99)
            print(Fore.GREEN + 'Connecting to device:', device['ip'])
            net_connect = ConnectHandler(**device)
            get_bgp_idle_state = net_connect.send_command('show ip bgp vpnv4 all sum | inc Active|Idle')
            get_bgp_etablished_state = net_connect.send_command('sh ip bgp vpnv4 all summary | excl Active|Idle')

            match_all_bgp_idle_neighbors = re.findall(r'(Active|Idle)+', get_bgp_idle_state)
            match_all_bgp_neighbors = re.findall(r'[0-9]+[w]+[0-9]+[d]+', get_bgp_etablished_state)
            num_of_idle_neighbors = sum(1 for item in match_all_bgp_idle_neighbors)
            num_of_established_neighbors = sum(1 for item in match_all_bgp_neighbors)

            for idle_items in match_all_bgp_idle_neighbors:
                print(Fore.YELLOW + f"There are total of:", num_of_idle_neighbors, "Idle/Active BGP neighbors")
                #print(get_bgp_idle_state)
                break
            for established_items in match_all_bgp_neighbors:
                if str('Active') or str('Idle') not in match_all_bgp_neighbors:
                    print(Fore.YELLOW + f"There are total of:", num_of_established_neighbors, "Established BGP neighbors")
                    #print(established_items)
                    #print(get_bgp_etablished_state)
                    break

            net_connect = ConnectHandler(**device)
            get_bgp_routes = net_connect.send_command('show ip route vrf ' + str(vrf_name) + ' ' + 'bgp')
            match_all_bgp_routes = re.findall(r'[0-9|/0-9]+[.]+[0-9/0-9]+[.]+[0-9/0-9]+[.]+[0-9/0-9]+', get_bgp_routes)
            num_of_routes = sum(1 for item in match_all_bgp_routes)
            for items in match_all_bgp_routes:
                print(Fore.YELLOW + f"There are total of:", num_of_routes, "BGP routes")
                break
