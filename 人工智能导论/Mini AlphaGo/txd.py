import math
import random
import time
from copy import deepcopy
import numpy as np


class AIBoard(object):
    """
    约定：
        在棋盘上：
            1表示白棋及后手玩家
            -1表示黑棋及先手玩家
            0表示空位
        切换玩家时取反即可
        计算子数差时求和即可

    静态变量：
        Weights:    棋盘各位置的权重
        Directions: 8个方向的方向向量
    """
    Weights: np.array = np.array([[20, 2, 16, 12, 12, 16, 2, 20],
                                  [2, 1, 3, 4, 4, 3, 1, 2],
                                  [16, 3, 7, 5, 5, 7, 3, 16],
                                  [12, 4, 5, 0, 0, 5, 4, 12],
                                  [12, 4, 5, 0, 0, 5, 4, 12],
                                  [16, 3, 7, 5, 5, 7, 3, 16],
                                  [2, 1, 3, 4, 4, 3, 1, 2],
                                  [20, 2, 16, 12, 12, 16, 2, 20]])
    Directions: list = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, board: np.array) -> None:
        self.board = board.copy()

    def CountDiff(self) -> int:
        return np.sum(self.board)

    def ApplyAction(self, Action: tuple, Player: int) -> bool:
        FlippedPoses: list = self.GetFlippedPoses(Action, Player)

        if FlippedPoses == []:
            return False

        for flip in FlippedPoses:
            Row: int = flip[0]
            Col: int = flip[1]
            self.board[Row][Col] = Player
        Row, Col = Action
        self.board[Row][Col] = Player
        return True

    def IsOnBoard(self, Row: int, Col: int):
        return Row >= 0 and Row < 8 and Col >= 0 and Col < 8

    def GetFlippedPoses(self, Action: tuple, Player: int) -> list:
        x, y = Action
        if not self.IsOnBoard(x, y) or self.board[x][y] != 0:
            return []

        Oppo = -Player
        FlippedPoses = []
        for DeltaX, DeltaY in AIBoard.Directions:
            Row, Col = x + DeltaX, y + DeltaY
            Path = []
            while self.IsOnBoard(Row, Col) and self.board[Row][Col] == Oppo:
                Path.append((Row, Col))
                Row += DeltaX
                Col += DeltaY
            if self.IsOnBoard(Row, Col) and self.board[Row][Col] == Player:
                FlippedPoses.extend(Path)

        return FlippedPoses

    def GetLegalActions(self, Player: int) -> list:
        Own: int = Player
        Oppo: int = -Player
        PendingPoses: set = set()

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == Oppo:
                    for DeltaX, DeltaY in AIBoard.Directions:
                        Row: int = i + DeltaX
                        Col: int = j + DeltaY
                        if self.IsOnBoard(Row, Col) and self.board[Row][Col] == 0:
                            PendingPoses.add((Row, Col))

        return [pos for pos in PendingPoses if self.GetFlippedPoses(pos, Own)]

    def GetEmptyPoses(self) -> list:
        return [(i, j) for i in range(8) for j in range(8) if self.board[i][j] == 0]


class TreeNode:
    def __init__(self, board: AIBoard, Player: int = 1, Father=None, PrevAction=None, MaySkip=False):
        self.board: AIBoard = deepcopy(board)
        self.Player: int = Player
        self.Father: 'TreeNode' = Father
        self.PrevAction: tuple = PrevAction
        self.MaySkip: bool = MaySkip

        self.TotalVisits: int = 0
        self.TotalValue: float = 0
        self.Children: list = []
        self.PreferValue: int = self.EvalNode()

    def EvalNode(self) -> int:
        if self.Father is None or self.PrevAction is None:
            return 2
        FlippedPoses: list = self.Father.board.GetFlippedPoses(self.PrevAction, self.Father.Player)
        return sum(AIBoard.Weights[Flip[0]][Flip[1]] * 2 for Flip in FlippedPoses) + \
            AIBoard.Weights[self.PrevAction[0]][self.PrevAction[1]]

    def GetChildren(self) -> None:
        if self.IsLeaf(self.board) and self.TotalVisits != 0:
            return
        LegalActions = self.board.GetLegalActions(self.Player)
        Opponent = -self.Player
        for Action in LegalActions:
            NextStage = deepcopy(self.board)
            NextStage.ApplyAction(Action, self.Player)
            self.Children.append(TreeNode(NextStage, Player=Opponent, Father=self, PrevAction=Action))
        if not LegalActions and not self.IsLeaf(self.board):
            self.Children.append(TreeNode(self.board, Player=Opponent, Father=self, MaySkip=True))
            self.Children[-1].GetChildren()

    def IsLeaf(self, board: AIBoard) -> bool:
        return not any(board.GetLegalActions(Player) for Player in [1, -1])

    def IsFullyExpanded(self) -> bool:
        return all(Child.TotalVisits > 0 for Child in self.Children) if self.Children else False


