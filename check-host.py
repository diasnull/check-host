import sys
import os
import json
import requests
import time
from prettytable import PrettyTable


# COLORS #
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
RESET = "\u001b[0m"
# COLORS #


method_list = ["iplook", "ping", "http", "tcp", "dns"]
help_menu = """ iplook: website location search, IP address
 usage:
 | python3 check-host.py iplook <target>
 examples:
 | python3 check-host.py iplook 1.1.1.1
 | python3 check-host.py iplook example.com
 only for domain, IP address!

 ping: checking the integrity and quality of connections
 usage:
 | python3 check-host.py ping <target>
 examples:
 | python3 check-host.py ping 1.1.1.1
 | python3 check-host.py ping http://example.com
 | python3 check-host.py ping https://example.com
 | python3 check-host.py ping example.com 

 http: website availability and performance check
 usage:
 | python3 check-host.py http <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py http https://1.1.1.1:443
 | python3 check-host.py http http://example.com
 | python3 check-host.py http https://example.com
 | python3 check-host.py http example.com:80

 tcp: testing TCP connection of any port of an IP address, website
 usage:
 | python3 check-host.py tcp <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py tcp 1.1.1.1:53
 | python3 check-host.py tcp http://example.com
 | python3 check-host.py tcp ssmtp://smtp.gmail.com

 dns: website domain monitoring
 usage:
 | python3 check-host.py dns <target>
 examples:
 | python3 check-host.py dns 1.1.1.1
 | python3 check-host.py dns http://example.com
 | python3 check-host.py dns https://example.com
 | python3 check-host.py dns example.com"""


def LOGO_PART():
	if sys.platform == "win32": os.system("cls")
	else: os.system("clear")
	logo = f"""
	      __           __       __            __ 
	 ____/ /  ___ ____/ /______/ /  ___  ___ / /_
	/ __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
	\__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v1.0 / https://github.com/diasnull
	                    {YELLOW}ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ{RESET}
	"""
	print(logo)


def METHOD_PART():
	if user_method not in method_list:
		print(f" [{RED}ERROR{RESET}] invalid method")
		sys.exit()
	if user_method == "iplook":
		IP_LOOK_UP_PART()
	elif user_method == "ping" or user_method == "http" or user_method == "tcp" or user_method == "dns":
		CONNECT_PART()


def IP_LOOK_UP_PART():
	table_list = PrettyTable(["title", "data"])
	result_key = json.loads(requests.get(f"http://ip-api.com/json/{user_data}").text)
	if result_key["status"] == "fail":
		print(f" [{RED}ERROR{RESET}] invalid domain, IP address")
		sys.exit()
	for data_output_one, data_output_two in result_key.items():
		table_list.add_row([data_output_one, data_output_two])
	print(f" method: IP address lookup, target: {user_data}\n{table_list}")


def CONNECT_PART():
	id_key = json.loads(requests.get(f"https://check-host.net/check-{user_method}?host={user_data}&max_nodes=24", headers={"Accept": "application/json"}).text)
	RESULT_CONNECT_PART(id_key)


def RESULT_CONNECT_PART(id_key):
	result_key = requests.get(f"https://check-host.net/check-result/{id_key['request_id']}").text
	if user_method == "ping":
		PING_PART_LIST(id_key, result_key)
	elif user_method == "http":
		HTTP_PART_LIST(id_key, result_key)
	elif user_method == "tcp":
		TCP_PART_LIST(id_key, result_key)
	elif user_method == "dns":
		DNS_PART_LIST(id_key, result_key)


def PING_PART_LIST(id_key, result_key):
	table_list = PrettyTable(["location", "result", "time", "IP address"])
	loading_count = 0
	for server_list in json.loads(result_key):
		try:
			for data_output in json.loads(result_key)[server_list]:
				if data_output[0] == None: raise SystemExit
				if data_output[0][0] == "OK": data_output[0][0] = f"{GREEN}{data_output[0][0]}{RESET}"
				elif data_output[0][0] == "TIMEOUT" or data_output[0][0] == "MALFORMED": data_output[0][0] = data_output[0][0] = f"{RED}{data_output[0][0]}{RESET}"
				if data_output[1][0] == "OK": data_output[1][0] = f"{GREEN}{data_output[1][0]}{RESET}"
				elif data_output[1][0] == "TIMEOUT" or data_output[1][0] == "MALFORMED": data_output[1][0] = data_output[1][0] = f"{RED}{data_output[1][0]}{RESET}"
				if data_output[2][0] == "OK": data_output[2][0] = f"{GREEN}{data_output[2][0]}{RESET}"
				elif data_output[2][0] == "TIMEOUT" or data_output[2][0] == "MALFORMED": data_output[2][0] = data_output[2][0] = f"{RED}{data_output[2][0]}{RESET}"
				if data_output[3][0] == "OK": data_output[3][0] = f"{GREEN}{data_output[3][0]}{RESET}"
				elif data_output[3][0] == "TIMEOUT" or data_output[3][0] == "MALFORMED": data_output[3][0] = data_output[3][0] = f"{RED}{data_output[3][0]}{RESET}"
				table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", f"{data_output[0][0]} / {data_output[1][0]} / {data_output[2][0]} / {data_output[3][0]}",
				f"{round(data_output[0][1] * 1000, 1)} ms. / {round(data_output[1][1] * 1000, 1)} ms. / {round(data_output[2][1] * 1000, 1)} ms. / {round(data_output[3][1] * 1000, 1)} ms.", data_output[0][2]])
		except TypeError:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", "loading...", "...", "..."])
			loading_count =+ 1
		except SystemExit:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", "None", "None", "None"])
	if loading_count == 1:
		print(f" method: PING, target: {user_data}\n{table_list}")
		time.sleep(1)
		LOGO_PART()
		return RESULT_CONNECT_PART(id_key)
	print(f" method: PING, target: {user_data}\n{table_list}")


