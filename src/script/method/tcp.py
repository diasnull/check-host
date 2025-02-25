import time
import pandas
import argparse

from src.script.reqapi import reqapi
from src.script.logs import logs


class tcp():
	def __init__(self):
		self.reqapi_class = reqapi()
		self.logs_class = logs()


	"""
	{
		"us1.node.check-host.net": [{"time": 0.03, "address": "104.28.31.42"}],
		"ch1.node.check-host.net": [{"error": "Connection timed out"}]
	} -> dict[dict[float, str]]
	"""
	def _tcp_res_show(self, tcp_req: dict[str, dict[list[str]]], tcp_res: dict[dict[float, str]]) -> pandas.DataFrame:
		d_for_df_list: list[dict[float, str]] = []
		for key, value in tcp_res.items():
			# "us1.node.check-host.net": [None, [{"message": ""}]]
			if not value[0]:
				d_for_df_list.append({
						"country": tcp_req["nodes"][key][1],
						"city": tcp_req["nodes"][key][2],
						"result": "-",
						"time": "-",
						"ip address": "-"
					})
			if value[0]:
				d_for_df_list.append({
						"country": tcp_req["nodes"][key][1],
						"city": tcp_req["nodes"][key][2],
						"result": value[0]["error"] if value[0].get("error") else "connected",
						"time": value[0]["time"] if value[0].get("time") else "-",
						"ip address": value[0]["address"] if value[0].get("address") else "-"
					})
		return pandas.DataFrame(d_for_df_list)
	

	"""
	example of response (reqapi_ch_get_result):
	{
		"us1.node.check-host.net": [{"time": 0.03, "address": "104.28.31.42"}],
		"ch1.node.check-host.net": [{"error": "Connection timed out"}],
		"pt1.node.check-host.net": null
	} -> dict[dict[float, str]]
	"""
	def _tcp_get_res(self, request_id: str, timeout: int = 30) -> dict[dict[float, str]] | None:
		stime = time.time()
		while time.time() - stime < timeout:
			tcp_res: dict = self.reqapi_class.reqapi_ch_get_result(request_id)
			self.logs_class.logs_load_process_print()
			if all(tcp_res.get(key) is not None for key in tcp_res.keys()):
				return tcp_res
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
	def _tcp_get_req(self, target: str, max_nodes: int) -> dict[str, dict[list[str]]]:
		return self.reqapi_class.reqapi_ch_get_request(target, "tcp", max_nodes)


	def tcp_run(self, args: argparse.Namespace) -> None:
		self.logs_class.logs_console_print("tcp", "info", "runned")
		tcp_req: dict[str, dict[list[str]]] = self._tcp_get_req(args.target, args.max_nodes)
		if tcp_req.get("request_id"):
			tcp_res: dict[dict[float, str]] = self._tcp_get_res(tcp_req["request_id"])
			if not tcp_res:
				self.logs_class.logs_console_print("tcp", "info", "no 'tcp' result information, reached timeout")
			elif tcp_res: self.logs_class.logs_result_print(self._tcp_res_show(tcp_req, tcp_res))
		if not tcp_req.get("request_id"):
			self.logs_class.logs_console_print("tcp", "info", "no 'tcp' get information, reached api limit")
		self.logs_class.logs_console_print("tcp", "info", "ended")