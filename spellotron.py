"""
File: CS1 PROJECT SPELLOTRON
Author: Lea Boyadjian
"""

import sys

LEGAL_WORD_FILE = open("american-english.txt")
KEY_ADJACENCY_FILE = open("keyboard_letters.txt")
ALPHABET = tuple(chr(code) for code in range(ord('a'), ord('z') + 1))

def ultimate_list(file):
    """
    :param filename: the file
    :return: the file in a list
    """
    all = []
    for line in open(file):
        line = line.split()
        for word in line:
            all.append(word)
    return all

def keyboard_letters_dictionary():
    """
    This function takes the keyboard text file and make it into a dictionary.
    The key is the alphabet and the value is the neighboring letters.
    :return: dictionary where key is the alphabet and values are the adjacent letters
    """
    d = {}
    for line in KEY_ADJACENCY_FILE:
        line = line.split()
        # setting the alphabet as key
        key = line[0]
        # setting the values with the letters that follow after the key
        value = line[1:]
        d[key] = value
    return d

def american_english_dictionary():
    """
    The goal of this function is to return a dictionary of the american_english text file.
    What I noticed in the text file is that before moving on to the next letter in the
    alphabet, the text file starts with the letter and proceeds to include in the following
    lines words that starts with that letter. firstline takes this into account and essentially
    keeps track of the alphabet.
    :return: dictionary where key is the alphabet and values (set) are the words that
    begin with that letter
    """
    d2 = {}
    # firstline starts off as "A"
    firstline = LEGAL_WORD_FILE.readline().strip()
    # making the values as set
    var = set(firstline)
    d2[firstline] = var
    for line in LEGAL_WORD_FILE:
        # checks if the first letter in the line equals to firstline (the alphabet)
        if line[0] == firstline[0]:
            line = line.strip()
            # adds the line to the set of values
            d2[firstline[0]].add(line)
        else:
            line = line.strip()
            # this updates firstline to the next letter
            firstline = line[0]
            d2[firstline] = set(line)
    return d2

def check_if_right(file, d2):
    """
    This function checks and separates which words are spelled wrong
    and which one are spelled correctly. Those who are spelled incorrectly
    are added to wrong_spelling and those who are spelled correctly
    they are added to right_spelling.
    :param file: file that will be corrected
    :param d2: the american english dictionary
    :return: a list of words that are spelled wrong, a list of words that are
     spelled correctly, number of words counted from the file as well as a list
     of indices of the words that are not spelled correctly
    """
    wrong_spelling = []
    right_spelling = []
    word_count = 0
    z = -1
    indices_lst = []
    for line in open(file):
        line = line.split()
        # counts how many words there are
        word_count += len(line)
        for word in line:
            z+=1
            # separates the file into two list
            if word in d2[word[0]]:
                right_spelling.append(word)
            else:
                indices_lst.append(z)
                wrong_spelling.append(word)
    return wrong_spelling, right_spelling, word_count, indices_lst

def solve_adj(wrong_spelling, d, d2, all, indices_lst):
    """
    This function is dedicated to fixing the misspelling of words that the
    user finger accidentally hit a key adjacent to the intended one instead of
    the intended one
    :param wrong_spelling: the list of words spelled incorrectly
    :param d: the dictionary of keyboard text file
    :param d2: the dictionary of american english file
    :return: a list of words that were able to be corrected by solve_adj and
    a list of words that were unable to be solved (probs will be solved because of
    extra key or missing key)
    """

    spelling_corrected = [] # corrected spelling goes here
    spelling_not_corrected = [] # misspelling goes here
    hold = [] # this list holds all the wrong words
    for idx in range(len(wrong_spelling)):
        done = 0
        word = wrong_spelling[idx]
        for i in range(len(word)):
            # an extra break that ensures the loop continues to the next word
            if done == 1:
                break
            ch = word[i]
            lst = d[ch] # the values from keyboard file dictionary
            for c in lst:
                if i > 0:
                    # a form of inserting a letter into the word
                    new = word[:i] + c + word[i+1:]
                else:
                    new = c + word[1:]
                lst2 = d2[new[0]] # the set of values from american english dictionary
                if new in lst2:
                    # adds new correct spelling to list
                    spelling_corrected.append(new)
                    # adds the misspelled version to list
                    hold.append(word)
                    # replaces the wrong spelling with the correct spelling
                    all[indices_lst[idx]] = new
                    done = 1 # extra break
                    break
        if word not in hold:
            # adds words that were unable to be corrected to list
            spelling_not_corrected.append(word)
    return spelling_corrected, spelling_not_corrected, all, indices_lst

