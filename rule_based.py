#from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
#from nltk.stem.snowball import SnowballStemmer
from nltk.stem import 	WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from functools import reduce
import json
import sys
#import pysrt
import re

#stemmer = SnowballStemmer("english")

phrasal_file = 'phrasal.verbs.build.json'
#open file using open file mode
fp1 = open(phrasal_file) # Open file on read mode -- input file
data = json.load(fp1)
fp1.close() # Close file

phrasal_hash = {}
#print(data)
for i in data:
    #print(data[i]['derivatives'])
    phrasal_hash[i.lower()] = 1
    
idiom_file = 'idioms.build.json'
#open file using open file mode
fp = open(idiom_file) # Open file on read mode -- input file
data = json.load(fp)
fp.close() # Close file

idiom_hash = {}
#print(data)
for i in data:
    #print(data[i]['derivatives'])
    idiom_hash[i.lower()] = 1
#exit()
#ps = PorterStemmer()

srtfilename = sys.argv[1]
# subs = pysrt.open(srtfilename)
# out = []
# for sub in subs:
# 	#print(sub)
# 	sentence = sub.text
# 	cur_text = sub.text
# 	out.append(cur_text)

# text = " ".join(out)

#open file using open file mode
fp1 = open(srtfilename) # Open file on read mode -- input file
text = fp1.read()
fp1.close() # Close file

#sentence = "Programmers program with programming languages"
#sent_text = sent_tokenize(text) # this gives us a list of sentences

# out_text = sent_text
# for keys in phrasal_hash:
# 	i = 0
# 	for sentence in sent_text:
# 		words = word_tokenize(sentence)
# 		stemmed_sentence = reduce(lambda x, y: x + " " + wordnet_lemmatizer.lemmatize(y), words, "")
# 		if(re.search(r'\b' + keys + r'\b', stemmed_sentence)):
# 			flag = 1
# 			stemmed_sentence = re.sub(r'\b' +keys + r'\b', r'['+ keys + r']', stemmed_sentence)
# 			out_text[i] = stemmed_sentence
# 		else:
# 			out_text[i] = stemmed_sentence
# 		i = i + 1


out_text = []
#for sentence in sent_text:
	#words = word_tokenize(sentence)

	#print(sentence)
	#root = stemmer.stem(word)
	#stemmed_sentence = reduce(lambda x, y: x + " " + ps.stem(y), words, "")
	#stemmed_sentence = reduce(lambda x, y: x + " " + stemmer.stem(y), words, "")

	#stemmed_sentence = reduce(lambda x, y: x + " " + wordnet_lemmatizer.lemmatize(y), words, "")

stemmed_sentence = text#.lower()
flag = 0
for keys in phrasal_hash:
	if(re.search(r'\b' + keys + r'\b', stemmed_sentence, re.IGNORECASE)):
		flag = 1
		stemmed_sentence = re.sub(r'\b' +keys + r'\b', r'<<'+ keys + r'>>', stemmed_sentence,flags=re.IGNORECASE)
for keys in idiom_hash:
	if(re.search(r'\b' + keys + r'\b', stemmed_sentence, re.IGNORECASE)):
		flag = 1
		stemmed_sentence = re.sub(r'\b' +keys + r'\b', r'##'+ keys + r'##', stemmed_sentence, flags=re.IGNORECASE)
print(stemmed_sentence)
#if(flag == 0):
	#out_text.append(stemmed_sentence)
	#print(out_text)
			#print("Sentence:|%s|Verb Phrase:|%s|" %(stemmed_sentence, keys))
	#for w in words:
		#print("Lemma for {} is {}".format(w, wordnet_lemmatizer.lemmatize(w)))  
	#print(stemmed_sentence)

#print("\n".join(out_text))