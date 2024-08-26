# 导入随机包
import copy
import math
import random
import copy
from board import Board
#棋局阶段的适应性权重，开局阶段可能更重视控制中心区域，而终局阶段可能更重视角落和边缘的稳定性。
def get_game_phase_weights(board):
    # 开局阶段权重矩阵
    early_game_weights = [
        [90, -10, 15, 10, 10, 15, -10, 90],
        [-10, -30, 5, 2, 2, 5, -30, -10],
        [10, -2, 2, 1, 1, 2, -2, 10],
        [5, -2, 1, 2, 2, 1, -2, 5],
        [5, -2, 1, 2, 2, 1, -2, 5],
        [10, -2, 2, 1, 1, 2, -2, 10],
        [-10, -30, 5, 2, 2, 5, -30, -10],
        [90, -10, 15, 10, 10, 15, -10, 90]
    ]

    # 中盘阶段权重矩阵,在游戏的中盘，尤其是边缘棋子（非角落），可能因为易于被对方翻转而变得不那么有价值。
    mid_game_weights = [
        [110, -20, 20, 15, 15, 20, -20, 110],
        [-20, -40, 10, 5, 5, 10, -40, -20],
        [20, 0, 5, 2, 2, 5, 0, 20],
        [10, 0, 2, 5, 5, 2, 0, 10],
        [10, 0, 2, 5, 5, 2, 0, 10],
        [20, 0, 5, 2, 2, 5, 0, 20],
        [-20, -40, 10, 5, 5, 10, -40, -20],
        [110, -20, 20, 15, 15, 20, -20, 110]
    ]

    # 终局阶段权重矩阵
    end_game_weights = [
        [130, -10, 25, 20, 20, 25, -10, 130],
        [-10, -20, 10, 5, 5, 10, -20, -10],
        [15, -1, 5, 2, 2, 5, -1, 15],
        [10, -1, 2, 2, 2, 2, -1, 10],
        [10, -1, 2, 2, 2, 2, -1, 10],
        [15, -1, 5, 2, 2, 5, -1, 15],
        [-10, -20, 10, 5, 5, 10, -20, -10],
        [130, -10, 25, 20, 20, 25, -10, 130]
    ]
    empty_count = sum(row.count('.') for row in board)  # 计算空位数量
    if empty_count > 48:
        return early_game_weights
    elif empty_count > 16:
        return mid_game_weights
    else:
        return end_game_weights

#稳定的棋子是不能被对方翻转的棋子。稳定性的计算可以从四个角开始，逐步向外扩展。
def is_stable(x, y, board, color):
    if board[x][y] != color:
        return False
    # 方向向量定义所有可能的移动方向
    directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    stable = True
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # 检查每个方向
        while 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == color:
                nx += dx
                ny += dy
            else:
                # 如果在任何方向上找到非同色棋子或边界，则检查该方向相反方向是否也是非同色或边界
                if board[nx][ny] != color:
                    back_x, back_y = x - dx, y - dy
                    while 0 <= back_x < 8 and 0 <= back_y < 8:
                        if board[back_x][back_y] != color:
                            stable = False
                            break
                        back_x -= dx
                        back_y -= dy
                break
        if not stable:
            break
    return stable

def calculate_stability(board, color):
    stable_count = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == color and is_stable(r, c, board, color):
                stable_count += 1
    return stable_count

#行动力是指对手可行的走步数量。减少对手行动力的核心是限制对方下一步的合法位置。
def opponent_mobility(board, color):
    opponent_color = 'O' if color == 'X' else 'X'
    # 正确地使用 board 实例调用 get_legal_actions 方法
    return len(list(board.get_legal_actions(opponent_color)))

#将上述因素综合到评估函数中：
def evaluate_board(board, color):
    weights = get_game_phase_weights(board)
    score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == color:
                score += weights[r][c]
                if is_stable(r, c, board, color):
                    score += 20  # 稳定棋子增加额外分数
            elif board[r][c] != '.':
                score -= weights[r][c]
    # 增加稳定性评分
    score += calculate_stability(board, color) * 20
    # 减少对方的行动力
    score -= opponent_mobility(board, color)
    return score
class Node:# Node 类：代表搜索树中的节点
    def __init__(self,state,color,parent = None,action = None):
        # 初始化节点访问次数，黑白棋胜利次数，节点奖励，棋盘状态，子节点列表，父节点，节点动作，行动方颜色
        self.visit = 0
        self.blackwin = 0
        self.whitewin = 0
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent
        self.action = action
        self.color = color

    def add_child(self,new_state,action,color):
        #添加子节点
        child_node = Node(new_state,parent=self,action = action,color=color)
        self.children.append(child_node)

    def if_fully_expanded(self):
        # 检查是否所有合法动作都已扩展为子节点
        cnt_max = len(list(self.state.get_legal_actions(self.color)))
        cnt_now = len(self.children)
        if(cnt_max <= cnt_now):
            return True
        else:
            return False

