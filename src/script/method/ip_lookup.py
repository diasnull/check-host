import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class ip_lookup():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	def _ip_lookup_show(self, ip_lookup_res: dict[str, int, float]) -> pandas.DataFrame:
		d_for_df_list: list[dict[str, int, float]] = []
		for key, value in ip_lookup_res.items():
			d_for_df_list.append({"name": key, "value": value})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ia_get_result):
	{
		"status": "success",
		"country": "Australia",
		"countryCode": "AU",
		"region": "QLD",
		"regionName": "Queensland",
		"city": "South Brisbane",
		"zip": "4101",
		"lat": -27.4766,
		"lon": 153.0166,
		"timezone": "Australia/Brisbane",
		"isp": "Cloudflare, Inc",
		"org": "APNIC and Cloudflare DNS Resolver project",
		"as": "AS13335 Cloudflare, Inc.",
		"query": "1.1.1.1"
	} -> dict[str, int, float]
	"""
	def _ip_lookup_get_res(self, target: str) -> dict[str, int, float]:
		return self.reqapi_class.reqapi_ia_get_result(target)
	

	def ip_lookup_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("ip-lookup", "info", "runned")
		ip_lookup_res: dict[str, int, float] = self._ip_lookup_get_res(args.target)
		if ip_lookup_res["status"] == "fail":
			self.logs_class.logs_console_print("ip-lookup", "info", "no 'ip-lookup' result information")
		elif ip_lookup_res["status"] == "success":
			self.logs_class.logs_result_print(self._ip_lookup_show(ip_lookup_res))
		self.logs_class.logs_console_print("ip-lookup", "info", "ended")