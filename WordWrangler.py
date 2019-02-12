"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_duplicates = []
    num = 0
    while num <= len(list1) - 1:
        no_duplicates.append(list1[num])
        i = 1
        if num < len(list1) - 1:
            while list1[num] == list1[num + i]:
                i += 1
                if num + i > len(list1) - 1:
                    break
        num += i
            
    return no_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if len(list1) == 0 or len(list2) == 0:
        return []
    elif list1[0] > list2[-1] or list1[-1] < list2[0]:
        return []
    else:
        if(list1[0] <= list2[0]):
            first_list = list1
            second_list = list2
        else:
            first_list = list2
            second_list = list1
        intersect_list = []
        num = 0
        index = 0
    
        while num < len(second_list) and index < len(first_list):
            while second_list[num] > first_list[index]:
                index += 1
                if index > len(first_list) - 1:
                    break
            if index < len(first_list):
                if second_list[num] == first_list[index]:
                    intersect_list.append(second_list[num])
                    index += 1
            num += 1
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """ 
    if len(list1) == 0:
        return list2
    elif len(list2) == 0:
        return list1
    elif list1[0] <= list2[0]:
        first_list = list1
        second_list = list2
    else:
        first_list = list2
        second_list = list1
    sorted_list = []
    index = 0
    for num1 in range(len(second_list)):
        if index < len(first_list):
            while first_list[index] < second_list[num1]:
                sorted_list.append(first_list[index])
                index += 1
                if index > len(first_list) -1:
                    break
        sorted_list.append(second_list[num1])
    if index < len(first_list):
        sorted_list = sorted_list + first_list[index:]
    return sorted_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    if len(list1) == 2:
        return merge(list1[:1], list1[1:])
    else:
        list11 = merge_sort(list1[0:(len(list1)/2)])
        list12 = merge_sort(list1[len(list1)/2:])
        return merge(list11, list12)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    if len(word) == 1:
        return ['', word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        all_possibles = []
        for item in rest_strings:
            for ind in range(len(item)+1):
                new = item[:ind] + first + item[ind:]
                all_possibles.append(new)
        return rest_strings + all_possibles 

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    doc = urllib2.urlopen(url)
    words = []
    for line in doc.readlines():
        words.append(line[:-1])
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    