def missing_key(spelling_corrected, spelling_not_corrected, d2, all, indices_lst):
    """
    This function is dedicated to finding the missing key stroke that was left out
    and insert it back into the word in the correct spot and then append it
    to spelling corrected list.
    :param spelling_corrected: a list of words that were fixed and now are spelled correct
    :param spelling_not_corrected: a list of words that were unable to be fixed
    :param d2: dictionary of american english file
    :return: list of correctly spelled words, list of words that are not spelled correctly and
    a list of all the words in the file
    """
    i = 0
    for word in spelling_not_corrected:
        for letter in word:
            # made into a list since strings are immutable
            original = list(word)
            temp = list(word)
            # ensures that all letters of the alphabet are tried before moving on to next word
            for l in range(len(ALPHABET)):
                # alphabet is a tuple so I changed it into a str here
                temp.insert(i, str(ALPHABET[l]))
                # bring them back to a str so the function can check if its correct
                temp = ''.join(temp)
                lst2 = d2[temp[0]]
                if temp in lst2:
                    # removes the word from the list since it is now corrected
                    spelling_not_corrected.remove(''.join(original))
                    spelling_corrected.append(temp)
                    break
                else:
                    # shallow copy of list unchanged when modify
                    temp = original.copy()
            # ensures incrementation
            i += 1
        # resets for the next word
        i = 0
    return spelling_corrected, spelling_not_corrected, all, indices_lst

def extra_key(spelling_corrected, spelling_not_corrected, d2):
    """
    This function focuses on the misspelling due to an extra key that was
    accidentally typed. Has a lot of similarity to missing keys except I
    am deleting the extra key and not using i for incrementation.
    :param spelling_corrected: a list of words that are now spelled correctly
    :param spelling_not_corrected: a list of words that were unable to be fixed
    :param d2: dictionary of american english file
    :return: the final list of words that are now spelled correctly and the final
    list of words that are unknown or have multiple errors
    """
    # This is a copy to avoid any annoying errors since I'm moving a lot of things around
    copy = spelling_not_corrected[:]
    for word in copy:
        original = list(word)
        temp = list(word)
        for l in range(len(original)):
            # this deletes the extra key
            del temp[l]
            temp =''.join(temp)
            lst2 = d2[temp[0]]
            if temp in lst2:
                spelling_not_corrected.remove(''.join(original))
                spelling_corrected.append(temp)
                break
            else:
                temp = original.copy()
    return spelling_corrected, spelling_not_corrected

def count_unknown(spelling_not_corrected):
    """
    :param spelling_not_corrected: a list of words that are completely unknown
    :return: how many words there are in this list
    """
    unknown_count = 0
    for word in spelling_not_corrected:
        unknown_count += 1
    return unknown_count

def count_wrongtotal(spelling_not_corrected, wrong_spelling):
    """
    :param spelling_not_corrected: a list of words that are not spelled correctly
    :param wrong_spelling: the original list of unknown words before corrected
    :return: a list of misspelled words that were able to be corrected and
    how many words there are in that list
    """
    i = 0
    words_corrected_count = 0
    words_corrected = []
    for word in wrong_spelling:
        if word not in spelling_not_corrected:
            words_corrected.append(wrong_spelling[i])
            words_corrected_count += 1
        # ensures incrementation
        i += 1
    return words_corrected, words_corrected_count

def main():

    mode = sys.argv[1]
    sys.args = ["spellotron.py", mode]


    if len(sys.argv) == 3:
        file = sys.argv[2]
    if len(sys.argv) == 2:
        file = input("Enter name of plain text file: ")
    if len(sys.argv) > 3:
        print("Error")

    all = ultimate_list(file)
    d = keyboard_letters_dictionary()
    d2 = american_english_dictionary()
    wrong_spelling, right_spelling, word_count, indices_lst = check_if_right(file,d2)
    spelling_corrected, spelling_not_corrected, all, indices_lst = solve_adj(wrong_spelling, d, d2, all, indices_lst)
    spelling_corrected, spelling_not_corrected, all, indices_lst = missing_key(spelling_corrected, spelling_not_corrected, d2, all, indices_lst)
    spelling_corrected, spelling_not_corrected = extra_key(spelling_corrected, spelling_not_corrected, d2)

    unknown_count = count_unknown(spelling_not_corrected)
    words_corrected, words_corrected_count = count_wrongtotal(spelling_not_corrected, wrong_spelling)


    if mode == "words":
        for i in range(len(words_corrected)):
            print(words_corrected[i], "->", spelling_corrected[i])
    if mode == "lines":
        merge = " ".join(all)
        print(merge)

    print()
    print(word_count, "words read from file")
    print()
    print(words_corrected_count, "Corrected Words")
    print(words_corrected)
    print()
    print(unknown_count, "Unknown Words")
    print(spelling_not_corrected)
    print()

main()