# AI_player.py
import copy
import math
import random
from board import Board


class MCT_node:
    def __init__(self, state, parent=None, action=None, color=''):

        self.color = color
        self.parent = parent
        self.state = state
        self.value = 0.00
        self.visit_num = 0
        self.action = action
        self.children = []

    def add(self, child_state, action, color):

        child = MCT_node(child_state, self, action, color)
        self.children.append(child)

    def full_expand(self):

        action = self.state.get_legal_actions(self.color)
        return len(self.children) == len(list(action))

class AIPlayer:


    def __init__(self, color):

        self.color = color
        self.max_try_time = 50
        self.scalar = 1
        self.select_probability = 0.3
        self.max_stimulate_times = 500

    def calu_ucb(self, node, scalar = 1):

        max_value = -float('inf')
        best_child = []
        for child in node.children:
            if child.visit_num == 0:
                best_child = [child]
                break
            value = child.value / child.visit_num + scalar * math.sqrt(
                2.0 * math.log(node.visit_num) / float(child.visit_num))
            if value > max_value:
                best_child = [child]
                max_value = value
            elif value == max_value:
                best_child.append(child)
        if len(best_child) == 0:
            return node.parent
        return random.choice(best_child)


    def select(self, node):
        '''
        选择以便于扩展的节点，选择策略为UCB策略
        '''
        while any(node.state.get_legal_actions(player) for player in ['X', '0']):
            if len(node.children) == 0:
                return self.expand(node)
            elif random.uniform(0, 1) < self.select_probability:
                node = self.calu_ucb(node)
            else:
                node = self.calu_ucb(node)
                if not node.full_expand():
                    return self.expand(node)
                else:
                    node = self.calu_ucb(node)
        return node

    def expand(self, node):
        '''
        扩展节点
        '''
        actions = list(node.state.get_legal_actions(node.color))
        if len(actions) == 0:
            return node.parent

        tried_action = [child.action
                        for child
                        in node.children]
        not_tried_action = [a
                            for a
                            in actions
                            if not a in tried_action]
        action = random.choice(not_tried_action)

        new_state = copy.deepcopy(node.state)
        new_state._move(action, node.color)
        node.add(new_state, action, color = '0' if node.color == 'X' else 'X')
        return node.children[-1]


    def simulate(self, node):
        state = copy.deepcopy(node.state)
        color = node.color
        count = 0

        while any(node.state.get_legal_actions(player) for player in ['X', '0']) and count < self.max_stimulate_times:
            actions = list(state.get_legal_actions(color))
            if not len(actions) == 0:
                action = random.choice(actions)
                state._move(action, color)
            count = count + 1
            color = 'X' if color == 'O' else 'O'

        winner, delta = state.get_winner()
        if winner == 0 and self.color == 'X':
            return 100 + delta
        elif winner == 0 and self.color == '0':
            return 0
        if winner == 1 and self.color == '0':
            return 100 + delta
        elif winner == 1 and self.color == 'X':
            return 0
        else:
            return -(100 + delta)



    def backpropagation(self, node, reward):

        while node is not None:
            node.visit_num = node.visit_num + 1
            node.value = node.value + reward
            node = node.parent
        return

    def choose_best_child(self, node):

        for i in range(self.max_try_time):
            leaf = self.select(node)
            reward = self.simulate(leaf)
            self.backpropagation(leaf, reward)
            best_child = self.calu_ucb(node, 0)
        return best_child.action

    def get_move(self, board):

        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        now_state = copy.deepcopy(board)
        node = MCT_node(now_state, color = self.color)
        return self.choose_best_child(node)
