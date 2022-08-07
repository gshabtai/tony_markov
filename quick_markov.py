#!/usr/bin/python3
# Created by Guy Shabtai

import random
import sys
from os.path import exists,isdir
from os import listdir
from datetime import date, datetime

# A class used for the post part of mapping pre-to-post
class Post:
    def __init__(self):
        self.text = [] # Contains all the potential posts. Quantity is used to achieve weight. Used in LOAD.
        self.encoding = {} # Contains mapping of post to weight of post as an integer. Used in MAKE.

    # Adds text to the class, in a way that adds it both to self.text and self.encoding. Used in MAKE.
    def add_text(self,s):
        self.text.append(s)
        val = self.encoding.get(s)
        if val is None:
            self.encoding.update({s : 1})
        else:
            self.encoding.update({s : val+1})

    # Gets a random text from possible posts, weighted.
    def get_text(self):
        if len(self.text) == 1:
            return self.text[0]
        return self.text[random.randint(0,len(self.text)-1)]

def count(s):
    return len(s.split())

markov = {}

if True:
    if True:
        operation = "LOAD"

    if True:
        fs = open(sys.argv[2],"r")
        line = fs.readline()
        if not line:
            raise Exception("File bad!")

        # Reads multiplicity from file.
        line = line.strip()
        mult_txt = "Multiplicity: %s. Recommended to be at least 2." % line


        # Reads pre and post lengths from file.
        for i in range(2):
            line = fs.readline()
            line = line.strip()
            if i == 0:
                PRE_LENGTH = int(line)
            else:
                POST_LENGTH = int(line)

        num_invalid_lines = 0
        while True:
            line = fs.readline()
            if not line:
                break

            line = line.strip().split()

            # Reads pre from file
            invalid = False
            new_pre = ""
            for i in range(PRE_LENGTH):
                if i >= len(line):
                    invalid = True
                if invalid:
                    num_invalid_lines += 1
                    break
                new_pre = new_pre + line[i] + " "
            if invalid:
                continue

            new_pre = new_pre[:-1]
            new_post = Post()
            post_txt = ""

            idx1=0

            # Reads all possible posts for the pre in this line, and adds to Post() object.
            for i in range(PRE_LENGTH,len(line)):
                if idx1 < POST_LENGTH:
                    post_txt = post_txt + line[i] + " "
                    idx1 += 1
                else:
                    for j in range(int(line[i])):
                        new_post.text.append(post_txt[:-1])
                    post_txt = ""
                    idx1=0  
            markov.update({new_pre : new_post})
                  
        fs.close()

        # Debugging: lists all loaded items
        #for item in markov.items():
        #    print(item[0],item[1].text)

        # Determines approximately how many words will be outputed.
        if True:
            times = (int(sys.argv[3])-PRE_LENGTH) // POST_LENGTH

            # Gets number of words from input rather than arg
            #times = 0
            #while times <= 0:
            #    in_text = input("Make how many words? ")
            #    if len(in_text) == 0:
            #        continue
            #    times = int(in_text) // (POST_LENGTH)
            
            #alternate use: get a random pre to start with
            #s = list(markov)[random.randint(0,len(markov.keys())-1)]

            # Get a pre to start with from this list
            starts = [
                "how you guys doing this is very important in reference",
                "how you guys doing this is another thing of importance in reference"
            ]

            # s = starts[random.randint(0,len(starts)-1)]
            s = list(markov)[random.randint(0,len(markov.keys())-1)]
            
            total = 0 # Used only to determine chain effectiveness. Effectivesness is how many times the chain is able to use a pre-post pair to determine the next word, instead of a random pre.
            added = 0 # Used only to determine chain effectiveness.
            
            for i in range(times):
                total += 1
                temp = s.split()
                key = ""
                for i in range(len(temp)-PRE_LENGTH,len(temp)):
                    key = key + temp[i] + " "
                key = key.strip()
                to_add = markov.get(key)

                # If we found a post for the current pre, add it.
                if to_add is not None:
                    s = s + " " + to_add.get_text()
                    added += 1
                # Otherwise, just continue with a random pre.
                else:
                    s = s + " " + list(markov)[random.randint(0,len(markov.keys())-1)]
            print(s)