from lxml import etree
from pymystem3 import Mystem


class MystemOCTagger(object):
	def __init__(self):
		self.mystem_inst = Mystem()

	def run_and_convert(self, input_file, output_file):
		f_in = open(input_file, 'rb')
		f_out = open(output_file, 'w+')
		context = etree.iterparse(f_in, tag='sentence')
		for event, sentence_elem in context:
			sentence = sentence_elem.find('source')
			analyzed = self.analyze_sentence(sentence.text)
			tokens_tree = sentence_elem.find('tokens')
			tokens = self.extract_tokens(tokens_tree)
			matched = self.match_analyzed_tokens(tokens, analyzed)

			result = self.analyzed_to_csv_list(matched)
			for s in result:
				f_out.write(s+'\n')
			
			sentence_elem.clear()

	def analyze_sentence(self, sentence):
		return self.mystem_inst.analyze(sentence)

	# builds word-index mapping, indices sorted in order of appearance
	def extract_tokens(self, tokens_tree):
		tokens_dict = {}
		for t in tokens_tree.iter('token'):
			idx = t.get('id')
			token = t.get('text')
			if token in tokens_dict:
				tokens_dict.get(token).append(idx)
			else:
				tokens_dict[token] = [idx]

		return tokens_dict

	# matches analysis with original tokens indices   
	def match_analyzed_tokens(self, tokens_index, analyzed):
		analysis_indexed = {}
		#unindexed = []
		for t in analyzed:
			t_text = t.get('text') 
			if t_text in tokens_index:
				idx = tokens_index.get(t_text).pop(0)
				if (len(tokens_index.get(t_text)) == 0):
					tokens_index.pop(t_text)
				analysis_indexed[idx] = t.get('analysis')
			#else:
				#word = t_text.strip()
				#word = t_text.strip(',.][()«»–-—:% \n')
				#if len(word) > 0:
				#	unindexed.append(word)

		#not_analyzed = []
		#if len(tokens_index) > 0:
		#	for t in tokens_index:
		#		word = t.strip(',.][()«»–-—:% \n')
		#		if len(word) > 0:
		#			not_analyzed.append(word)

		#if len(not_analyzed) > 0:
			#f_unindexed = open('mismatch.txt', 'a+')
			#f_unindexed.write('oc ')
			#f_unindexed.write(str(not_analyzed)+'  ')


		#if len(unindexed) > 0:
		#	f_unindexed = open('mismatch.txt', 'a+')
		#	f_unindexed.write(' ')
		#	f_unindexed.write(str(unindexed)+'\n')

		return analysis_indexed

	def analyzed_to_csv_list(self, analyzed):
		out = []
		for idx, analysis in sorted(analyzed.items()):
			if analysis and len(analysis) > 0:
				#do we need only grammar?        
				s = str(idx) + ', ' + str(analysis[0].get('gr'))
				out.append(s)

		return out
		

