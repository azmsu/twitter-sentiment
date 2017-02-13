'''
PART 2
This script builds the .arff file from the .twt file. The inputs are the name of the .twt file, the name of the .arff
file and the max number of tweets to build per class.
'''

import re
import sys

input_f = sys.argv[1]
output_f = sys.argv[2]
if len(sys.argv) == 4:
    max_tweets = int(sys.argv[3])
else:
    max_tweets = 20000

input_file = open(input_f, 'r')
output_file = open(output_f, 'w')
first_person = open('/u/cs401/Wordlists/First-person', 'r')
second_person = open('/u/cs401/Wordlists/Second-person', 'r')
third_person = open('/u/cs401/Wordlists/Third-person', 'r')
conjunct = open('/u/cs401/Wordlists/Conjunct', 'r')
slang = open('/u/cs401/Wordlists/Slang', 'r')

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

def make_lower_list(file):
    '''
    makes a list of the lines in file and converts all elements to lowercase
    :param file: a file object
    :return: list containing each line in file converted to lowercase
    '''
    lst = []
    for line in file:
        lst += [line.strip('\n').lower()]
    return lst

def feat1(tweet):
    '''
    finds number of first person-pronouns in tweet
    :param tweet: string containing tweet
    :return: number of first-person pronouns in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in FIRST_PERSON:
            count += 1
    return count

def feat2(tweet):
    '''
    finds number of second-person pronouns in tweet
    :param tweet: string containing tweet
    :return: number of second-person pronouns in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in SECOND_PERSON:
            count += 1
    return count

def feat3(tweet):
    '''
    finds number of third-person pronouns in tweet
    :param tweet: string containing tweet
    :return: number of third-person pronouns in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in THIRD_PERSON:
            count += 1
    return count

def feat4(tweet):
    '''
    finds number of conjunctions in tweet
    :param tweet: string containing tweet
    :return: number of conjunctions in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in CONJUNCT:
            count += 1
    return count

def feat5(tweet):
    '''
    finds number of past-tense verbs in tweet
    :param tweet: string containing tweet
    :return: number of past-tense verbs in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['vbd', 'vbn']:
            count += 1
    return count

def feat6(tweet):
    '''
    finds number of future-tense verbs in tweet
    :param tweet: string containing tweet
    :return: number of future-tense verbs in tweet
    '''
    count = 0
    tweet = tweet.lower()
    lst = tweet.split()
    for i in range(len(lst)):
        token = lst[i]
        index = token.rfind('/')
        if token[:index] in ['\'ll', 'will', 'gonna']:
            count += 1
        elif token[:index] == 'going':
            if i > len(lst) - 3:
                continue
            next_token = lst[i+1]
            final_token = lst[i+2]
            next_index = next_token.rfind('/')
            final_index = final_token.rfind('/')
            if next_token[:next_index] == 'to' and final_token[final_index + 1:] == 'vb':
                count += 1
    return count

def feat7(tweet):
    '''
    finds number of commas in tweet
    :param tweet: string containing tweet
    :return: number of commas in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] == ',':
            count += 1
    return count

def feat8(tweet):
    '''
    finds number of colons and semi-colons in tweet
    :param tweet: string containing tweet
    :return: number of colons and semi-colons in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in [':', ';']:
            count += 1
    return count

def feat9(tweet):
    '''
    finds number of dashes in tweet
    :param tweet: string containing tweet
    :return: number of dashes in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if re.search(r'^-+$', token[:index]):
            count += 1
    return count

def feat10(tweet):
    '''
    finds number of parentheses in tweet
    :param tweet: string containing tweet
    :return: number of parentheses in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['(', ')']:
            count += 1
    return count

def feat11(tweet):
    '''
    finds number of ellipses in tweet
    :param tweet: string containing tweet
    :return: number of ellipses in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] == '...':
            count += 1
    return count

def feat12(tweet):
    '''
    finds number of common nouns in tweet
    :param tweet: string containing tweet
    :return: number of common nouns in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['nn', 'nns']:
            count += 1
    return count

def feat13(tweet):
    '''
    finds number of proper nouns in tweet
    :param tweet: string containing tweet
    :return: number of proper nouns in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['nnp', 'nnps']:
            count += 1
    return count

