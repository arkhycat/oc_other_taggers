from lxml import etree
from pymystem3 import Mystem

#removes punctuation from ends of string
def strip_word(str):
	return str.strip(',.][()«»""–-—:%&?! \n')

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
			token = strip_word(token)
			if (len(token) > 0):
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
			t_text = strip_word(t_text)
			if len(t_text) > 0:
				if t_text in tokens_index:
					idx = tokens_index.get(t_text).pop(0)
					if (len(tokens_index.get(t_text)) == 0):
						tokens_index.pop(t_text)
					analysis_indexed[idx] = t.get('analysis')
				else:
					unindexed.append(t)

		analysis_not_strict = {}
		if len(tokens_index) > 0:
			analysis_not_strict = self.match_not_strict(tokens_index, unindexed)

		analysis_indexed.update(analysis_not_strict)

#		not_analyzed = []
#		if len(tokens_index) > 0:
#			for t in tokens_index:
#				not_analyzed.append(t)

#		if len(not_analyzed) > 0:
#			f_unindexed = open('mismatch.txt', 'a+')
#			f_unindexed.write('oc ')
#			f_unindexed.write(str(not_analyzed)+'  ')


#		if len(unindexed) > 0:
#			f_unindexed = open('mismatch.txt', 'a+')
#			f_unindexed.write(' ')
#			f_unindexed.write(str(unindexed)+'\n')

		return analysis_indexed

	def match_not_strict(self, tokens_index, analyzed):
		analysis_indexed = {}
		for t_indexed, idx_list in tokens_index.items():
			for idx in idx_list:
				for i in range(0, len(analyzed)):
					t_analyzed = analyzed[i]
					if t_indexed.endswith(t_analyzed.get('text')):
						analysis_indexed[idx] = t_analyzed.get('analysis')
						#print(t_analyzed.get('text')+' '+t_indexed)
						analyzed.pop(i)
						idx_list.remove(idx)
						break
					else:
						print(t_indexed)

		idx_copy = tokens_index.copy()
		for t, i in idx_copy.items():
			if len(i) == 0:
				del tokens_index[t]


		return analysis_indexed

	def analyzed_to_csv_list(self, analyzed):
		out = []
		for idx, analysis in sorted(analyzed.items()):
			if analysis and len(analysis) > 0:
				#do we need only grammar?        
				s = str(idx) + ', ' + str(analysis[0].get('gr'))
				out.append(s)

		return out
		


