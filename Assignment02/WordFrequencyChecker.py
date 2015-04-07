# -*- coding:utf-8 -*-
import re, csv, os

class WordFrequencyChecker:

    def __init__(self):
        pass

    def isEnglishWord(self, word): 
        """ Checking English word Return True if word is English word. Otherwise, return False.
        >>> isEnglishWord("The")
        True
        >>> isEnglishWord("the food")
        False
        >>> isEnglishWord(".")
        False
        >>> isEnglishWord("100K")
        False
        """
        if re.match('^[a-zA-Z]*$', word):
            return True
        else:
            return False

    def replaceWordToLowerWord(self, word):
        """Change word to lowercase
        >>> replaceWordToLowerWord("As")
        "as"
        >>> replaceWordToLowerWord("AssIgNMent")
        "assignment"
        """
        if self.isEnglishWord(word):
            return word.lower()
        else:
            return None

    def countWord(self, dicOfNumberOfWords, word):
        """If word existed in the dictionary, increase its counting value to 1.
        Otherwise, make a new key-value for dictionary and set its counting value is 1.
        >>> countWord({"the":2, "word":3}, "the")
        #{"the":3, "word":3}
        >>> countWord({"the":2, "word":3}, "love")
        #{"the":2, "word":3, "love":1}
        """
        if {word}.issubset(dicOfNumberOfWords):
            dicOfNumberOfWords[word] = dicOfNumberOfWords[word] + 1
        else:
            dicOfNumberOfWords[word] = 1

    def getSortedListFromDicOfNumberOfWords(self, dicOfNumberOfWords):
        """Sort the dictionary according to key field. The returned list is the list of tuples (word, frequency)
        The returned list has the descending order of frequency.
        >>> getSortedListFromDicOfNumberOfWords({"the":2, "word":3, "love":1})
        [("word", 3), ("the", 2), ("love", 1)]
        """
        return sorted(dicOfNumberOfWords.items(), key=lambda dicOfNumberOfWords: dicOfNumberOfWords[1], reverse=True)

    #Soon-gyo
    def check(self, rfcFilePath):
        """Read the RFC files and display the frequency of words in a CSV file.
        >>> check("rfc.txt")
        word : 3
        the : 2
        love : 1
        output : rfc_checked.txt
        """
        with open(rfcFilePath, 'r') as rfcFile:
            lines = rfcFile.readlines()
            dicOfNumberOfWords = {}
            for line in lines:
                for word in re.split(r"[\W]+", line):
                    if word != "" and self.isEnglishWord(word):
                        self.countWord(dicOfNumberOfWords , self.replaceWordToLowerWord(word))

            sortedList = self.getSortedListFromDicOfNumberOfWords(dicOfNumberOfWords)

            self.writeCSV(os.path.splitext(os.path.basename(rfcFilePath))[0] + "_checked.csv", sortedList)

    def writeCSV(self, fileName, wordList):
        """Write the returned list to CSV file.
        >>> writeCSV("rfc.txt", [("word", 3), ("the", 2), ("love", 1)])
        output : rfc_checked.txt
        """
        with open(fileName, 'wb') as csvfile:
            w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (word, count) in wordList:
                w.writerow([word, count])

if __name__ == "__main__":
    wordFrequencyChecker = WordFrequencyChecker()
    wordFrequencyChecker.check("./RFCs/rfc2251.txt")
    wordFrequencyChecker.check("./RFCs/rfc6850.txt")
    wordFrequencyChecker.check("./RFCs/rfc6871.txt")
    wordFrequencyChecker.check("./RFCs/rfc6876.txt")