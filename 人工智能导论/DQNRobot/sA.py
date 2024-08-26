# 导入相关包
import os
import random
import numpy as np
from Maze import Maze
from Runner import Runner
from QRobot import QRobot
from ReplayDataSet import ReplayDataSet
from torch_py.MinDQNRobot import MinDQNRobot as TorchRobot  # PyTorch版本
from keras_py.MinDQNRobot import MinDQNRobot as KerasRobot  # Keras版本
import matplotlib.pyplot as plt
import heapq  # 引入堆队列

# 机器人移动方向
move_map = {
    'u': (-1, 0),  # up
    'r': (0, +1),  # right
    'd': (+1, 0),  # down
    'l': (0, -1),  # left
}


# 计算曼哈顿距离的函数
def manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


# 迷宫路径搜索树
class SearchTree(object):
    def __init__(self, loc=(), action='', parent=None, g_cost=0, h_cost=0):
        self.loc = loc  # 当前节点位置
        self.to_this_action = action  # 到达当前节点的动作
        self.parent = parent  # 当前节点的父节点
        self.children = []  # 当前节点的子节点
        self.g_cost = g_cost  # 从起点到当前节点的实际成本
        self.h_cost = h_cost  # 当前节点到目标节点的估算成本
        self.f_cost = g_cost + h_cost  # 综合成本

    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def __lt__(self, other):
        return self.f_cost < other.f_cost


def expand(maze, node, goal):
    can_move = maze.can_move_actions(node.loc)
    children = []
    for a in can_move:
        new_loc = tuple(node.loc[i] + move_map[a][i] for i in range(2))
        g_cost = node.g_cost + 1
        h_cost = manhattan_distance(new_loc, goal)
        child = SearchTree(loc=new_loc, action=a, parent=node, g_cost=g_cost, h_cost=h_cost)
        children.append(child)
    return children


def back_propagation(node):
    path = []
    while node.parent is not None:
        path.insert(0, node.to_this_action)
        node = node.parent
    return path


def a_star_search(maze):
    start = maze.sense_robot()
    goal = maze.destination
    root = SearchTree(loc=start, g_cost=0, h_cost=manhattan_distance(start, goal))
    open_set = []
    heapq.heappush(open_set, root)
    closed_set = set()
    closed_set.add(start)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.loc == goal:
            return back_propagation(current_node)

        children = expand(maze, current_node, goal)
        for child in children:
            if child.loc in closed_set:
                continue
            heapq.heappush(open_set, child)
            closed_set.add(child.loc)

    return []


def my_search(maze):
    """
    使用最佳优先搜索（A*）算法实现路径搜索
    :param maze: 迷宫对象
    :return :到达目标点的路径 如：["u","u","r",...]
    """
    path = a_star_search(maze)
    return path


maze = Maze(maze_size=10)  # 从文件生成迷宫
path_2 = my_search(maze)
print("搜索出的路径：", path_2)
for action in path_2:
    maze.move_robot(action)
if maze.sense_robot() == maze.destination:
    print("恭喜你，到达了目标点")

# 其他代码保持不变
from ReplayDataSet import ReplayDataSet

test_memory = ReplayDataSet(max_size=1e3)  # 初始化并设定最大容量
actions = ['u', 'r', 'd', 'l']
test_memory.add((0, 1), actions.index("r"), -10, (0, 1), 1)  # 添加一条数据（state, action_index, reward, next_state）
print(test_memory.random_sample(1))  # 从中随机抽取一条（因为只有一条数据）

from torch_py.MinDQNRobot import MinDQNRobot as TorchRobot  # PyTorch版本
from keras_py.MinDQNRobot import MinDQNRobot as KerasRobot  # Keras版本

import matplotlib.pyplot as plt
from Maze import Maze
from Runner import Runner
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 允许重复载入lib文件

maze = Maze(maze_size=5)

# 选择keras版本或者torch版本的机器人, MinRobot是尽量选择reward值最小的动作，对象初始化过程中修改了maze的reward参数
# robot = KerasRobot(maze=maze)
robot = TorchRobot(maze=maze)

print(robot.maze.reward)  # 输出最小值选择策略的reward值

# 开启金手指，获取全图视野
robot.memory.build_full_view(maze=maze)

# training by runner
runner = Runner(robot=robot)
runner.run_training(training_epoch=10, training_per_epoch=75)

# Test Robot
robot.reset()
for _ in range(25):
    a, r = robot.test_update()
    print("action:", a, "reward:", r)
    if r == maze.reward["destination"]:
        print("success")
        break

# QLearning机器人类实现
import random
from QRobot import QRobot


class Robot(QRobot):
    valid_action = ['u', 'r', 'd', 'l']

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon=0.5):
        self.maze = maze
        self.state = None
        self.action = None
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon  # 动作随机选择概率
        self.q_table = {}

        self.maze.reset_robot()  # 重置机器人状态
        self.state = self.maze.sense_robot()  # state为机器人当前状态

        if self.state not in self.q_table:  # 如果当前状态不存在，则为 Q 表添加新列
            self.q_table[self.state] = {a: 0.0 for a in self.valid_action}

    def train_update(self):
        self.state = self.maze.sense_robot()  # 获取机器人当初所处迷宫位置

        if self.state not in self.q_table:
            self.q_table[self.state] = {a: 0.0 for a in self.valid_action}

        action = random.choice(self.valid_action) if random.random() < self.epsilon else max(self.q_table[self.state],
                                                                                             key=self.q_table[
                                                                                                 self.state].get)  # action为机器人选择的动作
        reward = self.maze.move_robot(action)  # 以给定的方向移动机器人,reward为迷宫返回的奖励值
        next_state = self.maze.sense_robot()  # 获取机器人执行指令后所处的位置

        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.valid_action}

        current_r = self.q_table[self.state][action]
        update_r = reward + self.gamma * float(max(self.q_table[next_state].values()))
        self.q_table[self.state][action] = self.alpha * (self.q_table[self.state][action]) + (1 - self.alpha) * (
                    update_r - current_r)

        self.epsilon *= 0.99  # 衰减随机选择动作的可能性

        return action, reward

    def test_update(self):
        self.state = self.maze.sense_robot()  # 获取机器人现在所处迷宫位置

        if self.state not in self.q_table:
            self.q_table[self.state] = {a: 0.0 for a in self.valid_action}

        action = max(self.q_table[self.state], key=self.q_table[self.state].get)  # 选择动作
        reward = self.maze.move_robot(action)  # 以给定的方向移动机器人

        return action, reward
