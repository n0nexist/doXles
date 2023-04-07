# ┌┬┐┌─┐═╗ ╦┬  ┌─┐┌─┐
#  │││ │╔╩╦╝│  ├┤ └─┐
# ─┴┘└─┘╩ ╚═┴─┘└─┘└─┘
#
# doXles - github.com/n0nexist/doXles
# wifi research and osint tool
# made by n0nexist.github.io

from rich.table import Table
from rich.console import Console
import rich.box as box
from colorama import Fore, Style, init
import requests
import math

# Initialize rich console
rconsole = Console()
rconsole.clear()

# Initialize colors
init()

blue = Fore.BLUE
cyan = Fore.CYAN
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
white = Fore.WHITE
reset = Style.RESET_ALL
bright = Style.BRIGHT

# Command list
commands = [ 
    [ "help",   "shows this list" ],
    [ "cls",    "clears the screen" ],
    [ "ssid",   "searches wifi networks with a given ssid" ],
    [ "bssid",  "searches wifi networks with a given bssid" ],
    [ "loc",    "searches all wifi networks within a radius from a given location" ],
    [ "opn",    "searches open wifi networks within a radius from a given location" ],
    [ "bye",    "quits from doXles" ],
]

# Prompt string
prompt = f"{reset}doxxer{cyan}@{blue}doXles{reset}${green} "

# Logo
print(f"""{white}
┌┬┐┌─┐═╗ ╦┬  ┌─┐┌─┐
 │││ │╔╩╦╝│  ├┤ └─┐
─┴┘└─┘╩ ╚═┴─┘└─┘└─┘
{cyan}> {reset}wifi research and osint tool by {bright}{cyan}n0nexist.github.io{reset}
""")

# Variable for the api token
try:
    f = open("token.txt","r")
    api_token = f.read().strip()
    f.close()
except:
    print(f"{red}File token.txt not found - you will have to enter your WiGLE api token manually.{reset}") 
    api_token = input("Token: ")

