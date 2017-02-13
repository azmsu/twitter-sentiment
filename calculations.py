'''
PART 3.4
This script takes in the values a1 and a3 from the WEKA output for the testing set, as shown below. It computes the
accuracy, precision, and recall for the data and outputs it in the format that is presented in the table in
'3.4output.txt'. It also calculates the ttest using the accuracy vectors which have been manually coded in.

Example output from running WEKA:
=== Confusion Matrix ===

   a   b   <-- classified as
  a1  a2 |   a = 0
  a3  a4 |   b = 4
'''

import sys
from scipy import stats
import numpy as np

a1 = int(sys.argv[1])
a3 = int(sys.argv[2])
a2 = 1000-a1
a4 = 1000-a3

def accuracy(a1, a2, a3, a4):
    '''
    gets accuracy given the confusion matrix
    :params a1 - a4: matrix entries shown in example at top
    :return: accuracy
    '''
    return (a1+a4*1.)/(a1+a2+a3+a4)*100

def precision(c, a1, a2, a3, a4):
    '''
    gets precision given desired class and confusion matrix
    :param c: 0 or 4 depending on which class's precision is desired
    :params a1 - a4: matrix entries shown in example at top
    :return: precision for class c
    '''
    if c == 0:
        return (a1*1.)/(a1+a3)*100
    else:
        return (a4*1.)/(a2+a4)*100

def recall(c, a1, a2, a3, a4):
    '''
    gets recall given desired class and confusion matrix
    :param c: 0 or 4 depending on which class's recall is desired
    :params a1 - a4: matrix entries shown in example at top
    :return: recall for class c
    '''
    if c == 0:
        return (a1*1.)/(a1+a2)*100
    else:
        return (a4*1.)/(a3+a4)*100

print '%.2f%s\t\t%.2f%s\t\t%.2f%s\t\t%.2f%s\t\t%.2f%s' %(accuracy(a1, a2, a3, a4), '%', precision(0, a1, a2, a3, a4), '%', recall(0, a1, a2, a3, a4), '%', precision(4, a1, a2, a3, a4), '%', recall(4, a1, a2, a3, a4), '%')

# accuracy vectors
a = np.array([63.65, 62.35, 63.6, 62.8, 62.95, 64, 60.45, 62.1, 62.5, 63.1])
b = np.array([58.75, 60.4, 60.15, 61.7, 59.85, 60.15, 57.95, 57.7, 58.95, 58.5])
c = np.array([59.1, 60.25, 60.25, 59, 58.75, 59.1, 58.75, 58.65, 58.7, 60.5])

S = stats.ttest_rel(a, b) #1.0947495325081104e-05
print S
S = stats.ttest_rel(a, c) #2.4314516400345232e-06
print S
S = stats.ttest_rel(b, c) #0.8044091306423895
print S
