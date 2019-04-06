import random as rn
import tkinter
import time


class Dice:
    'Dice class'

    # Current value on dice
    number = 0
    
    def __init__ (self):
        return

    # Dice rolled
    def diceRolled (self):
        Dice.number = rn.randint(1, 6)
        return Dice.number


class Player:
    'Player class'

    # Dice object common to all players
    dice = Dice()

    
    def __init__ (self, id, game):
        self.id = id
        self.score = 0
        self.diceval = 0
        Player.game = game # Game common to all players

    # Player rolls the dice
    def rollDice (self):
        self.diceval = Player.dice.diceRolled()

    # Player performs the move
    def doMove (self):
        self.score += self.diceval

    # Check if Player wins or not
    def checkWin (self):
        if (self.score >= 100):
            Game.gamestat = True
            print ("Player", self.id," wins......!!!!")

    def showScore (self):
        print ("Current score of Player", self.id, ": ", self.score)

    def setColor (self, color):
        self.color = color



class Gui:
    'Class creating Gui'

    root = tkinter.Tk(  )
    board = []
    scoreLabels = []

    colors = ['red', 'green', 'pink', 'gray']

    def __init__(self, noOfPlayers):

        # Create board
        boardFrame = tkinter.Label(Gui.root)
        for r in range(10):
           for c in range(10):
               if r % 2 == 0:
                   cell = tkinter.Label(boardFrame, text='%s'%((r*10+c)+1), bg='blue', borderwidth=1, width=7, height=3, relief='solid')
                   Gui.board.append(cell)
                   #Gui.board[(r*10+c)] = cell
                   cell.grid(row=r,column=c)
               else:
                   cell = tkinter.Label(boardFrame, text='%s'%((r+1)*10-c), bg='blue', borderwidth=1, width=7, height=3, relief='solid')
                   Gui.board.append(cell)
                   #Gui.board[(r*10+c)-1] = cell
                   cell.grid(row=r,column=c)

        boardFrame.pack(side="top", fill="both", expand=False)

        # Create bottom scores frame
        labelframe = tkinter.LabelFrame(Gui.root, text="Snake and Ladders Game")
        labelframe.pack(side="bottom", fill="both", expand=True)

        for i in range(1, noOfPlayers+1):
            player = tkinter.Label(labelframe, text="Player%s Score: 0" % i,fg=Gui.colors[i-1])
            player.pack()
            Gui.scoreLabels.append(player)

        # Show labels for snakes and ladders colors
        labelSnake = tkinter.Label(labelframe, text="Snake", bg='blue',fg='yellow')
        labelLadder = tkinter.Label(labelframe, text="Ladder", bg='blue',fg='white')
        labelSnake.pack(side='left')
        labelLadder.pack(side='right')

    # Returns root
    def getRoot (self):
            return (Gui.root)

    # Return Board
    def getBoard (self):
            return (Gui.board)

    def putLaddersOnBoard (self, ladders):
        for ladder in ladders:
            Gui.board[ladder-1].config(fg='white')

    def putSnakesOnBoard (self, snakes):
        for snake in snakes:
            Gui.board[snake-1].config(fg='yellow')

    def updateColors (self, player, i):
        if i:
            if player.score <= 100:
                Gui.board[player.score-1].config(bg = Gui.colors[player.id-1])
            else:
                Gui.board[90].config(bg = Gui.colors[player.id-1])
        else:
            Gui.board[player.score-1].config(bg = 'blue')
        Gui.root.update()

    def updateScore (self, player):
        Gui.scoreLabels[player.id-1].config(text='Player %s Score: %s'% (player.id, player.score))




class Game:
    'Game class'

    # List of Players playing the Game
    players_list = []


    # Snake positions with losses on board
    snakes = {15: 5,
              37: 10,
              50: 8,
              57: 12,
              79: 6,
              99: 14}

    # Ladder positions with earnings on board
    ladders = {25: 4,
               40: 10,
               54: 7,
               87: 5}
    
    # Indicates whether the Game is on or not
    gamestat = False
    
    def __init__ (self, noOfPlayers):
         # Create Game GUI
        Game.gui = Gui(noOfPlayers)
        Game.gui.putSnakesOnBoard(Game.snakes)
        Game.gui.putLaddersOnBoard(Game.ladders)
        return

    # Add a Player to the Game
    def addPlayer (self, player):
        player.setColor(Game.gui.colors[player.id-1])
        Game.players_list.append(player)


    # Checks if Player encountered a Snake or a Ladder
    def checkSnakeorLadder (self, player):
        for pos in Game.snakes:
            if player.score == pos:
                player.score -= Game.snakes[pos]
                print ("Player", player.id," encountered a snake...")
                player.showScore()
                return
        for pos in Game.ladders:
            if player.score == pos:
                player.score += Game.ladders[pos]
                print ("Player", player.id," encountered a ladder...")
                player.showScore()
                break

    # Play the Game
    def playGame (self):
        root = Game.gui.getRoot()
        board = Game.gui.getBoard()
        
        # Loop till one of the player wins
        while Game.gamestat != True:
            
            # Players exchange turns
            for player in Game.players_list:
                if Game.gamestat == True:
                    break

                #board[player.score-1].config(bg ='blue')
                Game.gui.updateColors(player, False)
                player.rollDice()
                player.doMove()
                player.showScore()
                self.checkSnakeorLadder(player)
                player.checkWin()
                Game.gui.updateColors(player, True)
                Game.gui.updateScore(player)
                time.sleep(0.5)
                

        
        
# Program entrance
if __name__ == '__main__':

    noOfPlayers = 2
    
    # Game object
    myGame = Game(noOfPlayers)

    # Create player objects
    for i in range(1, noOfPlayers + 1):
        player = Player(i, myGame)
        myGame.addPlayer(player)

    # Play the game
    myGame.playGame()
    #root.mainloop(  )
