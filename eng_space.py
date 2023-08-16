from spacy.matcher import Matcher
import spacy
import sys
import pysrt

nlp_matcher = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp_matcher.vocab)

srtfilename = sys.argv[1]

subs = pysrt.open(srtfilename)
out = []
for sub in subs:
	#print(sub)
	cur_text = sub.text
	out.append(cur_text)
	#index = index + 1

text = " ".join(out)
doc = nlp(text)
#print(text)
#exit()
#open file using open file mode
#fp1 = open(inpfile) # Open file on read mode -- input file
#text = fp1.read()#.split("\n") # Create a list containing all lines
#fp1.close() # Close file


#We create our patterns as a list of dictionaries
pattern = [
    [{"POS": "AUX"}, {"POS": "VERB"}]
]

matcher.add("verb-phrases", pattern)

doc2 = nlp_matcher(text)
matches = matcher(doc2)
for match in matches:
    print (match)
    print(doc2[match[1]].sent)
    span = doc2[match[1]:match[2]]	

    #print (span)
