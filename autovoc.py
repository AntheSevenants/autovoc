# autovoc

import argparse
import random
import sys
import time
import json
import re

from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from nltk.corpus import wordnet

parser = argparse.ArgumentParser(description='autovoc - automatic vocabulary exercises')
parser.add_argument('vocabulary', type=str, help='the vocabulary file against which the exercises will be checked')
parser.add_argument('exercise_no', type=int, help='how many exercises should be generated')

args = parser.parse_args()

class Vocabulary:
	def __init__(self, filename):
		# Open the vocabulary file
		with open(args.vocabulary, "r") as available_vocabulary_file:
			raw_content = available_vocabulary_file.read()
			self.words = raw_content.split("\n")

	def get_random_word(self):
		return random.choice(self.words)

class SketchEngineApi:
	def __init__(self, api_key, corpus_name):
		self.api_key = api_key
		self.headers = { "Authorization": "Bearer {}".format(self.api_key) }
		self.base_url = 'https://api.sketchengine.eu/bonito/run.cgi'
		self.base_fields = { "corpname": corpus_name }

	def make_request(self, method, fields={}, request_method="GET"):
		attempts = 0
		fields.update(self.base_fields)

		url = "{}/{}?corpname={}&json={}".format(self.base_url,
											   method,
											   self.base_fields["corpname"],
											   quote(json.dumps(fields)))
		#print(url)

		request = Request(url,
						headers=self.headers,
						method=request_method)
		return json.loads(urlopen(request).read().decode())

def remove_html_tags(text):
	clean = re.compile('<.*?>')
	return re.sub(clean, ' ', text)

with open("sketchengine_api_key", "r") as api_key_reader:
	sketchengine_api_key = api_key_reader.read()
	sketchengine_api = SketchEngineApi(sketchengine_api_key, "preloaded/bnc2")

vocabulary = Vocabulary(args.vocabulary)

output_exercises = []

for exercise_no in range(args.exercise_no):
	word_found = False

	# I limit the script to one-word gapfills at this time
	while word_found is False:
		exercise_word = vocabulary.get_random_word()
		if len(exercise_word.split(" ")) == 1:
			word_found = True

	print("---" + exercise_word + "---")
	synset = wordnet.synsets(exercise_word)
	definition = synset[0].definition()
	print(definition)

	response = sketchengine_api.make_request("view", { "async": "0", 
													   "q": ["q[lemma=\"{}\"]".format(exercise_word), 
															  "e150"],
													   "kwicleftctx": "-2:s",
													   "kwicrightctx": "2:s",
													   "pagesize": "4" })

	#with open("output.json", "w") as output_writer:
	#	json_dump = json.dumps(response, sort_keys=True, indent=4)
	#	output_writer.write(json_dump)

	for i in range(len(response["Lines"])):
		corpus_sentence = "".join(list(map(lambda segment: segment["str"], response["Lines"][i]["Left"]))) + \
						  response["Lines"][i]["Kwic"][0]["str"] + \
						  "".join(list(map(lambda segment: segment["str"], response["Lines"][i]["Right"])))
		corpus_sentence = remove_html_tags(corpus_sentence)

		exercise_object = { "unit": "0",
		  					"word": response["Lines"][i]["Kwic"][0]["str"].strip(),
		  					"definition": definition,
		  					"synonyms": "",
		  					"corpus": corpus_sentence }

		output_exercises.append(exercise_object)

with open("output.json", "w") as output_writer:
	output_writer.write(json.dumps(output_exercises))