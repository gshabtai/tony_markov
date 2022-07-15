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

# Verifies input
HELP_USAGE = "Usage\n\ndir_name =\tdirectory containing trining files, only .txt\nPRE_LENGTH =\tlength of markov state in words\nPOST_LENGTH =\tlength of markov outputs in words\nfile_name =\tname of generated file, only .swag\n\nMultiplicity is the average number of posts for each pre in the dictionary\n\nUsage:\ttony_markov.py make <dir_name> <PRE_LENGTH> <POST_LENGTH>\n\ttony_markov.py load <file_name>"
USAGE = "Usage (type \"help\" for more details)\n\nUsage:\ttony_markov.py make <dir_name> <PRE_LENGTH> <POST_LENGTH>\n\ttony_markov.py load <file_name>"
if len(sys.argv) < 2:
    raise Exception(USAGE)
elif sys.argv[1].upper() == "HELP":
    raise Exception(HELP_USAGE)
elif sys.argv[1].upper() not in ("MAKE","LOAD"):
    raise Exception("Unrecognized command \"%s\"" % sys.argv[1])
elif sys.argv[1].upper() == "MAKE" and len(sys.argv) != 5:
    raise Exception("Wrong number of arguments for load (expected 3)")
elif sys.argv[1].upper() == "MAKE" and (int(sys.argv[3]) <= 0 or int(sys.argv[4]) <= 0):
    raise Exception("Pre and post arguments must be greater than 0")
elif sys.argv[1].upper() == "LOAD" and len(sys.argv) != 3:
    raise Exception("Wrong number of arguments for load (expected 1)")
elif not exists(sys.argv[2]) and sys.argv[1].upper() == "LOAD":
    raise Exception("Can't find file \"%s\"" % sys.argv[2])
elif not isdir(sys.argv[2]) and sys.argv[1].upper() == "MAKE":
    raise Exception("Can't find directory \"%s\"" % sys.argv[2])
else:
    if sys.argv[1].upper() == "MAKE":
        PRE_LENGTH = int(sys.argv[3])
        operation = "MAKE"
        POST_LENGTH = int(sys.argv[4])
        print("Doing make...")
    elif sys.argv[1].upper() == "LOAD":
        operation = "LOAD"
        print("Doing load...")

    # The MAKE operation
    if operation == "MAKE":
        time = date.today().strftime("%d%m%Y") + datetime.now().strftime("%H%M%S") # Records time used for formatting file name
        fw = open("markov_"+time+".swag","x")

        new_path = sys.argv[2]
        
        while len(new_path) > 0 or new_path[len(new_path)-1] != '/':
            new_path = new_path[:-1]

        if len(new_path) == 0:
            new_path = sys.argv[2]

        # Iterates over files in the given directory.
        for f_name in listdir(new_path):
            if not f_name.endswith(".txt"):
                continue

            fs = open(f_name,"r")

            # Reads through the whole file
            while True:
                line = fs.readline()
                if not line:
                    break

                # Gets the current line, ignoring ' signs
                new_line = ""
                for c in line.lower():
                    if c != '\'':
                        new_line += c
                line = new_line

                # Ignores empty lines
                line_arr = line.strip().split()
                if len(line_arr) == 0:
                    continue

                
                pre = ""
                post = ""
                init_string = ""
                initializing = True
                for word in line_arr:
                    word = word.strip()
                    
                    # Makes sure init_string has enough words to fill 1 pre and 1 post.
                    if count(init_string) < PRE_LENGTH + POST_LENGTH:
                        init_string = init_string + word + " "

                    else:
                        if initializing:
                            initializing = False
                            init_string_arr = init_string.strip().split()
                            idx = 0

                            # fills pre from init_string
                            for i in range(PRE_LENGTH):
                                pre = pre + init_string_arr[idx] + " "
                                idx += 1

                            # fills post for init_string
                            for i in range(POST_LENGTH):
                                post = post + init_string_arr[idx] + " "
                                idx += 1

                            pre = pre.strip()
                            post = post.strip()

                        # Updates markov mapping of pre-to-post
                        curr_post = markov.get(pre)
                        if curr_post is None:
                            markov.update({pre : Post()})
                        markov.get(pre).add_text(post)

                        # Finds the next pre-post pair.
                        if PRE_LENGTH == 1 and POST_LENGTH == 1:
                            pre = post
                            post = word
                        elif PRE_LENGTH == 1:
                            pre = post.split()[0]
                            post = post.split(' ',1)[1] + " " + word
                        elif POST_LENGTH == 1:
                            pre = pre.split(' ',1)[1] + " " + post.split()[0]
                            post = word
                        else:
                            pre = pre.split(' ',1)[1] + " " + post.split()[0]
                            post = post.split(' ',1)[1] + " " + word

                # Update markov mapping of pre-to-post, for the final word of line.
                curr_post = markov.get(pre)
                if curr_post is None:
                    markov.update({pre : Post()})
                markov.get(pre).add_text(post)

            fs.close()

        # Calculates multiplicity
        num_items = 0
        total = 0
        for item in markov.items():
            total += len(item[1].text)
            num_items += 1
        ratio = str(total/num_items)

        # Writes file
        fw.write(ratio+ "\n" + str(PRE_LENGTH) + '\n' + str(POST_LENGTH) + "\n")
        for item in markov.items():
            fw.write(item[0])
            for i in item[1].encoding.items():
                fw.write(" " + i[0] + " " + str(i[1]))
            fw.write("\n")

        fw.close()
            
        # Multiplicity is the average number of posts for each pre in the dictionary
        mult_txt = "Multiplicity: %s. Recommended to be at least 2." % ratio

        print("Done! %s\nUse \"python tony_markov.py load %s\"" % (mult_txt,("markov_"+time+".swag")))

    # The LOAD operation
    else:
        fs = open(sys.argv[2],"r")
        line = fs.readline()
        if not line:
            raise Exception("File bad!")

        # Reads multiplicity from file.
        line = line.strip()
        mult_txt = "Multiplicity: %s. Recommended to be at least 2." % line
        print(mult_txt)

        # Reads pre and post lengths from file.
        for i in range(2):
            line = fs.readline()
            line = line.strip()
            if i == 0:
                PRE_LENGTH = int(line)
            else:
                POST_LENGTH = int(line)

        while True:
            line = fs.readline()
            if not line:
                break

            line = line.strip().split()

            # Reads pre from file
            new_pre = ""
            for i in range(PRE_LENGTH):
                new_pre = new_pre + line[i] + " "

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
        times = 0
        while times <= 0:
            times = int(input("Done! Make how many words? ")) // (POST_LENGTH)
        
        #alternate use: get a random pre to start with
        #s = list(markov)[random.randint(0,len(markov.keys())-1)]

        # Get a pre to start with from this list
        starts = [
            "how you guys doing this is very important in reference",
            "how you guys doing this is another thing of importance in reference"
        ]

        s = starts[random.randint(0,len(starts)-1)]
        
        total = 0 # Used only to determine chain effectiveness. Effectivesness is how many times the chain is able to use a pre-post pair to determine the next word, instead of a random pre.
        added = 0 # Used only to determine chain effectiveness.
        print()
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
        print("\nDone! Chain %s%s effective."%(str(100*added/total),'%'))