import re
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class whois():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	def _whois_res_show(self, whois_res: str) -> str:
		return whois_res


	"""
	example of response (reqapi_ch_post_request):
	% IANA WHOIS server
	% for more information on IANA, visit http://www.iana.org
	% This query returned 1 object
	-> str
	"""
	def _whois_get_res(self, target: str) -> str:
		return self.reqapi_class.reqapi_ch_post_request(target)
	

	def whois_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("whois", "info", "runned")
		whois_res: str = self._whois_get_res(args.target)
		if whois_res.strip() == "" or re.search("invalid query", whois_res, re.IGNORECASE):
			self.logs_class.logs_console_print("whois", "info", "no 'whois' result information")
		elif not whois_res.strip() == "" or not re.search("invalid query", whois_res, re.IGNORECASE):
			self.logs_class.logs_result_print(self._whois_res_show(whois_res))
		self.logs_class.logs_console_print("whois", "info", "ended")