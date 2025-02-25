import re
import pandas
import datetime


class logs():
	def __init__(self):
		super(logs, self).__init__()


	def logs_console_print(self, func: str, reason: str, desc: str) -> None:
		print(f"{datetime.datetime.now()} {func} ~ ( {reason} ): {desc}.")


	def logs_logo_print(self, logo: str, version: str) -> None:
		print(re.sub("<version>", version, logo))


	def logs_result_print(self, result: str | pandas.DataFrame) -> None:
		print(result)


	def logs_load_process_print(self) -> None:
		print(f"{datetime.datetime.now()} ( loading ).", end="\r")