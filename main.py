import sys
import os
import argparse
from mystem_oc import MystemOCTagger

tagger = MystemOCTagger()

def run_on_list(filename, strict_match):
	print(filename)
	with open(filename) as f_list:
		idir = f_list.readline().rstrip(' /\n') + '/'
		for l in f_list.readlines()[1:]:
#			f_unindexed = open('mismatch.txt', 'a+') #!!!
#			f_unindexed.write('\n'+l) #!!!!
#			f_unindexed.close()
			tagger.run_and_convert(idir+l.rstrip(), './out/'+l.rstrip()+'.mystem.txt', strict_match)

def run_on_file(filename, strict_match):
	print(filename)
	tagger.run_and_convert(filename, filename+'.mystem', strict_match)	

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('-l','--list')
	parser.add_argument('file', nargs='?')
	parser.add_argument('-s', help='use only strictly matching tokens', action='store_true')

	args = parser.parse_args()
	print(args)

	strict_match = args.s
	print(strict_match)

	if (args.file and not args.list):
		run_on_file(args.file, strict_match)
	else:
		if (not args.file and args.list):
			run_on_list(args.list, strict_match)
		else:
			print ('Wrong arguments! Use either unnamed argument for single file or -l for file with list of files')


parse_args()