def feat14(tweet):
    '''
    finds number of adverbs in tweet
    :param tweet: string containing tweet
    :return: number of adverbs in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['rb', 'rbr', 'rbs']:
            count += 1
    return count

def feat15(tweet):
    '''
    finds number of wh-words in tweet
    :param tweet: string containing tweet
    :return: number of wh-words in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[index + 1:] in ['wdt', 'wp', 'wp$', 'wrb']:
            count += 1
    return count

def feat16(tweet):
    '''
    finds number of slang terms in tweet
    :param tweet: string containing tweet
    :return: number of slang terms in tweet
    '''
    count = 0
    tweet = tweet.lower()
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index] in SLANG:
            count += 1
    return count

def feat17(tweet):
    '''
    finds number of uppercase words (length at least 2) in tweet
    :param tweet: string containing tweet
    :return: number of uppercase words (length at least 2) in tweet
    '''
    count = 0
    for token in tweet.split():
        index = token.rfind('/')
        if token[:index].isupper() and len(token[:index]) > 1:
            count += 1
    return count

def feat18(tweet):
    '''
    finds average number of tokens in a sentence in tweet
    :param tweet: string containing tweet
    :return: average number of length of sentences in tweet
    '''
    n = 0
    d = tweet.count('\n')
    #note: splitting using '\n' results in entry in list that is '' at the end, so we subtract 1 from final numerator
    for line in tweet.split('\n'):
        n += line.count(' ') + 1
    return (n-1.)/d

def feat19(tweet):
    '''
    finds average number of characters in a token in tweet
    :param tweet: string containing tweet
    :return: number of length of tokens in tweet (excluding punctuation)
    '''
    n = 0
    d = 0
    for token in tweet.split():
        index = token.rfind('/')
        #only punctuation tokens have length of 1
        if len(token[index + 1:]) != 1:
            n += len(token[:index])
            d += 1
    return (1.*n)/d

def feat20(tweet):
    '''
    finds number of sentences in tweet
    :param tweet: string containing tweet
    :return: number of sentences in tweet
    '''
    n = tweet.count('\n')
    return n

FIRST_PERSON = make_lower_list(first_person)
SECOND_PERSON = make_lower_list(second_person)
THIRD_PERSON = make_lower_list(third_person)
CONJUNCT = make_lower_list(conjunct)
SLANG = make_lower_list(slang)

line_num = 1
file_len = file_length(input_file)
input_file = open(input_f, 'r')
tweet = ''
class_dict = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
data_dict = {}
data = '@data\n'
for line in input_file:
    if line_num == 1:
        pass
    elif line[:-3] == '<A=' or line_num == file_len:
        if line_num == file_len:
            tweet += line

        c = tweet[3]

        tweet = tweet[6:]

        if max_tweets < 20000:
            if class_dict[c] < max_tweets:
                class_dict[c] += 1
            else:
                tweet = ''
                tweet += line
                line_num += 1
                continue

        data_dict['f1'] = feat1(tweet)
        data_dict['f2'] = feat2(tweet)
        data_dict['f3'] = feat3(tweet)
        data_dict['f4'] = feat4(tweet)
        data_dict['f5'] = feat5(tweet)
        data_dict['f6'] = feat6(tweet)
        data_dict['f7'] = feat7(tweet)
        data_dict['f8'] = feat8(tweet)
        data_dict['f9'] = feat9(tweet)
        data_dict['f10'] = feat10(tweet)
        data_dict['f11'] = feat11(tweet)
        data_dict['f12'] = feat12(tweet)
        data_dict['f13'] = feat13(tweet)
        data_dict['f14'] = feat14(tweet)
        data_dict['f15'] = feat15(tweet)
        data_dict['f16'] = feat16(tweet)
        data_dict['f17'] = feat17(tweet)
        data_dict['f18'] = feat18(tweet)
        data_dict['f19'] = feat19(tweet)
        data_dict['f20'] = feat20(tweet)

        for i in range(20):
            data += str(data_dict['f'+str(i+1)]) + ','
        data += c + '\n'

        tweet = ''

    tweet += line
    line_num += 1

relation = '@relation tweets\n\n'

attributes = ''
for i in range(20):
    attributes += '@attribute feat' + str(i + 1) + ' numeric\n'
attributes += '@attribute class {0, 4}\n\n'

output = relation + attributes + data

output_file.write(output)

input_file.close()
output_file.close()
