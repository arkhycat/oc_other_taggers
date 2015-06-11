import os
import OtherTagger
from lxml import etree

class MystemTagger(OtherTagger.BaseTagger):
	def __init__(self):
		dir = os.path.dirname(__file__)
		full_path = os.path.join(dir, "third_party\\bin\\mystem-3.0-win7-64bit\\mystem.exe")
		super().__init__(full_path)

	def run_and_convert(self, filename):
		f = open(filename)
		root = etree.fromstring(f)
		print (root.tag)
		

ot = MystemTagger()

ot.run_and_convert("C:\\Users\\arkhy\\Documents\\progTasks\\opencorpora_taggers\\my_input\\test1.txt")
