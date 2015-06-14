from lxml import etree
from pymystem3 import Mystem


class MystemOCTagger(object):
	def __init__(self):
		self.mystem_inst = Mystem()

	def run_and_convert(self, input_file, output_file):
		f_in = open(input_file)
		f_out = open(output_file, 'w+')
		tree = etree.parse(f_in)
		for sentence_tree in tree.getroot().iter('sentence'):
			sentence = sentence_tree.find('source')
			analyzed = self.analyze_sentence(sentence.text)
			tokens_tree = sentence_tree.find('tokens')
			tokens = self.extract_tokens(tokens_tree)
			matched = self.match_analyzed_tokens(tokens, analyzed)

			result = self.analyzed_to_csv_list(matched)
			for s in result:
				f_out.write(s+'\n')
			#f_out.write(str(analyzed))

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
		unindexed = []
		for t in analyzed:
			t_text = t.get('text') 
			if t_text in tokens_index:
				idx = tokens_index.get(t_text).pop(0)
				if (len(tokens_index.get(t_text)) == 0):
					tokens_index.pop(t_text)
				analysis_indexed[idx] = t.get('analysis')
			else:
				unindexed.append(t_text)

		print(unindexed)

		return analysis_indexed

	def analyzed_to_csv_list(self, analyzed):
		out = []
		for idx, analysis in sorted(analyzed.items()):
			if analysis and len(analysis) > 0:
				#do we need only grammar?        
				s = str(idx) + ', ' + str(analysis[0].get('gr'))
				out.append(s)

		return out
		