class MCTS:

    def __init__(self, Player: int, MaxIter: int = 10 ** 10, TimeLimit: int = 5,
                 DefaultK: float = 2 ** 0.5 / 2) -> None:
        self.Player: int = 1 if Player == 'O' else -1 if Player == 'X' else Player
        self.MaxIter: int = MaxIter
        self.TimeLimit: int = TimeLimit
        self.DefaultK: float = DefaultK

        self.Root: TreeNode = None

    def UCB1(self, Node: TreeNode, K: float) -> TreeNode:
        MaxNode = None
        MaxVal = -float('inf')
        for Child in Node.Children:
            if Child.TotalVisits == 0:
                return Child
            BaseVal = Child.TotalValue / Child.TotalVisits
            EmptyCount = len(Node.board.GetEmptyPoses())
            if Child.MaySkip and EmptyCount % 2 == 0 and EmptyCount > 9:
                BaseVal += 50
            Val = BaseVal + K * math.sqrt(2 * math.log(Node.TotalVisits) / Child.TotalVisits)
            if Val > MaxVal:
                MaxVal, MaxNode = Val, Child
        return MaxNode

    def Select(self, Node: TreeNode) -> TreeNode:
        if len(Node.Children) == 0:
            return Node
        if Node.IsFullyExpanded():
            return self.Select(self.UCB1(Node, self.DefaultK))
        for Child in Node.Children:
            if Child.TotalVisits == 0:
                return Child

    def Expand(self, Node: TreeNode) -> TreeNode:
        if list(Node.board.GetLegalActions(Node.Player)) == [] or Node.Children == []:
            Node.GetChildren()
            return Node
        for Child in Node.Children:
            if Child.TotalVisits == 0:
                Child.GetChildren()
                return Child

    def Simulate(self, Node: TreeNode) -> int:
        board: AIBoard = AIBoard(Node.board.board)
        CurPlayer: int = Node.Player
        while not Node.IsLeaf(board):
            LegalActions: list = board.GetLegalActions(CurPlayer)
            EmptyCount = len(board.GetEmptyPoses())
            if len(LegalActions) != 0:
                if CurPlayer == self.Player:
                    chosen_action = random.choice(LegalActions)
                    board.ApplyAction(chosen_action, CurPlayer)
                else:
                    ActValues: list = [AIBoard.Weights[action[0]][action[1]] for action in LegalActions]
                    chosen_action = random.choices(LegalActions, weights=ActValues)[0]
                    board.ApplyAction(chosen_action, CurPlayer)
            else:
                if EmptyCount % 2 == 0 and EmptyCount > 9:
                    return 1000
            CurPlayer = -CurPlayer
        return board.CountDiff()

    def BackPropagate(self, Node: TreeNode, Value: float) -> None:
        while Node:
            Node.TotalVisits += 1
            Node.TotalValue += Value if Node.Player != self.Player else -Value
            Node = Node.Father

    def UpdateRoot(self, move):
        if self.Root and move:
            found = False
            for child in self.Root.Children:
                if child.PrevAction == move:
                    self.Root = child
                    self.Root.Father = None
                    found = True
                    break
            if not found:
                new_board = deepcopy(self.Root.board)
                new_board.ApplyAction(move, -self.Player)
                self.Root = TreeNode(new_board, Player=self.Player)

    def Run(self):
        Start = time.time()
        Cnt = 0
        while time.time() - Start < self.TimeLimit and Cnt < self.MaxIter:
            SelectedNode = self.Select(self.Root)
            if SelectedNode is None:
                break
            ExpandedNode = self.Expand(SelectedNode)
            Score = self.Simulate(ExpandedNode)
            self.BackPropagate(ExpandedNode, Score)
            Cnt += 1
        return self.UCB1(self.Root, 0).PrevAction


class AIPlayer:

    def __init__(self, color, MaxIter: int = 10 ** 10, TimeLimit: int = 59, DefaultK: float = 2):
        self.color = color
        self.Player = MCTS(self.color, MaxIter=MaxIter, TimeLimit=TimeLimit, DefaultK=DefaultK)

    def get_move(self, board):
        PlayerName: str = ''
        if self.color == 'X':
            PlayerName = '黑棋'
        else:
            PlayerName = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(PlayerName, self.color))
        BoardArray = self.GetBoardItem(board)
        if not self.Player.Root or not np.array_equal(self.Player.Root.board.board, BoardArray):
            self.Player.Root = TreeNode(AIBoard(BoardArray), Player=self.Player.Player)
            self.Player.Root.GetChildren()
        Action = self.Player.Run()
        Action = Action if Action else random.choice(self.Player.Root.board.GetLegalActions(self.Player.Player))
        self.Player.UpdateRoot(Action)
        return self.ConvertToAct(Action)

    def GetBoardItem(self, board):
        BoardItem: list = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(8):
            Part: list = board.__getitem__(i)
            for j in range(8):
                BoardItem[i][j] = 0 if Part[j] == '.' else (1 if Part[j] == 'O' else -1)
        return np.array(BoardItem)

    def ConvertToAct(self, Action: tuple) -> str:
        Letter: chr = chr(Action[1] + ord('A'))
        Number: str = str(Action[0] + 1)
        return Letter + Number