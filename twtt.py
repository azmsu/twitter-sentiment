import re
import sys
import string

# input = sys.argv[1]
# student_id = sys.argv[2]
# output = sys.argv[3]

train = open("trainingandtestdata/training.1600000.processed.noemoticon.csv", "r")
test = open("trainingandtestdata/testdata.manual.2009.06.14.csv", "r")

def file_length(file):
    with file as f:
        for i, l in enumerate(f):
            pass
    return i + 1

print file_length(train)


def twtt1(s):
    # remove all html tags
    if re.search("/", s) is not None:
        print s
    

def twtt2(s):
    # replace html character codes with ASCII equivalent
    if re.search("&", s) is not None:
        print s
#
# def twtt3(string):
#     # do something
#     
# def twtt4(string):
#     # do something
#     
# def twtt5(string):
#     # do something
#     
# def twtt7(string):
#     # do something
#     
# def twtt8(string):
#     # do something
#     
# def twtt9(string):
#     # do something

for line in test:
    #lis = string.split(line, ",", 5)
    #print lis[5]
    twtt2(line)
    
print "done"
