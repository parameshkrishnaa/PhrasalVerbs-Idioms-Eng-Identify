from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import 	WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from functools import reduce
import json
import sys
import pysrt
import re

stemmer = SnowballStemmer("english")

phrasal_file = sys.argv[1]
#open file using open file mode
fp1 = open(phrasal_file) # Open file on read mode -- input file
data = json.load(fp1)
fp1.close() # Close file

phrasal_hash = {}
#print(data)
for i in data:
    #print(data[i]['derivatives'])
    phrasal_hash[i] = 1
#exit()
ps = PorterStemmer()

srtfilename = sys.argv[2]
subs = pysrt.open(srtfilename)
out = []
for sub in subs:
	#print(sub)
	sentence = sub.text
	cur_text = sub.text
	out.append(cur_text)

text = " ".join(out)
#sentence = "Programmers program with programming languages"
sent_text = sent_tokenize(text) # this gives us a list of sentences

out_text = []
count = 0
for sentence in sent_text:
	words = word_tokenize(sentence)
	#print(sentence)
	#root = stemmer.stem(word)
	#stemmed_sentence = reduce(lambda x, y: x + " " + ps.stem(y), words, "")
	#stemmed_sentence = reduce(lambda x, y: x + " " + stemmer.stem(y), words, "")
	stemmed_sentence = reduce(lambda x, y: x + " " + wordnet_lemmatizer.lemmatize(y), words, "")
	flag = 0
	for keys in phrasal_hash:
		if(re.search(r''+keys, stemmed_sentence)):
			flag = 1
			out_text.append(re.sub(r''+keys, r'['+ keys + r']', stemmed_sentence))
	if(flag == 0):
		out_text.append(stemmed_sentence)

	#print(out_text)
			#print("Sentence:|%s|Verb Phrase:|%s|" %(stemmed_sentence, keys))
	#for w in words:
		#print("Lemma for {} is {}".format(w, wordnet_lemmatizer.lemmatize(w)))  
	#print(stemmed_sentence)

print("\n".join(out_text))