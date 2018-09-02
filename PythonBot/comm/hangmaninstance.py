import discord, log, string
from discord.ext import commands
from discord.ext.commands import Bot

RIGHT = 0
WRONG = 1
GAMEOVER = 2
WIN = 3
MAXFAULTS = 6


# Normal commands
class HangmanInstance:
    def __init__(self, word: str):
        self.word = word
        self.faults = 0
        self.guesses = []
        self.wrongguesses = []

    def guess(self, l):
        # Invalid guess
        l = l.lower()
        if (l not in self.word.lower()) & (l not in self.wrongguesses):
            self.faults += 1
            if l not in self.wrongguesses:
                self.wrongguesses.append(l)
            if self.faults >= MAXFAULTS:
                return GAMEOVER
            return WRONG
        if l not in self.guesses:
            self.guesses.append(l)
        for x in self.word.lower().translate(str.maketrans('', '', string.punctuation)):
            if (x.isalpha()) & (x not in self.guesses):
                return RIGHT
        return WIN

    def __str__(self):
        s = ""
        for x in self.word:
            if x.isalpha():
                if x.lower() in self.guesses:
                    s += str(x)
                else:
                    s += "\_"
            else:
                s += str(x)
        return s
