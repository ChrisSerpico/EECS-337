import nltk
from nltk.corpus import names  # for exercise 8
from nltk.corpus import brown  # for exercise 15
from nltk.corpus import reuters
from nltk.corpus import stopwords

## 1 - EXERCISES ##
print("----QUESTION 1----")
# 8 #
initials = nltk.ConditionalFreqDist(
    (fileid, name[0])
    for fileid in names.fileids()
    for name in names.words(fileid))
# male initials
print("Most common male first initials: "
      + str(initials['male.txt'].most_common()))
# female initials
print ("\nMost common female first initials: "
       + str(initials['female.txt'].most_common()))

# 15 #
# I left this commented out because it takes a while to generate a
# frequency distribution for the entire Brown Corpus
##brown_freq = nltk.FreqDist(w.lower() for w in brown.words())
##brownlist = []
##for word in brown_freq:
##    if brown_freq[word] >= 3:
##        brownlist.append(word)
##print ("Number of words in Brown Corpus that occur at least three times: "
##       + str(len(brownlist)))

# 17 #
# I'm using the second document in reuters for practice
frequent_words = nltk.FreqDist(w.lower() for w
                               in reuters.words(reuters.fileids()[1])
                               if w not in stopwords.words('english'))
print ("\n50 most common words in Reuters Corpus' second document: "
       + str(frequent_words.most_common(50)))

# 18 #
# Using the third document from reuters this time
frequent_bigrams = nltk.FreqDist(b for b
                                 in nltk.bigrams(
                                     reuters.words(reuters.fileids()[2]))
                                 if set(b).isdisjoint(
                                     stopwords.words('english')))
print ("\n50 most common bigrams in Reuters Corpus' third document: "
       + str(frequent_bigrams.most_common(50)))


## 2 - TF-IDF ##
print ("\n\n----QUESTION 2----")
# get the words of the first document in reuters corpus
document = reuters.words(reuters.fileids()[0])
# list of punctuation for elimination
punctuation = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
               '-', '_', '=', '+', '[', ']', '{', '}', '\\', ';', ':', '\'',
               '\"', ',', '.', '<', '>', '/', '?', '', ' ']

#get rid of unwanted text from document
cleandoc = [w for w in document
            if w.lower() not in stopwords.words('english')
            and set(w).isdisjoint(punctuation)]

# Generate unigrams
unigrams = nltk.FreqDist(
    word for word in cleandoc)
print ("\n10 most common unigrams in Reuters Corpus' first document: "
       + str(unigrams.most_common(10)))
# Generate bigrams
bigrams = nltk.FreqDist(
    bg for bg in nltk.bigrams(cleandoc))
print ("\n10 most common bigrams in Reuters Corpus' first document: "
       + str(bigrams.most_common(10)))
# Generate trigrams
trigrams = nltk.FreqDist(
    tg for tg in nltk.trigrams(cleandoc))
print ("\n10 most common trigrams in Reuters Corpus' first document: "
       + str(trigrams.most_common(10)))
