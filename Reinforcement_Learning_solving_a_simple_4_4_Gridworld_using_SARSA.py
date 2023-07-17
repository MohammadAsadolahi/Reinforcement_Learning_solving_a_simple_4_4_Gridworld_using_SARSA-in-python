import numpy as np
import copy
class GridWorld:
    def __init__(self):
        # S O O O
        # O O O *
        # O * O O
        # O * 0 T
        self.actionSpace = ('U', 'D', 'L', 'R')
        self.actions = {
            (0, 0): ('D', 'R'),
            (0, 1): ('L', 'D', 'R'),
            (0, 2): ('L', 'D', 'R'),
            (0, 3): ('L', 'D'),
            (1, 0): ('U', 'D', 'R'),
            (1, 1): ('U', 'L', 'D', 'R'),
            (1, 2): ('U', 'L', 'D', 'R'),
            (1, 3): ('U', 'L', 'D'),
            (2, 0): ('U', 'D', 'R'),
            (2, 1): ('U', 'L', 'D', 'R'),
            (2, 2): ('U', 'L', 'D', 'R'),
            (2, 3): ('U', 'L', 'D'),
            (3, 0): ('U', 'R'),
            (3, 1): ('U', 'L', 'R'),
            (3, 2): ('U', 'L', 'R')
            #(3,3) isn't included because its the terminal state
        }
        self.rewards = {(3, 3): 0.5, (1, 3): -0.5, (2, 1):-0.5, (3, 1):-0.5}
        
    def reset(self):
        self.state = (0, 0)
        return self.state
        
    def is_terminal(self, s):
        return s not in self.actions

    def getNewState(self,state,action):
      i, j = zip(state)
      row = int(i[0])
      column = int(j[0])
      if action == 'U':
          row -= 1
      elif action == 'D':
          row += 1
      elif action == 'L':
          column -= 1
      elif action == 'R':
          column += 1
      return row,column

    def move(self, action):
        row,column=self.getNewState(self.state,action)
        self.state=(row, column)
        if (row, column) in self.rewards:
            return (row, column),self.rewards[(row, column)],self.is_terminal(self.state)
        return (row, column),-0.01,self.is_terminal(self.state)
class Agent:
    def __init__(self,action_space, exploreRate=0.01):
        self.qTable = None
        self.action_space=action_space
        self.exploreRate= exploreRate
        self.initial_random_policy()
        self.initialQtable()
        self.explored = 0
        self.exploited = 0

    def initialQtable(self):
        self.qTable = {}
        for state in self.action_space:
            self.qTable[state]={}
            for move in self.action_space[state]:
                self.qTable[state][move]=0
        print(self.qTable)
        
    def updateQtable(self, newQ,updateRate=0.05):
        for state in self.qTable:
            for action in self.qTable[state]:
                self.qTable[state][action] = self.qTable[state][action]+(updateRate*(newQ[state][action]-self.qTable[state][action]))
    
    def chooseAction(self, state):
        if self.exploreRate > np.random.rand():
            self.explored += 1
            return np.random.choice(self.action_space[state])
        self.exploited += 1
        return self.policy[state]
    
    def initial_random_policy(self):
        self.policy = {}
        for state in self.action_space:
            self.policy[state] = np.random.choice(self.action_space[state])
            
    def learn(self,state,nextState,reward,done):
        if not done:
            targetQ= reward + (0.9 * self.qTable[nextState][self.chooseAction(nextState)])
            self.qTable[state][action]=self.qTable[state][action]+alpha*(targetQ - self.qTable[state][action])
    
    def update_policy(self):
        for state in self.policy:
            self.policy[state] = max(self.qTable[state], key=self.qTable[state].get)
def printPolicy(policy):
        line = ""
        counter = 0
        for item in policy:
            line += f" | {policy[item]} | "
            counter += 1
            if counter > 3:
                print(line)
                print("----------------------------")
                counter = 0
                line = ""
        print(line)
        print("----------------------------")
env=GridWorld()
agent = Agent(env.actions)

# policy = {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D'
#     ,(2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R'}
# env.printPolicy(policy)

alpha=0.1
for i in range(2000):
    state = env.reset()
    stepCounts=0
    done=False
    while not done and (stepCounts<20):
        action=agent.chooseAction(state)
        nextState, reward, done = env.move(action)
        stepCounts += 1
        targetQ=reward
        agent.learn(state,nextState, reward, done )
        state = nextState
    agent.update_policy()
    if i%200==0:
        print(f"\n\n\n step:{i}")
        printPolicy(agent.policy)
        print("\n")
print(f"exploited:{agent.exploited}  explored:{agent.explored}")