def HTTP_PART_LIST(id_key, result_key):
	table_list = PrettyTable(["location", "result", "time", "code", "IP address"])
	loading_count = 0
	for server_list in json.loads(result_key):
		try:
			for data_output in json.loads(result_key)[server_list]:
				if data_output[3] == None: data_output[3] = "None"
				if data_output[3][0] == "2": data_output[3] = f"{GREEN}{data_output[3]}{RESET}"
				elif data_output[3][0] == "3": data_output[3] = f"{YELLOW}{data_output[3]}{RESET}"
				elif data_output[3][0] == "4" or data_output[3][0] == "5":
					data_output[2][0] = f"{RED}{data_output[2]}{RESET}"
					data_output[3][0] = f"{RED}{data_output[3]}{RESET}"
				table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", data_output[2], f"{round(data_output[1], 2)} s.", data_output[3], data_output[4]])
		except TypeError:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", "loading...", "...", "...", "..."])
			loading_count =+ 1
	if loading_count == 1:
		print(f" method: HTTP, target: {user_data}\n{table_list}")
		time.sleep(1)
		LOGO_PART()
		return RESULT_CONNECT_PART(id_key)
	print(f" method: HTTP, target: {user_data}\n{table_list}")


def TCP_PART_LIST(id_key, result_key):
	table_list = PrettyTable(["location", "result", "time"])
	loading_count = 0
	for server_list in json.loads(result_key):
		try:
			for data_output in json.loads(result_key)[server_list]:
				table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", f"{GREEN}connected{RESET}", f"{round(data_output['time'], 2)} s."])
		except TypeError:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", "loading...", "..."])
			loading_count =+ 1
		except KeyError:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", f"{RED}{data_output['error']}{RESET}", "None"])
	if loading_count == 1:
		print(f" method: TCP, target: {user_data}\n{table_list}")
		time.sleep(1)
		LOGO_PART()
		return RESULT_CONNECT_PART(id_key)
	print(f" method: TCP, target: {user_data}\n{table_list}")


def DNS_PART_LIST(id_key, result_key):
	table_list = PrettyTable(["location", "result A record", "result AAAA record", "ttl"])
	loading_count = 0
	for server_list in json.loads(result_key):
		try:
			for data_output in json.loads(result_key)[server_list]:
				a_record, aaaa_record = ",\n".join(data_output["A"]), ",\n".join(data_output["AAAA"])
				if a_record == "": a_record = f"{RED}no A record{RESET}"
				if aaaa_record == "": aaaa_record = f"{RED}no AAAA record{RESET}"
				table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", a_record, aaaa_record, time.strftime("%M m. %S s.", time.gmtime(data_output["TTL"]))])
		except TypeError:
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", "loading...", "loading...", "..."])
			loading_count =+ 1
		except KeyError:
			if data_output["PTR"] == []: data_output["PTR"] = [f"{RED}no A record{RESET}"]
			table_list.add_row([f"{id_key['nodes'][server_list][1]}, {id_key['nodes'][server_list][2]}", data_output["PTR"][0], f"{RED}no AAAA record{RESET}", time.strftime("%M m. %S s.", time.gmtime(data_output["TTL"]))])
	if loading_count == 1:
		print(f" method: DNS, target: {user_data}\n{table_list}")
		time.sleep(1)
		LOGO_PART()
		return RESULT_CONNECT_PART(id_key)
	print(f" method: DNS, target: {user_data}\n{table_list}")


if __name__ == '__main__':
	LOGO_PART()
	try:
		user_method, user_data = sys.argv[1].lower(), sys.argv[2].lower()
		if user_method == "help": raise IndexError
	except IndexError:
		print(help_menu)
		sys.exit()
	METHOD_PART()
