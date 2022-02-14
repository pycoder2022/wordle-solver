
import sys
import os
import re

# Download file https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt
# Save to ~/wordle/5lw.txt

class Solver():
    def __init__(self):
        self.not_found = []
        self.__load()

    def __load(self):
        data = open(os.path.expanduser("~/wordle/5lw.txt")).read().split("\n")
        data = [w.strip() for w in data]
        self.all_words = [w for w in data if len(w) == 5 ]

        self.letter_freq = {}

        print ("TOTAL DICTIONARY SIZE", len(self.all_words))
        for w in self.all_words:
            for c in w:
                if c not in self.letter_freq:
                    self.letter_freq[c] = 0

                self.letter_freq[c] += 1

    def get_freq(self, w):
        freq = 0
        done_c = set()
        for c in w:
            if c in done_c:
                continue

            done_c.add(c)
            freq += self.letter_freq.get(c, 0)
        
        return freq

    def get_best(self, words, n=1):
        freqs = []

        for w in words:
            freqs.append({'word': w, 'freq': self.get_freq(w)})

        freqs = sorted(freqs, key=lambda x: x['freq'], reverse=True)
        freqs = freqs[:n]

        return [w['word'] for w in freqs]

    def get_best_initial_words(self, n=5):
        return self.get_best(self.all_words, n=n)

    def get_next(self, word, score):
        if len(word) != 5 or len(score) != 5:
            print ("Invalid input")
            return None

        pattern = [ '.', '.', '.', '.', '.']
        somwehere = []
        somwehere_chars = []
        confirmed = []

        for i in range(5):
            c = word[i]
            s = score[i]

            if s not in [ "0", "1", "2" ]:
                print ("Invalid score. Must be only 0 or 1 or 2")
                return

            if s == "0":
                self.not_found.append(c)

            elif s == "2":
                confirmed.append(c)
                pattern[i] = c
            else:
                spat = list(pattern)
                spat[i] = '[^'+c+']'
                somwehere.append("".join(spat))
                somwehere_chars.append(c)

        pat = "".join(pattern)

        # print (pat)
      
        matches = [w for w in self.all_words if re.match(pat, w) ]

        
        for i in range(len(somwehere_chars)):
            matches = [w for w in matches if somwehere_chars[i] in w]
            matches = [w for w in matches if re.match(somwehere[i], w)]
        
        nf = set(self.not_found)
        for c in nf:
            if c in somwehere_chars or c in confirmed:
                continue

            matches = [w for w in matches if c not in w]
        
        #print (" ".join(matches))

        print ("Final {} matches".format(len(matches)))

        if len(matches) == 0:
            return None

        matches = self.get_best(matches, n=5)

        return "\n".join(matches)

    def process_stdin(self):
        while True:
            inp = input("> ")
            inp = inp.strip()
            words = inp.split(" ")

            if inp.lower() in [ "q", "quit", "exit" ]:
                return

            if inp.lower() in [ "reset" ]:
                self.not_found = []
                rec = self.get_best_initial_words()
                print ("\n".join(rec).upper())

                continue

            if len(words) != 2:
                print("enter WORD SCORE")
                continue
            
            word = words[0].lower()
            score = words[1]
            next_word = self.get_next(word, score)
            if not next_word:
                continue

            print ()
            print (next_word.upper())
            print ()
    

if __name__ == "__main__":
    solver = Solver()

    solver.process_stdin()

    sys.exit(0)

    