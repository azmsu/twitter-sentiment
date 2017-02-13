'''
PART 1
This script preprocesses the data given in the input file. The arguments are the name of the input .csv file, a student
ID, and the name of the output .twt file.
'''

import re
import sys
import NLPlib

input_f = sys.argv[1]
student_id = int(sys.argv[2])
output_f = sys.argv[3]

input_file = open(input_f, 'r')
output_file = open(output_f, 'w')

abbrev = open('/u/cs401/Wordlists/abbrev.english', 'r')

tagger = NLPlib.NLPlib()

def file_length(file):
    '''
    get length of file
    :param file: a file object
    :return: length of the file
    '''
    with file as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def twtt1(s):
    '''
    removes html tags from the tweet string
    :param s: string containing tweet
    :return: string containing tweet with html tags removed
    '''
    s = re.sub(r'/<[^>]+>/', '', s)
    return s

def twtt2(s):
    '''
    replaces html character codes with ASCII equivalents
    :param s: string containing tweet
    :return: string containing tweet with html character codes replaced
    '''
    html_replacements = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>'}
    match = re.search(r'&[^\s;]+;', s)
    while match:
        s = re.sub(match.group(), html_replacements.get(match.group(), match.group()), s)
        match = re.search(r'&[^\s;]+;', s)
    return s

def twtt3(s):
    '''
    removes urls
    :param s: string containing tweet
    :return: string containing tweet with urls removed
    '''
    s = re.sub(r'([wW]{3}|[hH][tT]{2}[pP])[^\s]*\w\.\w[^\s")(\[\]}\{;,(\.\s)]*', '', s)
    return s

def twtt4(s):
    '''
    removes '@' from Twitter usernames and '#' from hashtags
    :param s: string containing tweet
    :return: string containing tweet with '@'s removed from Twitter usernames and '#'s removed from hashtags
    '''
    match = re.search(r'@[\w]{3,15}', s)
    while match:
        s = re.sub(match.group(), match.group()[1:], s)
        match = re.search(r'@[\w]{3,15}', s)

    match = re.search(r'#[\w]{2,}', s)
    while match:
        s = re.sub(match.group(), match.group()[1:], s)
        match = re.search(r'#[\w]{2,}', s)
    return s

def twtt5(s):
    '''
    puts each sentence in the tweet on its own line
    :param s: string containing tweet
    :return: string containing tweet with each sentence on its own line
    '''
    abbrev = open('/u/cs401/Wordlists/abbrev.english', 'r')
    prev = 0
    match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s)
    while match:
        is_abb = False
        for abb in abbrev:
            if match.group().strip().lower() == abb.strip('\n').lower():
                is_abb = True
                break

        if is_abb:
            prev += match.end()
            match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s[prev:])
            continue

        s = s[:prev + match.end()].strip() + '\n' + s[prev + match.end():].strip()
        prev += match.end()
        match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s[prev:])

    return s

def twtt7(s):
    '''
    seperates each token by spaces
    :param s: string containing tweet
    :return: string containing tweet with tokens seperated by spaces
    '''
    #seperate each token by spaces
    match = re.search(r'[^a-zA-Z0-9_\s\t\n\r\f\v]+', s)
    prev = 0
    while match:
        end_insert, start_insert = 0, 0
        if prev + match.end() != len(s):
            if s[prev + match.end()] != ' ' and match.group() != '\'':
                s = s[:prev + match.end()] + ' ' + s[prev + match.end():]
                end_insert = 1

        if s[prev + match.start() - 1] != ' ':
            s = s[:prev + match.start()] + ' ' + s[prev + match.start():]
            start_insert = 1

        prev += match.end() + end_insert + start_insert
        match = re.search(r'[^a-zA-Z0-9_\s\t\n\r\f\v]+', s[prev:])

    return s

def twtt8(s):
    '''
    tags each token with its Part of Speech (PoS) tag
    :param s: string containing tweet
    :return: string containing tweet with PoS tags
    '''
    # print s
    lines = s.splitlines()
    sent = s.split()
    tags = tagger.tag(sent)
    s = ''

    for ln in lines:
        lst = ln.split()
        for i in range(len(lst)):
            lst[i] = lst[i] + '/' + tags[i]
            s += lst[i] + ' '
        s = s[:-1] + '\n'
        tags = tags[len(lst):]

    # print s
    return s

def twtt9(s, polarity):
    '''
    adds polarity demarcation before tweet in the form of '<A=#>' where # is the polarity of the tweet
    :param s: string containing concatenation of polarity and tweet
    :param polarity: integer value containing the polarity of the tweet
    :return: string containing tweet with demarcation added
    '''
    s = '<A=' + str(polarity) + '>\n' + s
    return s

start_point = (student_id % 80)*10000
reduce_file = False

# check if file is 1600000 lines long, if it is then take the 20000 lines as specified in the assignment document
if file_length(input_file) == 1600000:
    preserved = range(start_point, start_point+10000) + range(start_point+800000, start_point+810000)
    reduce_file = True

input_file = open(input_f, 'r')
line_num = 1
final = ''

for line in input_file:
    if reduce_file:
        if line_num == start_point+810000:
            break
        if line_num not in preserved:
            line_num += 1
            continue

    # split the line to get the tweet and polarity
    line_lst = line.split(',', 5)
    polarity = line_lst[0]
    polarity = polarity.strip('"')
    polarity = int(polarity)
    tweet = line_lst[-1]
    tweet = tweet.rstrip('\n')
    tweet = tweet.strip('"')
    tweet = tweet.strip()

    tweet = twtt1(tweet)
    tweet = twtt2(tweet)
    tweet = twtt3(tweet)
    tweet = twtt4(tweet)
    tweet = twtt5(tweet)
    tweet = twtt7(tweet)
    tweet = twtt8(tweet)
    tweet = twtt9(tweet, polarity)

    final += tweet

    line_num += 1

output_file.write(final)
input_file.close()
output_file.close()

