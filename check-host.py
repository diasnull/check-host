import json
import argparse

from src.script.method.ip_lookup import ip_lookup
from src.script.method.whois import whois
from src.script.method.ping import ping
from src.script.method.http import http
from src.script.method.tcp import tcp
from src.script.method.udp import udp
from src.script.method.dns import dns

from src.script.logs import logs


class check_host():
	def __init__(self):
		self.ip_lookup_class = ip_lookup()
		self.whois_class = whois()
		self.ping_class = ping()
		self.http_class = http()
		self.tcp_class = tcp()
		self.udp_class = udp()
		self.dns_class = dns()
		self.logs_class = logs()


	def _check_host_config_file_open(self) -> dict[str, dict[str]]:
		return json.loads(open("src/check-host-config.json", "r").read())
	

	def _check_host_config_access(self, func: str, attribute: str) -> str:
		return self._check_host_config_file_open()[func][attribute]
	

	def _check_host_logo(self) -> str:
		return """
	      __           __       __            __ 
	 ____/ /  ___ ____/ /______/ /  ___  ___ / /_
	/ __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
	\__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v<version> / https://github.com/diasnull                                  
	                    ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ
						"""
		

	def _check_host_method(self, args: argparse.Namespace) -> None:
		method_dict: dict[function] = {
			"ip-lookup": self.ip_lookup_class.ip_lookup_run,
			"whois": self.whois_class.whois_run,
			"ping": self.ping_class.ping_run,
			"http": self.http_class.http_run,
			"tcp": self.tcp_class.tcp_run,
			"udp": self.udp_class.udp_run,
			"dns": self.dns_class.dns_run
		}
		method_dict[args.method](args)
	

	def _check_host_argparse_format_help(self) -> None:
		return """
	usage:
		python3 check-host.py -m { method } -t { target } -mx { count of nodes }
	example:
		python3 check-host.py -m http -t example.com -mx 3
		python3 check-host.py -m dns -t https://example.com
		python3 check-host.py -m ip-lookup -t example.com

	methods:
		ip-lookup, whois, ping, http, tcp, udp, dns

	accepts:
		ip-lookup -> domain, ip
		whois -> url, domain, ip
		ping -> url, domain, ip
		http -> url, domain, ip
		tcp -> url, domain, ip
		udp -> url, domain, ip
		dns -> url, domain, ip
	"""


	def _check_host_argparse_exception(self, exception: str) -> None:
		self.logs_class.logs_console_print("check-host/argparse", "error", exception)
		self.check_host_term()


	def _check_host_argparse(self) -> argparse.Namespace:
		parser: argparse.Namespace = argparse.ArgumentParser()
		parser.error = self._check_host_argparse_exception
		parser.format_help = self._check_host_argparse_format_help
		parser.add_argument("-t", "-s", "--target", "--source", required=True, type=str)
		parser.add_argument("-m", "--method", choices=self._check_host_config_access("check-host", "method").keys(), required=True)
		parser.add_argument("-mx", "--max-nodes", type=int)
		return parser.parse_args()


	def check_host_run(self) -> None:
		self.logs_class.logs_logo_print(self._check_host_logo(),
			self._check_host_config_access("check-host", "version"))
		args: argparse.Namespace = self._check_host_argparse()
		self._check_host_method(args)


	def check_host_term(self):
		raise SystemExit
		

if __name__ == "__main__":
	check_host_class = check_host()
	check_host_class.check_host_run()
	check_host_class.check_host_term()
	