# -*- coding: utf-8 -*-
#argparse allows the parsing of command line arguments
import argparse
#utility functions for the bloom filter project
import bfProjectUtils as util
#numpy numerical library - use for random values only
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
#USAGE :
#random.seed(x) : sets seed to x
#random.randint(a,b) : returns random integer in range [a,b) (inclusive beginning and exclusive ending values)
#DO NOT IMPORT NUMPY other than the function above


class HashType1(object):
    # Implement Hash Type 1

    def __init__(self, config, genHashes):
        """
        Args:
            config (dictionary) : contains configuration data for this hashing object
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients
                                    (Task 2 provides hash seeds/coefficients,
                                    Tasks 1 and 3 require you to make them yourself)
        """
        self.k = config['k']
        self.n = config['n']
        self.seeds = []
        # set random seed to be generated seed at config load
        # random.seed(config['genSeed'])
        # if generate new random hashes
        if genHashes:
            # build seed list self.seeds
            for i in range(0, self.k):
                self.seeds.append(random.randint(0, config['N']))
        # if not gen (task 2), then use hashes that are in config dictionary
        else:
            self.seeds = config['seeds']

    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using self.seeds[i]+x to
        seed random number gen to give i'th hash value
        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        res = []

        # your code goes here
        for i in range(0, self.k, 1):
            random.seed(self.seeds[i] + x)
            res.append(random.randint(0, self.n))

        #your code goes here
        return res


class HashType2(object):
    # Implement Hash Type 2

    def __init__(self, config, genHashes):
        """
        Args:
            config (dictionary):contains configuration data for this hashing object
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients
                                    (Task 2 provides hash seeds/coefficients,
                                    Tasks 1 and 3 require you to make them yourself)
        """
        self.k = config['k']
        self.n = config['n']
        self.N = config['N']
        self.Prime = util.findNextPrime(self.n)
        self.NPrime = util.findNextPrime(self.N)
        # generate new random hashes, or not if task2
        if genHashes:
            # set random seed to be generated seed at config load
            # random.seed(config['genSeed'])
            # build lists of coefficients self.a and self.b
            self.a = []
            self.b = []
            for i in range(0, self.k):
                self.a.append(random.randint(1, self.n))
                self.b.append(random.randint(0, self.n))
        # if not gen (task 2), then use hashes that are in config dictionary
        else:
            self.a = config['a']
            self.b = config['b']

    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using
        (self.a[i] * x + self.b[i] mod P) mod n
        to give i'th hash value - remember P and n must be prime, and P >= N

        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        res = []
        for i in range(0, self.k):
            res.append((((self.a[i] * x + self.b[i]) % self.NPrime) % self.Prime))
        return res


class BloomFilter(object):
    def __init__(self, config):
        """
        Args:
            config (dictionary): Configuration of this bloom filter
            config['N'] (int) universe size
            config['m'] (int) number of elements to add to filter
            config['n'] (int) number of bits in bloom filter storage array
            config['k'] (int) number of hash functions to use
            config['task'] (int) the task this bloom filter is to perform (1,2,3)
            config['type'] (int) type of hash function (1, 2, -1==unknown type)
            if type 1 hash :
                config['seeds'] (list of k ints) : seed values for k hash functions for type 1 hash function
            if type 2 hash :
                config['a'] (list of k ints) : a coefficients for k hash functions for type 2 hash function
                config['b'] (list of k ints) : b coefficients for k hash functions for type 2 hash function

            genHashes (boolean) : whether or not to generate new hash seeds/coefficients
                                    (Task 2 provides hash seeds/coefficients,
                                    Tasks 1 and 3 require you to make them yourself)
        """
        # task this boom filter is performing
        self.task = config['task']
        # task 1 requires generated seeds for hashes, task 2 uses provided seeds/coefficients
        genHashes = (self.task != 2)
        # type of hash for this bloom filter
        self.type = config['type']
        if (self.type == 1):
            self.hashFunc = HashType1(config, genHashes)
        elif (self.type == 2):
            self.hashFunc = HashType2(config, genHashes)
        else:
            print('BloomFilter for task ' + str(self.task) + ' ctor : Unknown Hash type : ' + str(self.type))
        self.hashTable = [0] * config['n']

    def add(self, x):
        """Adds x to the data structure, using self.hashFunc
        Args:
            x (int): The integer to add to the bloom filter
        """
        # your code goes here
        res = self.hashFunc.getHashList(x)
        for i in res:
            self.hashTable[i] = 1
        pass

    def contains(self, x):
        """Indicates whether data structure contains x, using self.hashFunc, with the possibility of false positives

        Args:
            x (int): The integer to test.
        Returns:
            True or False whether structure contains x or not
        """
        # your code goes here
        res = self.hashFunc.getHashList(x)
        for i in res:
            if self.hashTable[i] == 0:
                return False

        return True


