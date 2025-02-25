import time
import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class udp():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	"""
	{
		"us1.node.check-host.net": [{"timeout": 1, "address": "104.28.31.42"}],
		"ch1.node.check-host.net": [{"error": "Connection timed out", address: "104.28.31.42"}]
	} -> dict[dict[int, str]]
	"""
	def _udp_res_show(self, udp_req: dict[str, dict[list[str]]], udp_res: dict[dict[int, str]]) -> pandas.DataFrame:
		d_for_df_list: list[dict[int, str]] = []
		for key, value in udp_res.items():
			# "us1.node.check-host.net": [None, [{"message": ""}]]
			if not value[0]:
				d_for_df_list.append({
						"country": udp_req["nodes"][key][1],
						"city": udp_req["nodes"][key][2],
						"result": "-",
						"ip address": "-"
					})
			if value[0]:
				d_for_df_list.append({
						"country": udp_req["nodes"][key][1],
						"city": udp_req["nodes"][key][2],
						"result": value[0]["error"] if value[0].get("error") else "open or filtered",
						"ip address": value[0]["address"] if value[0].get("address") else "-"
					})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ch_get_result):
	{
		"us1.node.check-host.net": [{"timeout": 1, "address": "104.28.31.42"}],
		"ch1.node.check-host.net": [{"error": "Connection timed out", address: "104.28.31.42"}],
		"pt1.node.check-host.net": null
	} -> dict[dict[int, str]]
	"""
	def _udp_get_res(self, request_id: str, timeout: int = 30) -> dict[dict[int, str]] | None:
		stime = time.time()
		while time.time() - stime < timeout:
			udp_res: dict = self.reqapi_class.reqapi_ch_get_result(request_id)
			self.logs_class.logs_load_process_print()
			if all(udp_res.get(key) is not None for key in udp_res.keys()):
				return udp_res
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
	def _udp_get_req(self, target: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return self.reqapi_class.reqapi_ch_get_request(target, "udp", max_nodes)


	def udp_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("udp", "info", "runned")
		udp_req: dict[str, dict[list[str]]] = self._udp_get_req(args.target, args.max_nodes)
		if udp_req.get("request_id"):
			udp_res: dict[dict[int, str]] = self._udp_get_res(udp_req["request_id"])
			if not udp_res:
				self.logs_class.logs_console_print("udp", "info", "no 'udp' result information, reached timeout")
			if udp_res: self.logs_class.logs_result_print(self._udp_res_show(udp_req, udp_res))
		if not udp_req.get("request_id"):
			self.logs_class.logs_console_print("udp", "info", "no 'udp' get information, reached api limit")
		self.logs_class.logs_console_print("udp", "info", "ended")