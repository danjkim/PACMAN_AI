# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
	"""
		* Please read learningAgents.py before reading this.*

		A ValueIterationAgent takes a Markov decision process
		(see mdp.py) on initialization and runs value iteration
		for a given number of iterations using the supplied
		discount factor.
	"""
	def __init__(self, mdp, discount = 0.9, iterations = 100):
		"""
		  Your value iteration agent should take an mdp on
		  construction, run the indicated number of iterations
		  and then act according to the resulting policy.

		  Some useful mdp methods you will use:
			  mdp.getStates()
			  mdp.getPossibleActions(state)
			  mdp.getTransitionStatesAndProbs(state, action)
			  mdp.getReward(state, action, nextState)
			  mdp.isTerminal(state)
		"""
		self.mdp = mdp
		self.discount = discount
		self.iterations = iterations
		self.values = util.Counter() # A Counter is a dict with default 0
		for state in mdp.getStates():
			self.values[state] = 0
		self.runValueIteration()

	def runValueIteration(self):
		# Write value iteration code here
		itera = self.iterations
		while itera > 0:
			val_copy = self.values.copy()
			for state in self.mdp.getStates():
				qlist = []
				actions = self.mdp.getPossibleActions(state)

				for action in actions:
					val = self.computeQValueFromValues(state,action)
					qlist.append(val)
				if len(qlist) != 0:
					val_copy[state] = max(qlist)
				if self.mdp.isTerminal(state):
					val_copy[state] = 0
			self.values = val_copy
			# for val in val_copy:
			# 	self.values[val[1]] = val[0]
			itera = itera - 1
		"*** YOUR CODE HERE ***"



	def getValue(self, state):
		"""
		  Return the value of the state (computed in __init__).
		"""
		return self.values[state]


	def computeQValueFromValues(self, state, action):
		"""
		  Compute the Q-value of action in state from the
		  value function stored in self.values.
		"""
		"*** YOUR CODE HERE ***"
		totalQ = 0 
		transitions = self.mdp.getTransitionStatesAndProbs(state, action)
		for t in transitions:
			nextState = t[0]
			transition = t[1]
			valueFunc = self.getValue(nextState)
			totalQ += transition * (self.discount * valueFunc + self.mdp.getReward(state, action, nextState))	
		#get next states
		return totalQ


	def computeActionFromValues(self, state):
		"""
		  The policy is the best action in the given state
		  according to the values currently stored in self.values.

		  You may break ties any way you see fit.  Note that if
		  there are no legal actions, which is the case at the
		  terminal state, you should return None.
		"""
		"*** YOUR CODE HERE ***"
		dict = {}
		maxes = []
		actions = self.mdp.getPossibleActions(state)
		for action in actions:
			qVal = self.computeQValueFromValues(state, action)
			dict[qVal] = action
			maxes += [qVal]
		if len(maxes) != 0:
			return dict[max(maxes)]



	def getPolicy(self, state):
		return self.computeActionFromValues(state)

	def getAction(self, state):
		"Returns the policy at the state (no exploration)."
		return self.computeActionFromValues(state)

	def getQValue(self, state, action):
		return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
	"""
		* Please read learningAgents.py before reading this.*

		An AsynchronousValueIterationAgent takes a Markov decision process
		(see mdp.py) on initialization and runs cyclic value iteration
		for a given number of iterations using the supplied
		discount factor.
	"""
	def __init__(self, mdp, discount = 0.9, iterations = 1000):
		"""
		  Your cyclic value iteration agent should take an mdp on
		  construction, run the indicated number of iterations,
		  and then act according to the resulting policy. Each iteration
		  updates the value of only one state, which cycles through
		  the states list. If the chosen state is terminal, nothing
		  happens in that iteration.

		  Some useful mdp methods you will use:
			  mdp.getStates()
			  mdp.getPossibleActions(state)
			  mdp.getTransitionStatesAndProbs(state, action)
			  mdp.getReward(state)
			  mdp.isTerminal(state)
		"""
		ValueIterationAgent.__init__(self, mdp, discount, iterations)

	def runValueIteration(self):
		itera = self.iterations
		mdp = self.mdp
		disc = self.discount
		val_copy = self.values
		"*** YOUR CODE HERE ***"
		while itera > 0:
			# val_copy = ValueIterationAgent.values.copy()
			for state in mdp.getStates():
				# val_copy = ValueIterationAgent.values.copy()
				if itera > 0:
					qlist = []
					actions = mdp.getPossibleActions(state)

					for action in actions:
						val = self.computeQValueFromValues(state,action)
						qlist.append(val)
					if len(qlist) != 0:
						
						val_copy[state] = max(qlist)
					if mdp.isTerminal(state):
						val_copy[state] = 0
					itera -= 1


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
	"""
		* Please read learningAgents.py before reading this.*

		A PrioritizedSweepingValueIterationAgent takes a Markov decision process
		(see mdp.py) on initialization and runs prioritized sweeping value iteration
		for a given number of iterations using the supplied parameters.
	"""
	def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
		"""
		  Your prioritized sweeping value iteration agent should take an mdp on
		  construction, run the indicated number of iterations,
		  and then act according to the resulting policy.
		"""
		self.theta = theta
		ValueIterationAgent.__init__(self, mdp, discount, iterations)

	def runValueIteration(self):
		states = self.mdp.getStates()
		predecessors = {}
		for state in states:
			predecessors[state] = []
		for state in states:
			for action in self.mdp.getPossibleActions(state):
				for transition in self.mdp.getTransitionStatesAndProbs(state, action):
					if transition[1] != 0:
						predecessors[transition[0]].append(state)

		# for state in states:
		# 	predecessors[state] = []
		# 	for otherState in states:
		# 		if state != otherState:
		# 			for action in self.mdp.getPossibleActions(otherState):
		# 				transitions = self.mdp.getTransitionStatesAndProbs(otherState, action)
		# 				preds = []
		# 				for transition in transitions:
		# 					if transition[0] == state and transition[1] != 0 and otherState not in preds:
		# 						predecessors += [otherState]
		priority = util.PriorityQueue()

		for state in states:
			if len(self.mdp.getPossibleActions(state)) > 0:
				qVals = []
				for action in self.mdp.getPossibleActions(state):
					qVals += [self.computeQValueFromValues(state, action)]
				maxQ = 0
				if len(qVals) != 0:
					maxQ = max(qVals)
				diff = abs(self.values[state] - maxQ)
				priority.push(state, -1 * diff)
		for interation in range (0, self.iterations):
			if priority.isEmpty():
				break;
			poppedState = priority.pop()
			if len(self.mdp.getPossibleActions(poppedState)) != 0:
				qVals = []
				for action in self.mdp.getPossibleActions(poppedState):
					qVals += [self.computeQValueFromValues(poppedState, action)]
				maxQ = 0
				if len(qVals) != 0:
					maxQ = max(qVals)
				self.values[poppedState] = maxQ
			for predecessor in predecessors[poppedState]:
				if len(self.mdp.getPossibleActions(predecessor)) > 0:
					qVals2 = []
				for action in self.mdp.getPossibleActions(predecessor):
					qVals2 += [self.computeQValueFromValues(predecessor, action)]
				maxQ2 = 0
				if len(qVals2) != 0:
					maxQ2 = max(qVals2)
				diff = abs(self.values[predecessor] - maxQ2)
				if diff > self.theta:
					priority.update(predecessor, -1 * diff)
		"*** YOUR CODE HERE ***"