"""
function will take data list, insert first m elements into bloom filter, and check all elements in datalist for membership, returning a list of results of check
    Args : 
        data (list) : list of integer data to add 
        bf (object) : bloom filter object
        m (int) : number of elements to add to bloom filter from data (first m elements)
    Returns : 
        list of results of checking 

"""


def testBF(data, bf, m):
    # add first m elements
    for i in range(0, m):
        bf.add(data[i])
    print('Finished adding ' + str(m) + ' integers to bloom filter')
    resList = []
    # test membership of all elements
    for i in range(0, len(data)):
        resList.append(str(bf.contains(data[i])))
    return resList


"""
function will support required test for Task 2.  DO NOT MODIFY.
    configData : dictionary of configuration data required to build and test bloom filter
"""


def task2(configData):
    # instantiate bloom filter object
    bf = BloomFilter(configData)

    # bfInputData holds a list of integers.  Using these values you must :
    #   insert the first configData['m'] of them into the bloom filter
    #   test all of them for membership in the bloom filter
    bfInputData = util.readIntFileDat(configData['inFileName'])

    if (len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else:
        print('bfInputData has ' + str(len(bfInputData)) + ' elements')
    # testBF will insert elements and test membership
    outputResList = testBF(bfInputData, bf, configData['m'])
    # write results to output file
    util.writeFileDat(configData['outFileName'], outputResList)
    # load appropriate validation data list for this hash function and compare to results
    util.compareResults(outputResList, configData)
    print('Task 2 complete')


def task1(configData):
    # if you wish to use this code to perform task 1, you may do so
    # NOTE : task 1 does not require you to instantiate a bloom filter

    # Start random chosen data
    bfInputData = util.readIntFileDat(configData['inFileName'])
    ht1 = HashType1(configData, True)
    ht2 = HashType2(configData, True)
    ht1.k = 1
    ht2.k = 1
    ht1list = []
    ht2list = []
    x = bfInputData[:10000]
    for i in range(0, 10000):
        ht1list.append(ht1.getHashList(bfInputData[i]))
        ht2list.append(ht2.getHashList(bfInputData[i]))

    plt.scatter(x, ht1list, marker='.', s=1)
    plt.axis((0, max(x), 0, max(ht1list)[0]))
    plt.title('Type 1 Hash Function Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    plt.scatter(x, ht2list, marker='.', s=1)
    plt.axis((0, max(x), 0, max(ht2list)[0]))
    plt.title('Type 2 Hash Function Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    ht1list = []
    ht2list = []
    x = []
    for i in range(0, 20000):
        if bfInputData[i] % 2 == 0:
            x.append(bfInputData[i])
            ht1list.append(ht1.getHashList(bfInputData[i]))
            ht2list.append(ht2.getHashList(bfInputData[i]))

    plt.scatter(x, ht1list, marker='.', s=1)
    plt.axis((0, max(x), 0, max(ht1list)[0]))
    plt.title('Type 1 Hash Function Even Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    plt.scatter(x, ht2list, marker='.', s=1)
    plt.axis((0, max(x), 0, max(ht2list)[0]))
    plt.title('Type 2 Hash Function Even Values Mapped')
    plt.xlabel('input data value')
    plt.ylabel('hash value')
    plt.show()

    print('Task 1 complete')


# Plot results for task 3
def task3(configData):
    # if you wish to use this code to perform task 3, you may do so
    # NOTE task 3 will require you to remake your bloom filter multiple times to perform the appropriate trials
    # this will necessitate either making a new bloom filter constructor or changing the config dictionary to
    # hold the appropriate values for k and n (filter size) based on c value, derived as in the notes
    # REMEMBER for type 2 hashes n must be prime.  util.findNextPrime(n) is provided for you to use to find the next largest
    # prime value of some integer.
    configData['task'] = 3
    numTrials = 10
    kVals10 = [4, 5, 6, 7, 8, 9, 10]
    kVals15 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    c10Type1 = []
    c10Type2 = []
    c15Type1 = []
    c15Type2 = []
    c10equation = []
    c15equation = []

    # calculate theoretical false positive rate when c = 10
    for i in kVals10:
        c10equation.append((1 - np.exp(-(i / 10.0))) ** i)
    # calculate theoretical false positive rate when c = 15
    for i in kVals15:
        c15equation.append((1 - np.exp(-(i / 15.0))) ** i)

    # test c = 10 for Type 1
    print('Testing c = 10 Type 1 hash...')
    c = 10
    hashType = 1
    for i in kVals10:
        c10Type1.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 10 for Type 2
    print('Testing c = 10 Type 2 hash...')
    hashType = 2
    for i in kVals10:
        c10Type2.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 15 for Type 1
    print('Testing c = 15 Type 1 hash...')
    c = 15
    hashType = 1
    for i in kVals15:
        c15Type1.append(computeFalsePositive(configData, numTrials, i, c, hashType))
    # test c = 15 for Type 2
    print('Testing c = 15 Type 2 hash...')
    hashType = 2
    for i in kVals15:
        c15Type2.append(computeFalsePositive(configData, numTrials, i, c, hashType))

    # generate plots
    fig = plt.figure()
    c10Type1Plot, = plt.plot(kVals10, c10equation, label='Theoretical False Positive Rate')
    kVals10Plot, = plt.plot(kVals10, c10Type1, label='Real False Positive Rate')
    plt.title('c = 10, Type 1 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type1Plot, kVals10Plot], ['Theoretical False Positive Rate', 'Real False Positive Rate'])
    fig.savefig('c10Type1')

    fig = plt.figure()
    c10Type2Plot, = plt.plot(kVals10, c10equation, label='Theoretical Positive Rate')
    kVals10Plot, = plt.plot(kVals10, c10Type2, label='Real False Positive Rate')
    plt.title('c = 10, Type 2 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type2Plot, kVals10Plot], ['Theoretical False Positive Rate', 'Real False Positive Rate'])
    fig.savefig('c10Type2')

    fig = plt.figure()
    c15Type1Plot, = plt.plot(kVals15, c15equation, label='Theoretical False Positive Rate')
    kVals15Plot, = plt.plot(kVals15, c15Type1, label='Real False Positive Rate')
    plt.title('c = 15, Type 1 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c15Type1Plot, kVals15Plot], ['Theoretical False Positive Rate', 'Real False Positive Rate'])
    fig.savefig('c15Type1')

    fig = plt.figure()
    c10Type2Plot, = plt.plot(kVals15, c15equation, label='Theoretical False Positive Rate')
    kVals15Plot, = plt.plot(kVals15, c15Type2, label='Real False Positive Rate')
    plt.title('c = 15, Type 2 Hash Function, k vs False Positive Rate')
    plt.xlabel('k')
    plt.ylabel('False Positive Rate')
    plt.legend([c10Type2Plot, kVals15Plot], ['Theoretical False Positive Rate', 'Real False Positive Rate'])
    fig.savefig('c15Type2')

    print('Task 3 complete')


def computeFalsePositive(configData, numTrials, k, c, hashType):
    configData['k'] = k
    configData['type'] = hashType
    configData['n'] = util.findNextPrime(c * configData['m'])
    sumFalsePositive = 0
    for i in range(0, numTrials):
        # initialize bloom filter
        bf = BloomFilter(configData)
        bfInputData = util.readIntFileDat(configData['inFileName'])
        # add data to bloom filter
        for j in range(0, configData['m']):
            bf.add(bfInputData[j])
        falsePositive = 0
        # test false positive
        for l in range(configData['m'], len(bfInputData)):
            if bf.contains(bfInputData[l]):
                falsePositive += 1
        sumFalsePositive += falsePositive / float(configData['m'])
    avgFalsePositive = sumFalsePositive / numTrials
    return avgFalsePositive


"""     
main
"""


def main():
    # DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='BloomFilter Project')
    parser.add_argument('-c', '--configfile', help='File holding configuration of Bloom Filter',
                        default='testConfigHashType2.txt', dest='configFileName')
    parser.add_argument('-i', '--infile', help='Input file of data to add to Bloom Filter', default='testInput.txt',
                        dest='inFileName')
    parser.add_argument('-o', '--outfile', help='Output file holding Bloom Filter results', default='testOutput.txt',
                        dest='outFileName')
    # you may use this argument to distinguish between tasks - default is task 2 - do not change
    # you are not required to use this code template for tasks 1 and 3.
    parser.add_argument('-t', '--task', help='Which task to perform (1,2,3)', type=int, choices=[1, 2, 3], default=2,
                        dest='taskToDo')
    parser.add_argument('-v', '--valfile', help='Validation file holding Bloom Filter expected results',
                        default='validResHashType2.txt', dest='valFileName')

    # args for autograder, do not modify
    parser.add_argument('-n', '--sName', help='Student name, used by autograder', default='GT', dest='studentName')
    parser.add_argument('-x', '--autograde', help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2],
                        default=1, dest='autograde')
    args = parser.parse_args()

    # configData is a dictionary that holds the important info needed to build your bloom filter
    # this includes the hash functon coefficients for the hash calculation for Task 2 (do not use these for Tasks 1 and 3)
    # buildBFConfigStruct prints out to the console all the elements in configData
    configData = util.buildBFConfigStruct(args)

    # perform appropriate task - 2 is default and the task2 code execution will be tested for your grade
    if configData['task'] == 2:
        task2(configData)
    elif configData['task'] == 1:
        # you are not required to use this code template for tasks 1 and 3.
        task1(configData)
    elif configData['task'] == 3:
        # you are not required to use this code template for tasks 1 and 3.
        task3(configData)
    else:
        print ('Unknown Task : ' + str(configData['task']))


if __name__ == '__main__':
    main()