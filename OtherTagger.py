import subprocess
import os

class BaseTagger(object):
	def __init__(self, exec_str):
		self.exec_str = exec_str

	def run_on_file(self, filename):
		popen = subprocess.Popen((self.exec_str, filename), stdout=subprocess.PIPE)
		popen.wait()
		output = popen.stdout.read()
		return output
