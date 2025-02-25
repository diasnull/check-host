import time
import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class dns():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	"""
	{
		"us1.node.check-host.net": [{
			"A":    ["216.58.209.174"],
			"AAAA": ["2a00:1450:400d:806::200e"],
			"TTL":  299
		}]
	} -> dict[dict[list[str]], int]
	"""
	def _dns_res_show(self, dns_req: dict[str, dict[list[str]]], dns_res: dict[dict[list[str]], int]) -> pandas.DataFrame:
		d_for_df_list: list[dict[float, str]] = []
		for key, value in dns_res.items():
			# "us1.node.check-host.net": [None, [{"message": ""}]]
			if not value[0]:
				d_for_df_list.append({
					"country": dns_req["nodes"][key][1],
					"city": dns_req["nodes"][key][2],
					"a": "-",
					"aaaa": "-",
					"ttl": "-"
				})
			if value[0]:
				d_for_df_list.append({
						"country": dns_req["nodes"][key][1],
						"city": dns_req["nodes"][key][2],
						"a": value[0]["A"] if value[0].get("A") else "-",
						"aaaa": value[0]["AAAA"] if value[0].get("AAAA") else "-",
						"ttl": value[0]["TTL"] if value[0].get("TTL") else "-"
					})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ch_get_result):
	{
		"us1.node.check-host.net": [{
			"A":    ["216.58.209.174"],
			"AAAA": ["2a00:1450:400d:806::200e"],
			"TTL":  299
		}],
		"ch1.node.check-host.net": [{"A": [], "AAAA": [], "TTL": null}],
		"pt1.node.check-host.net": null
	} -> dict[dict[list[str]], int]
	"""
	def _dns_get_res(self, request_id: str, timeout: int = 30) -> dict[dict[list[str]], int] | None:
		stime = time.time()
		while time.time() - stime < timeout:
			dns_res: dict = self.reqapi_class.reqapi_ch_get_result(request_id)
			self.logs_class.logs_load_process_print()
			if all(dns_res.get(key) is not None for key in dns_res.keys()):
				return dns_res
		return None
	

	"""
	example of response (reqapi_ch_get_request):
	{
		"ok":             1,
		"request_id":     "29",
		"permanent_link": "https://check-host.net/check-report/29",
		"nodes": {
			"us1.node.check-host.net": ["us", "USA", "Los Angeles", "5.253.30.82", "AS18978"],
		}
	} -> dict[str, dict[list[str]]]
	"""
	def _dns_get_req(self, target: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return self.reqapi_class.reqapi_ch_get_request(target, "dns", max_nodes)


	def dns_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("dns", "info", "runned")
		dns_req: dict[str, dict[list[str]]] = self._dns_get_req(args.target, args.max_nodes)
		if dns_req.get("request_id"):
			dns_res: dict[dict[list[str]], int] = self._dns_get_res(dns_req["request_id"])
			if not dns_res:
				self.logs_class.logs_console_print("dns", "info", "no 'dns' result information, reached timeout")
			elif dns_res: self.logs_class.logs_result_print(self._dns_res_show(dns_req, dns_res))
		if not dns_req.get("request_id"):
			self.logs_class.logs_console_print("dns", "info", "no 'dns' get information, reached api limit")
		self.logs_class.logs_console_print("dns", "info", "ended")