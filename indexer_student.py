# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        """
        ["1st_line", "2nd_line", "3rd_line", ...]
        Example:
        "How are you?\nI am fine.\n" will be stored as
        ["How are you?", "I am fine." ]
        """
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0

        """ self.index is a dictionary with word as key and
        list of tuples (line#, msg_line) as value
        {word1: [(line_number_of_1st_occurrence, 'msg1'),
                 (line_number_of_2nd_occurrence, 'msg2'),
                 ...]
          word2: [(line_number_of_1st_occurrence, 'msg1'),
                 (line_number_of_2nd_occurrence, 'msg2'),
                  ...]
         ...
        }
        """
        self.load_poems()
    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    # implement
    def add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.msgs.append(m.strip('\n'))
        self.total_msgs += 1
        # ---- end of your code --- #
        return 

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """

        # IMPLEMENTATION
        # ---- start your code ---- #
        a = m.split()
        
        for i in a:
            if i not in self.index:
                self.index[i] = [(l, m.strip('\n'))]
            else:
                self.index[i].append((l, m.strip('\n')))

        # ---- end of your code --- #
        return

    # implement: query interface

    def search(self, term):
        """
        return a list of tupple.
        Example:
        if index the first sonnet (p1.txt),
        then search('thy') will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
        """
        msgs = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        
        for i in self.msgs:
            if term in i:
                msgs.append((self.msgs.index(i), i))
    

        # ---- end of your code --- #
        return msgs
    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        f = open('AllSonnets.txt','r')
        file = f.readlines()
        for i in file:
            self.add_msg_and_index(i)
            self.indexing(i, self.total_msgs - 1)
        l = self.msgs
        # ---- end of your code --- #
        
        return l 
    

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        idx = Index('a')
        f = open('AllSonnets.txt','r')
        file = f.readlines()
        for i in file:
            idx.add_msg_and_index(i)
            idx.indexing(i, idx.total_msgs)
        l = idx.msgs
        # ---- end of your code --- #
        return l

    def get_poem(self, p):
        """
        p is an integer, get_poem(1) returns a list,
        each item is one line of the 1st sonnet

        Example:
        get_poem(1) should return:
        ['I.', '', 'From fairest creatures we desire increase,',
         " That thereby beauty's rose might never die,",
         ' But as the riper should by time decease,',
         ' His tender heir might bear his memory:',
         ' But thou contracted to thine own bright eyes,',
         " Feed'st thy light's flame with self-substantial fuel,",
         ' Making a famine where abundance lies,',
         ' Thy self thy foe, to thy sweet self too cruel:',
         " Thou that art now the world's fresh ornament,",
         ' And only herald to the gaudy spring,',
         ' Within thine own bud buriest thy content,',
         " And, tender churl, mak'st waste in niggarding:",
         ' Pity the world, or else this glutton be,',
         " To eat the world's due, by the grave and thee.",
         '', '', '']
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        l = self.load_poems()
        roman1 = self.int2roman[p] + '.'
        roman2 = self.int2roman[p+1] + '.'
#        index_1 = l.index(roman1) 
#        index_2 = l.index(roman2) 

        
        
# =============================================================================
        index_1 = self.search(roman1)[0][0]
        index_2 = self.search(roman2)[0][0]
  
#         #怎么用search解决？
#  
#         print(l1)
#         print(l2)
# =============================================================================
        
        poem = l[index_1:index_2]
        
        
        #search the number of the poem

        

        # ---- end of your code --- #
        return poem

if __name__ == "__main__":
    s1 = Index("AllSonnets.txt")
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = s1.search("love")
    print(s_love)












