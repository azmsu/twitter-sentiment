import re
import sys
import NLPlib

# input_file = sys.argv[1]
# student_id = sys.argv[2]
# output_file = sys.argv[3]

# input_file = open(input_file, 'r')
# output_file = open(output_file, 'w')

o_file = open('test.twt', 'w')

train = open('trainingandtestdata/training.1600000.processed.noemoticon.csv', 'r')
test = open('trainingandtestdata/testdata.manual.2009.06.14.csv', 'r')
abbrev = open('Wordlists/abbrev.english', 'r')
testing_file = open('test.csv', 'r')

tagger = NLPlib.NLPlib()

def file_length(file):
    #check length of file
    with file as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def twtt1(s):
    #remove all html tags
    s = re.sub(r'/<[^>]+>/', '', s)
    return s

def twtt2(s):
    #replace html character codes with ASCII equivalent
    html_replacements = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>'}
    match = re.search(r'&[^\s;]+;', s)
    while match:
        s = re.sub(match.group(), html_replacements.get(match.group(), match.group()), s)
        match = re.search(r'&[^\s;]+;', s)
    return s

def twtt3(s):
    #remove urls
    s = re.sub(r'([wW]{3}|[hH][tT]{2}[pP])[^\s]*\w\.\w[^\s")(\[\]}\{;,(\.\s)]*', '', s)
    return s

def twtt4(s):
    #remove '@' from usernames
    match = re.search(r'@[\w]{3,15}', s)
    while match:
        s = re.sub(match.group(), match.group()[1:], s)
        match = re.search(r'@[\w]{3,15}', s)

    #remove '#' from hashtags
    match = re.search(r'#[\w]{2,}', s)
    while match:
        s = re.sub(match.group(), match.group()[1:], s)
        match = re.search(r'#[\w]{2,}', s)
    return s

def twtt5(s):
    #set each sentence in tweet to its own line
    abbrev = open('Wordlists/abbrev.english', 'r')
    prev = 0
    match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s)
    while match:
        is_abb = False
        # print 'match:', match.group()
        for abb in abbrev:
            if match.group().strip().lower() == abb.strip('\n').lower():
                is_abb = True
                break

        if is_abb:
            # print 'abbreviation found'
            prev += match.end()
            match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s[prev:])
            continue

        s = s[:prev + match.end()].strip() + '\n' + s[prev + match.end():].strip()
        prev += match.end()
        # print 'prev:', s[prev:]
        match = re.search(r'\s\w*([\?!]+|[^\.]\.)\s', s[prev:])
    # print 'final:', s
    # print
    return s

def twtt7(s):
    #seperate each token by spaces
    match = re.search(r'[^a-zA-Z0-9_\s\t\n\r\f\v]+', s)
    prev = 0
    while match:
        # print 'match:', match.group()
        end_insert, start_insert = 0, 0
        if prev + match.end() != len(s):
            if s[prev + match.end()] != ' ' and match.group() != '\'':
                s = s[:prev + match.end()] + ' ' + s[prev + match.end():]
                end_insert = 1

        if s[prev + match.start() - 1] != ' ':
            s = s[:prev + match.start()] + ' ' + s[prev + match.start():]
            start_insert = 1

        prev += match.end() + end_insert + start_insert
        # print 'prev:', s[prev:]
        match = re.search(r'[^a-zA-Z0-9_\s\t\n\r\f\v]+', s[prev:])

    # print 'final:', s
    return s

def twtt8(s):
    #tag each token with PoS tag
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

def twtt9(s):
    #add demarcation before the tweet
    s = '<A=' + s[0] + '>\n' + s[1:]
    return s

start_point = (1001575048%80)*10000
reduce_file = False

# if file_length(train) == 1600000:
#     preserved = range(start_point, start_point+10000) + range(start_point+800000, start_point+810000)
#     train = open('trainingandtestdata/training.1600000.processed.noemoticon.csv', 'r')
#     reduce_file = True
#     # input_data = list(line for i, line in enumerate(train) if i in preserved)
#     # print len(input_data)

line_num = 1
final = ''

for line in test:
    if reduce_file:
        if line_num == start_point+810000:
            break
        if line_num not in preserved:
            line_num += 1
            continue

    #split the line to get the tweet and polarity
    line_lst = line.split(',', 5)
    polarity = line_lst[0]
    polarity = polarity.strip('"')
    tweet = line_lst[-1]
    tweet = tweet.rstrip('\n')
    tweet = tweet.strip('"')
    tweet = tweet.strip()

    # print tweet

    tweet = twtt1(tweet)
    tweet = twtt2(tweet)
    tweet = twtt3(tweet)
    tweet = twtt4(tweet)
    tweet = twtt5(tweet)
    tweet = twtt7(tweet)
    tweet = twtt8(tweet)
    tweet = twtt9(polarity + tweet)

    final += tweet

    # print line_num
    line_num += 1

o_file.write(final)
# output_file.write(output_line)
# input_file.close()
# output_file.close()

