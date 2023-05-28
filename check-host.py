import sys
import argparse
import datetime

from src.scripts.methods.iplook import iplook_part
from src.scripts.methods.ping import ping_part
from src.scripts.methods.http import http_part
from src.scripts.methods.tcp import tcp_part
from src.scripts.methods.udp import udp_part
from src.scripts.methods.dns import dns_part


def parser_help_trigger(parser):
	help_text = """
 iplook: website location search
 usage:
 | python3 check-host.py --iplook -t <target>
 examples:
 | python3 check-host.py --iplook -t 1.1.1.1
 | python3 check-host.py --iplook -t example.com
 only for domain, IP address!

 ping: testing the integrity and quality of connections
 usage:
 | python3 check-host.py --ping -t <target>
 examples:
 | python3 check-host.py --ping -t 1.1.1.1
 | python3 check-host.py --ping -t http://example.com
 | python3 check-host.py --ping -t https://example.com
 | python3 check-host.py --ping -t example.com

 http: testing website availability and performance
 usage:
 | python3 check-host.py --http -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --http -t https://1.1.1.1:443
 | python3 check-host.py --http -t http://example.com
 | python3 check-host.py --http -t https://example.com
 | python3 check-host.py --http -t example.com:80

 tcp: testing TCP connection
 usage:
 | python3 check-host.py --tcp -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --tcp -t 1.1.1.1:53
 | python3 check-host.py --tcp -t http://example.com
 | python3 check-host.py --tcp -t ssmtp://smtp.gmail.com

 tcp: testing UDP connection
 usage:
 | python3 check-host.py --udp -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --udp -t 1.1.1.1:53
 | python3 check-host.py --udp -t http://example.com
 | python3 check-host.py --udp -t example.com:4444

 dns: website domain monitoring
 usage:
 | python3 check-host.py --dns -t <target>
 examples:
 | python3 check-host.py --dns -t 1.1.1.1
 | python3 check-host.py --dns -t http://example.com
 | python3 check-host.py --dns -t https://example.com
 | python3 check-host.py --dns -t example.com"""
	return help_text


def parser_error_trigger(error_info):
	print(datetime.datetime.now().strftime("%H:%M:%S"), "{ error } inf:", error_info)
	sys.exit()


def logo_part():
	logo_text = """
	      __           __       __            __ 
	 ____/ /  ___ ____/ /______/ /  ___  ___ / /_
	/ __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
	\__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v1.2 / https://github.com/diasnull                                  
	                    ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ
	"""
	return logo_text
		

def methods_part():
	while True:
		if args.iplook:
			iplook_part(args)
			break
		elif args.ping:
			ping_part(args)
			break
		elif args.http:
			http_part(args)
			break
		elif args.tcp:
			tcp_part(args)
			break
		elif args.udp:
			udp_part(args)
			break
		elif args.dns:
			dns_part(args)
			break
		print(datetime.datetime.now().strftime("%H:%M:%S"), "{ error } inf: no method selected.")
		break


def arg_parser_part():
	parser = argparse.ArgumentParser()
	parser.error = parser_error_trigger
	parser.format_help = lambda: parser_help_trigger(parser)
	parser.add_argument("-t", "--target", required=True)
	parser.add_argument("--iplook", dest="iplook", action="store_true")
	parser.add_argument("--ping", dest="ping", action="store_true")
	parser.add_argument("--http", dest="http", action="store_true")
	parser.add_argument("--tcp", dest="tcp", action="store_true")
	parser.add_argument("--udp", dest="udp", action="store_true")
	parser.add_argument("--dns", dest="dns", action="store_true")
	return parser.parse_args()


if __name__ == '__main__':
	print(logo_part())
	args = arg_parser_part()
	methods_part()