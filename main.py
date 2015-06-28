import sys
import os
import argparse
from mystem_oc import MystemOCTagger

tagger = MystemOCTagger()

def run_on_list(filename):
	print(filename)
	with open(filename) as f_list:
		idir = f_list.readline().rstrip(' /\n') + '/'
		for l in f_list.readlines()[1:]:
			#f_unindexed = open('mismatch.txt', 'a+') #!!!
			#f_unindexed.write('\n'+l) #!!!!
			#f_unindexed.close()
			tagger.run_and_convert(idir+l.rstrip(), './out/'+l.rstrip()+'.mystem.txt')

def run_on_file(filename):
	print(filename)
	tagger.run_and_convert(filename, filename+'.mystem')	

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('-l','--list')
	parser.add_argument('file', nargs='?')

	args = parser.parse_args()
	print(args)

	if (args.file and not args.list):
		run_on_file(args.file)
	else:
		if (not args.file and args.list):
			run_on_list(args.list)
		else:
			print ('Wrong arguments! Use either unnamed argument for single file or -l for file with list of files')


parse_args()
