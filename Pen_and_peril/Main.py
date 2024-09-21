from Patterns import *
from Player import *
# hello
class Main:
    def __init__(self):
        self.menu()

    def menu(self):
        game.makeScreen()
        title=tink.Label(game.screen,text="Pen and Peril",font=("Calibri",30,))
        title.place(relx=0.3,rely=0.2)
        play=tink.Button(game.screen,text="start game",command=self.startGame)
        play.place(relx=0.4,rely=0.5)
        player=Player()
        while True:
            player.move()
            game.root.update()
            game.stall()

    def startGame(self):
        game.makeScreen()
        player=Player()
        monster=Enemy(player)
        monster.loadEasy()
        #monster.loadPatterns([[monster.stormPattern],[monster.stormPattern]])
        while player.lives>0:
            monster.upkeep()
            player.move()
            game.stall()
        self.endScreen()
    
    def endScreen(self):
        game.makeScreen()
        gameOver=tink.Label(game.screen,text="GAME OVER",font=("calibri",24,"bold"))
        gameOver.place(x=200,y=200)
        tryAgain=tink.Button(game.screen,text="try again",command=self.startGame)
        backToMenu=tink.Button(game.screen,text="back to menu",command=self.menu)
        tryAgain.place(x=240,y=430)
        backToMenu.place(x=230,y=500)
        while True:
            game.root.update()

Main()
