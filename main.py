import sys
import os
import argparse
from mystem_oc import MystemOCTagger

tagger = MystemOCTagger()

def create_opath(filename, odir):
	path_head, path_tail = os.path.split(filename)
	if not os.path.exists(os.path.join(path_head, odir)):
		os.makedirs(os.path.join(path_head, odir))
	opath = os.path.join(path_head, odir, path_tail+'.mystem.txt')
	return opath


def run_on_list(filename, odir, strict_match):
	print(filename)
	with open(filename) as f_list:
		idir = f_list.readline()
		for l in f_list.readlines()[1:]:
#			f_unindexed = open('mismatch.txt', 'a+') #!!!
#			f_unindexed.write('\n'+l) #!!!!
#			f_unindexed.close()
			opath = create_opath(l.rstrip(), odir)
			tagger.run_and_convert(os.path.join(idir, l), opath, strict_match)

def run_on_file(filename, odir, strict_match):
	opath = create_opath(filename, odir)
	tagger.run_and_convert(filename, opath, strict_match)

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('-l','--list')
	parser.add_argument('file', nargs='?')
	parser.add_argument('-o', '--odir')
	parser.add_argument('-s', help='use only strictly matching tokens', action='store_true')

	args = parser.parse_args()

	strict_match = args.s
	if (args.odir):
		odir = args.odir
	else:
		odir = 'out'

	if (args.file and not args.list):
		run_on_file(args.file, odir, strict_match)
	else:
		if (not args.file and args.list):
			run_on_list(args.list, odir, strict_match)
		else:
			print ('Wrong arguments! Use either unnamed argument for single file or -l for file with list of files')


parse_args()
