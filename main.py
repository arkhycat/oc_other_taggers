import sys
import os
from mystem_oc import MystemOCTagger

tagger = MystemOCTagger()

if len(sys.argv) > 2:
	if (sys.argv[1] == '-l'):
		f_name = sys.argv[2]
		with open(f_name) as f_list:
			idir = f_list.readline().rstrip(' /\n') + '/'
			for l in f_list.readlines()[1:]:
				tagger.run_and_convert(idir+l.rstrip(), './out/'+l.rstrip()+'.mystem.txt')

if len(sys.argv) == 2:
	tagger.run_and_convert(sys.argv[1], sys.argv[1]+'.mystem')