# WiGLE api authorization headers
headers = {
    "Authorization": "Basic " + api_token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def ssid_search(ssid_name):
    """ 
    Searches for an SSID (wifi name)
    parameters: ssid_name (string)
    """

    print(f"Searching for '{ssid_name}' around the globe..")
    response = requests.get("https://api.wigle.net/api/v2/network/search", headers=headers, params={"ssid": ssid_name})
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            print(f"Found {len(data['results'])} results.")
            c = 0
            for network in data["results"]:
                c += 1
                ssid = network["ssid"]
                bssid = network["netid"]
                latitude = network["trilat"]
                longitude = network["trilong"]
                road = network["road"]
                city = network["city"]
                country = network["country"]
                encryption = network["encryption"]
                channel = network["channel"]
                print(f"{c}) {green}{ssid}{reset} ({cyan}{bssid}{reset}) -> {red}{latitude} {longitude} {reset}(\"{yellow}{road}{reset}\", {blue}{city}{reset}, {green}{country}{reset}) {encryption} CH:{channel}")
        else:
            print("No results found.")
    else:
        print("Error:", response.status_code, response.json()["message"])

def bssid_search(bssid_name):
    """ 
    Searches for a BSSID (wifi MAC address)
    parameters: bssid_name (string)
    """

    print(f"Searching for '{bssid_name}' around the globe..")
    response = requests.get("https://api.wigle.net/api/v2/network/search", headers=headers, params={"netid": bssid_name})
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            print(f"Found {len(data['results'])} results.")
            c = 0
            for network in data["results"]:
                c += 1
                ssid = network["ssid"]
                bssid = network["netid"]
                latitude = network["trilat"]
                longitude = network["trilong"]
                road = network["road"]
                city = network["city"]
                country = network["country"]
                encryption = network["encryption"]
                channel = network["channel"]
                print(f"{c}) {green}{ssid}{reset} ({cyan}{bssid}{reset}) -> {red}{latitude} {longitude} {reset}(\"{yellow}{road}{reset}\", {blue}{city}{reset}, {green}{country}{reset}) {encryption} CH:{channel}")
        else:
            print("No results found.")
    else:
        print("Error:", response.status_code, response.json()["message"])

def search_nearby_networks(latitude, longitude, radius=100):
    """ 
    Searches for nearby wifi networks within a radius (default 100 meters)
    Starting from given latitude and longitude
    parameters: latitude (string) longitude (string) radius (int + optional)
    """

    print(f"Searching for wifi networks within {radius} meters of {latitude}/{longitude} ...")
    latitude_range = (radius / 111300) 
    longitude_range = (radius / (111300 * abs(latitude)))
    params = {
        "latrange1": latitude - latitude_range,
        "latrange2": latitude + latitude_range,
        "longrange1": longitude - longitude_range,
        "longrange2": longitude + longitude_range,
    }
    response = requests.get("https://api.wigle.net/api/v2/network/search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            print(f"Found {len(data['results'])} results.")
            c = 0
            for network in data["results"]:
                c += 1
                ssid = network["ssid"]
                bssid = network["netid"]
                latitude = network["trilat"]
                longitude = network["trilong"]
                road = network["road"]
                city = network["city"]
                country = network["country"]
                encryption = network["encryption"]
                channel = network["channel"]
                print(f"{c}) {green}{ssid}{reset} ({cyan}{bssid}{reset}) -> {red}{latitude} {longitude} {reset}(\"{yellow}{road}{reset}\", {blue}{city}{reset}, {green}{country}{reset}) {encryption} CH:{channel}")
        else:
            print("No results found.")
    else:
        print("Error:", response.status_code, response.json()["message"])

def search_open_networks(latitude, longitude, radius=100):
    """ 
    Searches for open wifi networks within a radius (default 100 meters)
    Starting from given latitude and longitude
    parameters: latitude (string) longitude (string) radius (int + optional)
    """

    params = {
        "latrange1": latitude - radius/111319.9,
        "latrange2": latitude + radius/111319.9,
        "longrange1": longitude - radius/(111319.9 * math.cos(latitude)),
        "longrange2": longitude + radius/(111319.9 * math.cos(latitude)),
    }
    response = requests.get("https://api.wigle.net/api/v2/network/search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            open_networks = []
            for network in data["results"]:
                encryption = network["encryption"]
                if encryption == "":
                    open_networks.append(network)
            if len(open_networks) > 0:
                print(f"Found {len(open_networks)} results.")
                c = 0
                for network in open_networks:
                    c += 1
                    ssid = network["ssid"]
                    bssid = network["netid"]
                    latitude = network["trilat"]
                    longitude = network["trilong"]
                    road = network["road"]
                    city = network["city"]
                    country = network["country"]
                    channel = network["channel"]
                    print(f"{c}) {green}{ssid}{reset} ({cyan}{bssid}{reset}) -> {red}{latitude} {longitude} {reset}(\"{yellow}{road}{reset}\", {blue}{city}{reset}, {green}{country}{reset}) {encryption} CH:{channel}")
            else:
                print("No results found.")
        else:
            print("No results retrieved.")
    else:
        print("Error:", response.status_code, response.json()["message"])

def show_help_menu():
    """ 
    Prints available commands for doXles
    parameters: none
    """

    t = Table(box=box.HEAVY_EDGE)
    t.add_column("[cyan]Command[/cyan]")
    t.add_column("[blue]Description[/blue]")

    for x in commands:
        t.add_row(f"[yellow]{x[0]}[/yellow]",x[1])

    rconsole.print(t)

def loop():
    """ 
    The main loop that asks the user for commands
    and processes them
    parameters: none
    """

    while True:

        try:

            p = input(prompt).lower()

            if p.startswith("help"):
                show_help_menu()
            
            elif p.startswith("cls"):
                rconsole.clear()
            
            elif p.startswith("ssid"):
                try:
                    p = p.split(" ")
                    ssid_search(p[1])
                except:
                    print(f"{red}Usage: ssid (wifi name){reset}")
            
            elif p.startswith("bssid"):
                try:
                    p = p.split(" ")
                    bssid_search(p[1])
                except:
                    print(f"{red}Usage: bssid (wifi MAC address){reset}")
            
            elif p.startswith("loc"):
                try:
                    p = p.split(" ")
                    try:
                        search_nearby_networks(p[1], p[2], p[3])
                    except:
                        search_nearby_networks(p[1], p[2])
                except:
                    print(f"{red}Usage: loc (wifi name){reset}")
            
            elif p.startswith("opn"):
                try:
                    p = p.split(" ")
                    try:
                        search_open_networks(p[1], p[2], p[3])
                    except:
                        search_open_networks(p[1], p[2])
                except:
                    print(f"{red}Usage: opn (wifi name){reset}")

            elif p.startswith("bye"):
                print(f"{red}Bye{reset}")
                exit(1) # Exit code 1 - user input

        except KeyboardInterrupt:
            print(f"{red}Ctrl-C detected, exiting{reset}")
            exit(2) # Exit code 2 - ctrl-c

        except Exception as e:
            print(f"{red}Python error - {e}{reset}")
            exit(3) # Exit code 3 - python exception

loop()