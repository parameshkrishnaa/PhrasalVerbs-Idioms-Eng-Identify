#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import requests
from MyParser import MyParser
from socketserver import ThreadingMixIn
import threading
import codecs
import re
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
from urllib.parse import urlparse, parse_qs
import os
import sys

langs = ['eng']
files = ['phrasal-dict.json', 'idiom-dict.json']
starting_ending_characters = (u"'", u"\"", u".", u"?", u"}", u"{", u"(", u")", u"[", u"]", u",", u"!", u"`", u"\\", u"/", u"|", u"-", u"=", u"<", u">", u"*", u"@", u"।", u":")
starting_ending_characters_array = [u"'", u"\"", u".", u"?", u"}", u"{", u"(", u")", u"[", u"]", u",", u"!", u"`", u"\\", u"/", u"|", u"-", u"=", u"<", u">", u"*", u"@", u"।", u":"]
#configuring commandline parser and check if the all command line parameters are valid
parser=MyParser()
parser.add_argument('-s', '--serverFile', help='server file (with path)', required=True)
parser.add_argument('-p', '--Port', help='serverPort', required=True, type=int)
args = parser.parse_args()

#getting command line input/bag files and check if files exist
serverFile = args.serverFile
serverPort = args.Port

if not os.path.isfile(serverFile):
    print("serverFile file", serverFile ,"does not exist.")
    sys.exit(0);

if serverPort is None:
    print("Please enter valid port.")
    sys.exit(0);

#getting server details
with open(serverFile) as server_file:
    server_details = json.load(server_file)

if 'dictpath' not in server_details:
    print("please enter valid sdictpath in server.json file.")
    sys.exit(0);

dictpath = server_details['dictpath']
#print(type(dictpath))
if not os.path.isdir(dictpath):
    print("dictpath %s does not exist."%(dictpath ))
    sys.exit(0);

port = int(serverPort)
load_phrasal_dict  = {}
load_idiom_dict  = {}

for file in files:
    #print(type(lang))
    if file != "":
        current_phrase_dict = {}
        current_idiom_dict = {}
        print("going to load %s phrasal dictionary ....." %(file))
        if os.path.isfile(dictpath + 'phrasal-dict.json'):

            bagFileObject = open(dictpath + file, "r", encoding="utf-8")
            data = json.load(bagFileObject)
            bagFileObject.close()
            for i in data:
                #print(data[i]['derivatives'])
                current_phrase_dict[i.lower()] = 1
        print("size of %s dict %s" %(file, str(len(current_phrase_dict))))

        print("going to load %s idiom dictionary ....." %(file))
        if os.path.isfile(dictpath + "idiom-dict.json"):
            bagFileObject = open(dictpath + file, "r", encoding="utf-8")
            data = json.load(bagFileObject)
            bagFileObject.close()
            for i in data:
                #print(data[i]['derivatives'])
                current_idiom_dict[i.lower()] = 1
        print("size of %s nonverified dict %s" %(file, str(len(current_idiom_dict))))
        load_phrasal_dict[file] = current_phrase_dict
        load_idiom_dict[file] = current_idiom_dict



mybagdict = {}
idiomdict = {}

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        #print(self)
        if self.path == '/verbphrase-0.1/check':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.get('Content-Length'))
                #print(self.rfile.read(length))
                postvars = parse_qs(self.rfile.read(length).decode())

            try:
                response_data = {}
                #print(postvars)
                if "inputString" in postvars and "lang" in postvars:
                    #print(postvars)

                    inputString = postvars["inputString"][0]
                    lang = postvars["lang"][0]
                    print (inputString, lang)
                    if not lang in langs:
                        response_data['status'] = "FAILURE"
                        response_data['message'] = "The given lang is invalid or is yet to be deployed.."

                    else:

                        #inputString = inputString.replace('\n', ' ').replace('\r', '')
                        inputString = re.sub(' +', ' ', inputString)

                        #print inputString
                        #sent_text = inputString.split("\n")

                        phrasaldict = {}

                        outputList = []
                        #if lang == "hin":
                        phrasaldict = load_phrasal_dict['phrasal-dict.json']
                        idiomdict = load_idiom_dict['idiom-dict.json']
                        stemmed_sentence = inputString
                        for keys in phrasaldict:
                            if(re.search(r'\b' + keys + r'\b', stemmed_sentence, re.IGNORECASE)):
                                flag = 1
                                stemmed_sentence = re.sub(r'\b' +keys + r'\b', r'['+ keys + r']', stemmed_sentence,flags=re.IGNORECASE)
                        for keys in idiomdict:
                            if(re.search(r'\b' + keys + r'\b', stemmed_sentence, re.IGNORECASE)):
                                flag = 1
                                stemmed_sentence = re.sub(r'\b' +keys + r'\b', r'[['+ keys + r']]', stemmed_sentence, flags=re.IGNORECASE)

                        outputList= stemmed_sentence.split("\n")
                        print(len(outputList))
                            #print(stemmed_sentence)
                        #print(mybagdict)
                        #print("2")
                        #print (outputList)

                        

                        response_data['status'] = "SUCCESS"
                        response_data['message'] = "The request has been processed successfully."

                        if len(outputList) > 0:
                            response_data['outputList'] = outputList


                        response_data['status'] = "SUCCESS"
                        response_data['message'] = "The request has been processed successfully."

                        if len(outputList) > 0:
                            response_data['outputList'] = outputList

                else:
                    response_data['status'] = "FAILURE"
                    response_data['message'] = "the request parameters inputString and/or lang are/is missing."

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header("Access-Control-Allow-Origin", "*");
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                return

            except:
                response_data = {}
                response_data['status'] = "FAILURE"
                response_data['message'] = "The request can not be processed due to a technical problem2"
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header("Access-Control-Allow-Origin", "*");
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)

class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip,port), RequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

if __name__=='__main__':

    server = SimpleHttpServer("", port)
    print('HTTP Server Running...........')
    server.start()
    server.waitForThread()
