# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        PacPos = currentGameState.getPacmanPosition()
        curFood = currentGameState.getFood().asList()
        GhostStates = currentGameState.getGhostStates()
        ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

        ret = currentGameState.getScore()
        "*** YOUR CODE HERE ***"
        newfoodcount = len(newFood)
        foodcount = len(curFood)

        if newfoodcount < foodcount:
            ret += 10
        else:
            fooddistance = float("Inf")
            for food in curFood:
                fooddistance = min(manhattanDistance(PacPos, food), fooddistance)
            newfooddistance = float("Inf")
            for food in newFood:
                newfooddistance = min(manhattanDistance(newPos, food), newfooddistance)
            ret += 2*(fooddistance - newfooddistance)

        ghostpositions = [ghoststate.getPosition() for ghoststate in GhostStates]
        newghostpositions = [ghoststate.getPosition() for ghoststate in newGhostStates]
        newlocate_ghost = [manhattanDistance(ghost,newPos) for ghost in newghostpositions]
        locate_ghost = [manhattanDistance(ghost,PacPos) for ghost in ghostpositions]
        curghost = min(locate_ghost)
        newghost = min(newlocate_ghost)

        # curghost = min(locate_ghost)
        if newghost == 0:
            return ret - 500
        else:
            if newghost - curghost < 0:
                if newghost <= 3:
                    ret -= 20/newghost


        if newPos in newFood:
            sumfood += 1
        # ghostpositions = [ghoststate.getPosition() for ghoststate in newGhostStates]
        # locate_ghost = [-1/manhattanDistance(ghost,newPos) for ghost in ghostpositions if ghost != newPos]
        # sumghost = sum(locate_ghost)/4
        # if newPos in ghostpositions:
        #     sumghost -= 1

        return ret

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """



    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, agentIndex, depth):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)


            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth = depth - 1
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth)
            if agentIndex > 0:
                return min_value(gameState, agentIndex, depth)
        def max_value(gameState, agent, depth):
            v = float("-Inf")
            """
            v = (value, action)
            """
            maction = None
            nextAgent = (agent + 1) % gameState.getNumAgents()
            legalactions = gameState.getLegalActions(agent)
            if legalactions is not None:
                for action in gameState.getLegalActions(agent):
                    successor = gameState.generateSuccessor(agent, action)
                    successor_value = value(successor, nextAgent, depth)
                    v = max(v, successor_value[0])
                    if v == successor_value[0]:
                        maction = action

            else:
                return (self.evaluationFunction(gameState), maction)

            return (v, maction)

        def min_value(gameState, agent, depth):
            v = float("Inf")
            maction = None
            nextAgent = (agent + 1) % gameState.getNumAgents()
            legalactions = gameState.getLegalActions(agent)
            if legalactions is not None:
                for action in gameState.getLegalActions(agent):
                    successor = gameState.generateSuccessor(agent, action)
                    successor_value = value(successor, nextAgent, depth)
                    v = min(v, successor_value[0])
                    if v == successor_value[0]:
                        maction = action
            else:
                return (self.evaluationFunction(gameState), maction)

            return (v, maction)
        retur = value(gameState, 0, self.depth)
        return retur[1]
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

        "*** YOUR CODE HERE ***"
        def value(gameState, agentIndex, depth, alpha, beta):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)


            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth = depth - 1
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth, alpha, beta)
            if agentIndex > 0:
                return min_value(gameState, agentIndex, depth, alpha, beta)
        def max_value(gameState, agent, depth, alpha, beta):
            v = float("-Inf")
            """
            v = (value, action)
            """
            maction = None
            newalpha = alpha
            nextAgent = (agent + 1) % gameState.getNumAgents()
            legalactions = gameState.getLegalActions(agent)
            if legalactions is not None:
                for action in gameState.getLegalActions(agent):
                    successor = gameState.generateSuccessor(agent, action)
                    successor_value = value(successor, nextAgent, depth, newalpha, beta)
                    v = max(v, successor_value[0])
                    if v == successor_value[0]:
                        maction = action
                    if (v > beta):
                        return (v, maction)
                    newalpha = max(newalpha, v)

            else:
                return (self.evaluationFunction(gameState), maction)

            return (v, maction)

        def min_value(gameState, agent, depth, alpha, beta):
            v = float("Inf")
            maction = None
            newbeta = beta
            nextAgent = (agent + 1) % gameState.getNumAgents()
            legalactions = gameState.getLegalActions(agent)
            if legalactions is not None:
                for action in gameState.getLegalActions(agent):
                    successor = gameState.generateSuccessor(agent, action)
                    successor_value = value(successor, nextAgent, depth, alpha, newbeta)
                    v = min(v, successor_value[0])
                    if v == successor_value[0]:
                        maction = action
                    if (v < alpha):
                        return (v, maction)
                    newbeta = min(newbeta, v)
            else:
                return (self.evaluationFunction(gameState), maction)

            return (v, maction)
        retur = value(gameState, 0, self.depth, float("-Inf"), float("Inf"))
        return retur[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """



    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def value(gameState, agentIndex, depth):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)


            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                depth = depth - 1
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth)
            if agentIndex > 0:
                return exp_value(gameState, agentIndex, depth)
        def max_value(gameState, agent, depth):
            v = float("-Inf")
            """
            v = (value, action)
            """
            maction = None
            nextAgent = (agent + 1) % gameState.getNumAgents()
            legalactions = gameState.getLegalActions(agent)
            if legalactions is not None:
                for action in gameState.getLegalActions(agent):
                    successor = gameState.generateSuccessor(agent, action)
                    successor_value = value(successor, nextAgent, depth)
                    v = max(v, successor_value[0])
                    if v == successor_value[0]:
                        maction = action

            else:
                return (self.evaluationFunction(gameState), maction)

            return (v, maction)

        def exp_value(gameState, agent, depth):
            v = 0
            maction = None
            prob = get_prob(gameState, agent)
            for action in gameState.getLegalActions(agent):
                successor = gameState.generateSuccessor(agent, action)
                probability  = prob
                v += probability * value(successor, (agent + 1) % gameState.getNumAgents(), depth)[0]
                maction = action
            return (v, maction)

        def get_prob(gameState, agent):
            total = gameState.getLegalActions(agent)
            return 1.0/float(len(total))
        
        retur = value(gameState, 0, self.depth)
        return retur[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <We took into consideration the following variables: distance to nearest food, count of remaining food, 
                    average distance to nonscared ghosts, distance to scared ghost. We linearized it so that closer distance
                    to nearest food, smaller count of food, closer distance to scared ghost, would increase the return value. 
                    On the other hand, closer distance to nonscared ghost would decrease the return value.>
    """

    ret = currentGameState.getScore()
    PacPos = currentGameState.getPacmanPosition()
    FoodPos = currentGameState.getFood().asList()
    fooddistance = float("Inf")
    numghosts = currentGameState.getNumAgents()
    for food in FoodPos:
        fooddistance = min(manhattanDistance(PacPos, food), fooddistance)
    ret += 10/(fooddistance+1) + 500/(len(FoodPos)+1)

    ghostdistance = float("Inf")
    for i in range(1, numghosts):
        ghost = currentGameState.getGhostState(i)
        timer = ghost.scaredTimer
        manhat = manhattanDistance(PacPos, ghost.getPosition())
        if timer == 0:
            ghostdistance = min(ghostdistance, manhat)
            if manhat == 0:
                return - 500
            if manhat <= 2:
                ret -= (15/ghostdistance)/numghosts
        else:
            ret += 200/(manhat+1)
            # print (manhat, ret)



    return ret

    

# Abbreviation
better = betterEvaluationFunction

