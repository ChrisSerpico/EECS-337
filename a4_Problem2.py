import nltk
from nltk.corpus import names  # for exercise 8
from nltk.corpus import brown  # for exercise 15
from nltk.corpus import reuters
from nltk.corpus import stopwords

## 1 - EXERCISES ##
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

# First document in reuters corpus
document = reuters.fileids()[0]

# Generate unigrams
unigrams = nltk.ConditionalFreqDist(
    (document, word)
    for word in reuters.words(document)
        if word not in stopwords.words('english'))
print unigrams[document].most_common(20)
