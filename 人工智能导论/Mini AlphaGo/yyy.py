# 导入棋盘文件
from board import Board

# 初始化棋盘
board = Board()

# 打印初始化棋盘
board.display()

# 导入随机包
import random

import copy
import math
import random


class AIPlayer:
    def __init__(self, color):
        self.color = color

    class Node:
        def __init__(self, board_state, color, parent=None, action=None):
            self.color = color
            self.visit_times = 0
            self.reward = 0.0
            self.board_state = board_state
            self.parent = parent
            self.children = []
            self.action = action
            self.wins = 0

        def is_all_expand(self):
            all_actions = list(self.board_state.get_legal_actions(self.color))
            return len(all_actions) == len(self.children)

    def is_terminal(self, board_state):
        # 这里简化了原始的检查方式，具体实现可能需要调整
        return not list(board_state.get_legal_actions('X')) and not list(board_state.get_legal_actions('O'))

    def expansion(self, node):
        untried_actions = [action for action in list(node.board_state.get_legal_actions(node.color)) if
                           action not in [child.action for child in node.children]]
        if not untried_actions:
            return node.parent
        action = random.choice(untried_actions)
        new_state = copy.deepcopy(node.board_state)
        new_state._move(action, node.color)
        new_color = 'O' if node.color == 'X' else 'X'
        child_node = self.Node(new_state, new_color, parent=node, action=action)
        node.children.append(child_node)
        return child_node

    def selection(self, node):
        while not self.is_terminal(node.board_state):
            if not node.is_all_expand():
                return self.expansion(node)
            else:
                node = self.best_child(node)
        return node

    def selection(self, node):
        while not self.is_terminal(node.board_state):
            if not node.is_all_expand():
                return self.expansion(node)
            elif node.children:  # 确保有子节点
                node = self.best_child(node)
            else:
                # 处理没有子节点的情况
                break  # 或者是其他逻辑
        return node

    def best_child(self, node, c_param=1.4):
        if not node.children:
            # 没有子节点的情况下的处理逻辑
            return None  # 或者根据你的逻辑返回其他值
        choices_weights = [
            (child.wins / child.visit_times) + c_param * math.sqrt((2 * math.log(node.visit_times) / child.visit_times))
            for child in node.children
        ]
        return node.children[choices_weights.index(max(choices_weights))]

    def best_child(self, node, c_param=1.4):
        choices_weights = [
            (child.wins / child.visit_times) + c_param * math.sqrt((2 * math.log(node.visit_times) / child.visit_times))
            for child in node.children]
        return node.children[choices_weights.index(max(choices_weights))]

    def simulation(self, node):
        temp_board = copy.deepcopy(node.board_state)
        temp_color = node.color
        while not self.is_terminal(temp_board):
            possible_moves = list(temp_board.get_legal_actions(temp_color))
            if not possible_moves:
                temp_color = 'O' if temp_color == 'X' else 'X'
                continue
            action = random.choice(possible_moves)
            temp_board._move(action, temp_color)
            temp_color = 'O' if temp_color == 'X' else 'X'
        return temp_board.count('X'), temp_board.count('O')

    def back_propagation(self, node, winner):
        while node is not None:
            node.visit_times += 1
            if self.color == winner:
                node.wins += 1
            node = node.parent

    def get_move(self, board):
        root = self.Node(board_state=copy.deepcopy(board), color=self.color)
        for _ in range(1000):  # 增加迭代次数以提高准确性
            node = self.selection(root)
            winner = self.simulation(node)
            self.back_propagation(node, winner)
        return self.best_child(root, 0).action

    # 其他方法...