class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color

# 判断游戏结束
    def if_terminal(self,state):
        # to see a state is terminal or not
        action_black = list(state.get_legal_actions('X'))
        action_white = list(state.get_legal_actions('O'))
        if(len(action_white) == 0 and len(action_black) == 0):
            return True
        else:
            return False

    # 后向传播，从给定节点向上回溯至根节点，更新路径上每个节点的访问次数和胜利次数。
    def back_propagate(self,node,blackw,whitew):
        while(node is not None):
            node.visit+=1
            node.blackwin+=blackw
            node.whitewin+=whitew
            node = node.parent
        return 0

    # 颜色反转，辅助方法，用于更换当前玩家的颜色。
    def reverse_color(self,color):
        if(color == 'X'):
            return 'O'
        else:
            return 'X'

    # 模拟策略，从给定节点开始，随机模拟直到游戏结束，返回模拟结束时的分数（黑棋和白棋的棋子数）。
    def stimulate_policy(self, node):
        board = copy.deepcopy(node.state)  # 获取当前棋盘状态的深拷贝
        color = copy.deepcopy(node.color)  # 当前落子颜色
        cnt = 0
        while not self.if_terminal(board):
            actions = list(board.get_legal_actions(color))
            if not actions:
                color = self.reverse_color(color)  # 没有合法动作时切换颜色
            else:
                action = random.choice(actions)
                board._move(action, color)  # 执行落子动作
                color = self.reverse_color(color)  # 切换颜色
            cnt += 1
            if cnt > 20:
                break

        # 正确计算并返回黑棋和白棋的数量
        black_count = board.count('X')
        white_count = board.count('O')
        return black_count, white_count

    # UCB计算，使用UCB公式选择具有最大期望奖励的子节点。
    def ucb(self,node,uct_scalar=0.0):
        max = -float('inf')
        max_set=[]
        for c in node.children:
            exploit = 0
            if c.color == 'O':
                exploit = c.blackwin/(c.blackwin+c.whitewin)
            else:
                exploit = c.whitewin/(c.blackwin+c.whitewin)
            explore = math.sqrt(2.0*math.log(node.visit)/float(c.visit))
            uct_score = exploit+uct_scalar*explore
            if(uct_score==max):
                max_set.append(c)
            elif(uct_score>max):
                max_set=[c]
                max = uct_score
        if(len(max_set)==0):
            print("max_set is empty")
            print(len(node.children))
            node.state.display()
            return node.parent
        else:
            return random.choice(max_set)

    # 扩展节点，当节点未完全扩展时，随机选择一个未探索的动作创建新的子节点。
    def expand(self,node):
        actions_available = list(node.state.get_legal_actions(node.color))
        actions_already = [c.action for c in node.children]
        if(len(actions_available)==0):
            return node.parent
        action = random.choice(actions_available)
        while action in actions_already:
            action=random.choice(actions_available)
        new_state = copy.deepcopy(node.state)
        new_state._move(action,node.color)
        new_state.display()
        new_color = self.reverse_color(node.color)
        node.add_child(new_state,action = action,color= new_color)
        return node.children[-1]

    # 选择策略，选择过程，从根节点开始，根据是否已完全扩展和UCB值选择或扩展节点。
    def select_policy(self,node):
        while(not self.if_terminal(node.state)):
            if(len(list(node.state.get_legal_actions(node.color)))==0):
                return node;
            elif(not node.if_fully_expanded()):
                print("need to expand")
                new_node = self.expand(node)
                print("end of expand")
                return new_node
            else:
                print("fully expaned")
                node.state.display()
                print(len(node.children))
                print(list(node.state.get_legal_actions(node.color)))
                node = self.ucb(node)
        return node

    # 蒙特卡洛树搜索，实现MCTS搜索，返回最佳动作。
    def MCTS_search(self,root,maxt = 200):
        for t in range(maxt):
            leave = self.select_policy(root)
            blackwin,whitewin = self.stimulate_policy(leave)
            self.back_propagate(leave,blackw=blackwin,whitew=whitewin)
        return self.ucb(root).action

    # 获取最佳动作，AI玩家根据当前棋盘状态计算并返回最佳落子位置。
    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        action = None
        root_board = copy.deepcopy(board)
        root = Node(state=root_board,color=self.color)
        action = self.MCTS_search(root)

        # ------------------------------------------------------------------------

        return action

