#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter    #For creating the dictionary with term frequency
import string  #For removing punctuation
import math  #For log() and sqrt()
import sys  #For command line args


# In[2]:


def readFile(filename1, filename2):
    
    ''' Reads the files specified by filenames : filename1 and filename2. 
        Removes all punctuations from test data (except ') and converts everything to lowercase
        
        INPUT:    Two strings as filenames
        OUTPUT:   fileDoc1 - list containing all sentences from filename1.txt
                  fileDoc2 - list containing all sentences from filename2.txt'''
    
    translator = str.maketrans('', '', '''!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~0123456789''')    
    
    #Read the filename1.txt
    fh=open(filename1 , encoding="utf8")
    trainedOut = []
    for line in fh:
        s = line.lstrip().rstrip()   #String the \n
        if s != '':
            trainedOut.append(s)
    fh.close()

    #Remove punctuations and covert to lower case
    finalDoc1 = []
    for line in trainedOut:
        out = line.translate(translator)
        finalDoc1.append(out.lower())

    #Read the filename2.txt
    fh=open(filename2 , encoding="utf8")
    actualOut = []
    for line in fh:
        s = line.lstrip().rstrip()   #Strip the \n
        if s != '':
            actualOut.append(s)
    fh.close()

    #Remove punctuations and covert to lower case
    finalDoc2 = []
    for line in actualOut:
        out = line.translate(str.maketrans('','',string.punctuation))
        finalDoc2.append(out.lower())
    
    return finalDoc1,finalDoc2


# In[3]:


def parameterGeneration(finalDoc1, finalDoc2):
    
    ''' Reads the lists finalDoc1 and finalDoc2 and splits each sentence into words
        vector1: list which contains all the words from the sentences present in finalDoc1
        vector2: list which contains all the words from the sentences present in finalDoc2
        dict1: dictionary which contains the count of occurence (the value) of each word (the key) in vector1
        dict2: dictionary which contains the count of occcurence (the value of each word (the key) in vector2)
        bagOfWords: list which contains all the unique words present in both vector1 and vector2
        finalVector1: vector corresponding to finalDoc1
        finalVector2: vector corresponding to finalDoc2
        dotProduct: the non-normalized dot product of finalVector1 and finalVector2
        
        INPUT:   finalDoc1, finalDoc2
        OUTPUT:  Jaccard Coefficient, Cosine Similarity'''
    
    vector1=[]
    for line in finalDoc1:
        vector1 = vector1 + line.split()

    dict1=dict(Counter(vector1))
    vector2=[]
    for line in finalDoc2:
        vector2 = vector2 + line.split()

    dict2=dict(Counter(vector2))
    totalNumberofWords=len(vector1)+len(vector2)

    commonWords=list((Counter(vector1) & Counter(vector2)).elements())
    commonNumberofWords=len(commonWords)
    jaccardCoefficient=(commonNumberofWords)/(totalNumberofWords)
    bagOfWords=list(set(vector1).union(vector2))
    
    finalVector1=[]
    finalVector2=[]
    for word in bagOfWords:
        a = dict1.get(word)
        b = dict2.get(word)
        if a!= None:
            finalVector1.append(a)
        else:
            finalVector1.append(0)

        if b!=None:
            finalVector2.append(b)
        else:
            finalVector2.append(0)
    

    for i in range(len(finalVector1)):
        if(finalVector1[i]!=0):
            finalVector1[i] = (1 + math.log(finalVector1[i], 10))
        if(finalVector2[i]!=0):
            finalVector2[i] = (1 + math.log(finalVector2[i], 10))
    
    norm1=0.0
    norm2=0.0
    dotProduct=0.0
    for i in range(len(finalVector1)):
        norm1 = norm1 + (finalVector1[i]*finalVector1[i])
        norm2 = norm2 + (finalVector2[i]*finalVector2[i])
        dotProduct += (finalVector1[i]*finalVector2[i])

    norm1=math.sqrt(norm1)
    norm2=math.sqrt(norm2)
    
    cosineSimilarity=(dotProduct)/(norm1*norm2)
    # print(cosineSimilarity)
    # print(commonWords)
    # print(commonNumberofWords)
    # print(totalNumberofWords)
    # print(jaccardCoefficient)
    # print(dict1)
    # print(dict2)
    # print(bagOfWords)
    # print(finalVector1)
    # print(finalVector2)
    return jaccardCoefficient,cosineSimilarity


# In[4]:


def tester(testFile, transDirection):
    
    ''' Takes the testFile as the input file which contains the test data and transDirection as the direction of translations
        Translated the testFile based on dictionary developed by the model
        Writes the translated output to translatedData.txt
        
        INPUT:   testFile with test data, translation direction
        OUTPUT:  --'''
    
    translator = str.maketrans('', '', '''!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~0123456789''')    
    
    #Read the test file line by line, remove punctuations and convert to lower case
    #Store it in testData
    fh=open(testFile,encoding="utf8")
    testData=[]
    for line in fh:
        s = line.lstrip().rstrip()
        if s != '':
            s=s.translate(translator)
            testData.append(s.lower())    
    fh.close()
    
    #Open correct dictionary based on transDirection
    if transDirection == 0: #Translate from English to Dutch
        fh = open('dictionaryEtoF.txt', encoding='utf8')
    else:                   #Translate from Dutch to English
        fh = open('dictionaryFtoE.txt', encoding='utf8')

    #Read the dictionary to memory
    dictionary = {}
    for line in fh:
        s = line.lstrip().rstrip().lower()
        trans = []
        if s != '':
            trans = s.split()
            dictionary[trans[0]] = trans[1]
    fh.close()
    
    #Translate the test file sentence by sentence
    #If word is not found in dictionary, don't translate
    sentence=[]
    predicted=str()
    for line in testData:
        sentence=line.split()
        translated=str()
        for word in sentence:
            if(dictionary.get(word) != None):
                translated = translated + dictionary[word] + ' '
            else:
                translated = translated + word + ' '
        predicted += translated + '\n'
    
    #Write the translated output to translatedData.txt
    fh = open('translatedData.txt','w+')
    fh.write(predicted)
    print('***Translated data has been written to the file, translatedData.txt***\n')
    fh.close()


# In[5]:


argumentList = sys.argv
filename1 = sys.argv[1]   #Name of the file which contains test data
filename2 = sys.argv[2]   #Name of the file which contains translated data
transDirection = int(sys.argv[3])   #Direction to translate to
                            #0: English to Dutch
                            #[1..infi]: Dutch to English
print(argumentList)
# filename1 = "testFile.txt"
# filename2 = "result.txt"
# transDirection = 0
# finalDoc1 = []
# finalDoc2 = []

print('Translating...')

tester(filename1, transDirection)

finalDoc1, finalDoc2 = readFile('translatedData.txt',filename2)
jaccardCoefficient, cosineSimilarity = parameterGeneration(finalDoc1,finalDoc2)

print('***Following are the parameters:***')
print('Cosine Similarity : ' + str(cosineSimilarity))
print('Jaccard Coefficient : ' + str(jaccardCoefficient))
