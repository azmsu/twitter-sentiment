'''
PART 3.4
This script is used to partition the '10000train.arff' file into two .arff files, 'train_part.arff' and 'test_part.arff'
The first file contains 18000 data points and the second 2000; they are used as the training and testing sets. The
script takes in an argument that is a multiple of 1000 starting and 1000 and ending at 10000 (i.e., 1000, 2000, 3000,
..., 10000). The script will copy the 1000 data points up to the input argument max (i.e., from max-999 to max) into
'test_part.arff' for both class 0 and 4 (totalling 2000 data points). The remaining data points are copied to
'train_part.arff'; as such, there is no overlay between the sets.

This script was run 10 times starting with input argument 1000 and ending at 10000. Each time the files
'train_part.arff' and 'test_part.arff' were overwritten. This was done because, at each iteration, I manually executed
the WEKA program in my terminal, since the file names did not change at each iteration, the same command could be used,
(i.e., java -cp WEKA/weka.jar weka.classifiers.trees.J48 -t train_part.arff -T ctest_part.arff -o)
'''

import sys

max = int(sys.argv[1])
if max == 10000:
    max = 9999

def partition(file, train, test, max):
    '''
    partitions file into train and test, max specifies the partition boundary
    :param file: .arff file containing data to be partitioned ('10000train.arff')
    :param train: destination file for training data
    :param test: destination file for testing data
    :param max: specifies partition threshold as defined in script description
    :return: none
    '''
    begin = False
    count_0, count_4 = 0, 0
    for line in file:
        if '@data' in line:
            train.write(line)
            test.write(line)
            begin = True
            continue

        if begin:
            if line[-2:] == '0\n':
                count_0 += 1

            elif line[-2:] == '4\n':
                count_4 += 1

            if count_0 > max - 1000 and count_0 <= max:
                test.write(line)

            elif count_4 > max - 1000 and count_4 <= max:
                test.write(line)

            else:
                # special case for max = 10000
                if max == 10000:
                    if count_0 == 10000:
                        test.write(line)
                    elif count_4 == 10000:
                        test.write(line)
                else:
                    train.write(line)

        else:
            train.write(line)
            test.write(line)

    return

data = open('10000train.arff', 'r')
train = open('train_part.arff', 'w')
test = open('test_part.arff', 'w')

partition(data, train, test, max)

data.close()
train.close()
test.close()
