# force floating point division
from __future__ import division

import nltk
import collections
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
cleandoc = [w.lower() for w in document
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

# Observations about the 20 most common unigrams, bigrams and trigrams
# The first thing I noticed that I thought was interesting was that
# the most common unigrams, bigrams, and trigrams are all different.
# What I mean is that the most common unigrams are not necessarily present
# in the most common bigrams and so forth. This means that a lot of words
# that are very common are being used in multiple different places, while
# some groups of words are pretty much only used in that grouping, and not
# elsewhere, explaining their absence from the common unigrams. The other thing
# I noticed is that it's suprisingly easy to get a vague idea of what the
# article is about while only looking at the most commonly used words. We can
# see that the article is about the United States, South korea, Hong Kong,
# and Japan, and involves business and trade worth billions of dollars. It also
# appears to involve electronics and diplomacy, although it's more difficult
# to tell exactly what kinds or in what capacity.

# Counter for unigrams
unicounter = collections.Counter()
for fid in reuters.fileids():
    for word in list(unigrams):
        dist = nltk.FreqDist(w.lower() for w in reuters.words(fid))
        for distword in list(dist):
            if word == distword:
                unicounter[word] += 1
# calculate df
for c in unicounter:
    unicounter[c] = (unicounter[c]/len(reuters.fileids()))

print("\n20 unigrams with highest document frequency: "
      + str(unicounter.most_common(20)))

# Counter for bigrams
bicounter = collections.Counter()
for fid in reuters.fileids():
    for word in list(bigrams):
        lowerwords = (wd.lower() for wd in reuters.words(fid))
        dist = nltk.FreqDist(w for w in nltk.bigrams(lowerwords))
        for distword in list(dist):
            if word == distword:
                bicounter[word] += 1
# calculate df
for c in bicounter:
    bicounter[c] = (bicounter[c]/len(reuters.fileids()))
            
print("\n20 bigrams with highest document frequency: "
      + str(bicounter.most_common(20)))

# Counter for trigrams
tricounter = collections.Counter()
for fid in reuters.fileids():
    for word in list(trigrams):
        lowerwords = (wd.lower() for wd in reuters.words(fid))
        dist = nltk.FreqDist(w for w in nltk.trigrams(lowerwords))
        for distword in list(dist):
            if word == distword:
                tricounter[word] += 1
# calculate df
for c in tricounter:
    tricounter[c] = (tricounter[c]/len(reuters.fileids()))

print ("\n20 trigrams with highest document frequency: "
       + str(tricounter.most_common(20)))

# Observations
# Of course, the only n-grams we look at are the n-grams we retrieved from the
# first reuters document. However, looking at their document frequence, it's
# interesting to note that the df is tremendously low for almost every n-gram.
# A couple of the unigrams have noticably high ocurrences, but they're very
# common words, such as "said". This means that even for words with high
# frequency in a single document, different documents are very capable of
# having extremely different language. Finally, some words that appeared very
# often in the on document had a low document frequency and vice versa. This
# ultimately means that it's pretty much impossible to extract how common a
# word generally is if we only know how common it is in a single document. It
# also means that words with a high frequency in a single document but a low
# document frequency are good for identifying that document, as they're rarer
# and thus will create less overlap. 


# Calculate tf-idf
unitfidf = collections.Counter()
for word in list(unigrams):
    unitfidf[word] = (unigrams[word] / unicounter[word])
bitfidf = collections.Counter()
for word in list(bigrams):
    bitfidf[word] = (bigrams[word] / bicounter[word])
tritfidf = collections.Counter()
for word in list(trigrams):
    tritfidf[word] = (trigrams[word] / tricounter[word])

# print tf-idfs
print ("\n20 unigrams with highest tf-idf: "
       + str(unitfidf.most_common(20)))
print ("\n20 bigrams with highest tf-idf: "
       + str(bitfidf.most_common(20)))
print ("\n20 trigrams with highest tf-idf: "
       + str(tritfidf.most_common(20)))

# Observations
# The main observation I had here was that, while tf-idf has many words and
# phrases that we've seen in the previous sections, it heavily weights words
# and phrases that are common within the document we're looking at, but less
# common overall. This means that we're looking more at terms that could
# potentially differentiate the document from other documents.


## 3 - Applying TF-IDF ##
# a.
#   I would say that no, the dictionaries we've developed for this specific
# document would not be very useful if we're using them on non-reuters
# sources. That's because we've developed a very specific dictionary: the
# tf-idf of words in a given document when compared to the corpus the
# document is from. The way in which I wrote this program means that we're
# essentially comparing everything to the specified document. That means that
# comparing this document to things not in the reuters corpus would simply
# be seeing whether a certain corpus (not reuters) is similar to a document
# from reuters. It won't tell us a lot about the corpuse, just the relationship
# between the corpus and our document. While that could be helpful in some
# cases, it would be much more useful to create new dictionaries from the
# new document and new corpus, which would give us a more pertinent comparison
# and allow for more extrapolation about both the new corpus and new document.

# b.
#   The first thing I would do would be to look at those same words in other
# documents of similar length and topic. If the first word almost always
# occurs 10 times in a document of similar length on a similar topic, it
# occurring 10 times is almost meaningless. However, if it never appeared
# in similar documents, the fact that it appears 10 times in this document
# is VERY meaningful. If we quantify both words in the same way (How often
# does this word appear in similar documents? How different is that number
# to the number of times it appears in this document?), we can then compare
# them to each other. This is basically asking which word is more unique
# in a document of this type, which allows us to compare the significance
# of each one.

# c.
#   I would say that the word is more significant in the first article. This is
# because the word shows up 5 times out of 500 words, or once every 100 words.
# In the second article, the word shows up 6 times out of 1000 words, or 3 times
# every 500 words. The first fraction is larger, meaning the word shows up more
# often for the given number of words, even though the absolute number of
# appearances is larger in the second document. Thus we know that the first
# word takes up a larger percentage of the document, meaning it is more
# significant to the topic at hand. This method would probably be less
# neccessary with tweets. This is simply because tweets are so short (140
# characters or less): any word that shows up is significant by design.
# There just isn't enough space for superfluous words.
