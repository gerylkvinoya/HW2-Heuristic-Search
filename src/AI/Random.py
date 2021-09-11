import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Random")
    
    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

    ##
    #utility
    #Description: examines GameState object and returns a heuristic guess of how
    #               "good" that game state is on a scale of 0 to 1
    #
    #               a player will win if his opponent’s queen is killed, his opponent's
    #               anthill is captured, or if the player collects 11 units of food
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: the "guess" of how good the game state is
    ##
    def utility(self, currentState) -> float:
        
        #2 for the homework, designing a dictionary data structure for a 'node'
        #node = {'move': getMove(currentState), 'state': utility(currentState), 'depth': 1, }

        #get the my inventory and the enemy inventory
        myInv = getCurrPlayerInventory(currentState)
        enemyInv = getEnemyInv(currentState)

        #get the values of the queen, anthill, and foodcount
        myQueen = myInv.getQueen()
        myQueenHealth = myQueen.health
        myAntHill = myInv.getAnthill()
        myAntHillHealth = myAntHill.captureHealth
        myFoodCount = myInv.foodCount

        enemyQueen = enemyInv.getQueen()
        enemyQueenHealth = enemyQueen.health
        enemyAntHill = enemyInv.getAnthill()
        enemyAntHillHealth = enemyAntHill.captureHealth
        enemyFoodCount = enemyInv.foodCount

        #will modify this toRet value based off of gamestate
        toRet = 0.5



        #check for the start of game
        #foodCount should be 0, queen should have full health (10),
        #   anthill should have full capture health(3)
        if (myFoodCount == 0 and enemyFoodCount == 0 and
            myAntHillHealth == 3 and enemyAntHillHealth == 3 and
            myQueenHealth == 10 and enemyQueenHealth == 10):
            #toRet should be 0.5 at this point
            return toRet
        

        #food count
        myFoodCountScale = myFoodCount/11
        enemyFoodCountScale = enemyFoodCount/11
        foodCountDiff = myFoodCountScale - enemyFoodCountScale
        toRet += foodCountDiff

        #queen health
        myQueenHealthScale = 1 - (myQueenHealth/10)
        enemyQueenHealthScale = 1 - (enemyQueenHealth/10)
        queenHealthDiff = enemyQueenHealthScale - myQueenHealthScale

        #scaling down the diff because the numbers were unrealistic at first
        toRet += queenHealthDiff/1.5 

        #anthill capture health
        myCapHealthScale = 1 - (myAntHillHealth/3)
        enemyCapHealthScale = 1 - (enemyAntHillHealth/3)
        capHealthDiff = enemyCapHealthScale - myCapHealthScale

        #scaling down the diff because the numbers were unrealistic at first
        toRet += capHealthDiff/1.5

        return toRet


        


        

        

