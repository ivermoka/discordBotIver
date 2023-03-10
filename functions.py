import random

def checkWinner(winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] and board[condition[2]] == mark:
                gameOver = True

def get_valid_word(words):
        word = random.choice(words)
        while "-" in words or " " in words:
            word = random.choice(words)
        return word