from queue import Queue
import numpy as np

initial_board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]
testS_P = [[1, 1, 0, 0, 1, -1, 0, 0], [1, 1, 0, 0, -1, 1, 0, 0], [1, 1, 0, 0, 1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0],
           [1, 1, 0, 0, -1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0],
           [1, 1, 0, 0, -1, -1, 0, 0]]

testS = [[1, 1, 0, 0, 1, -1, -1, 0], [1, 1, 0, 0, -1, 1, 0, 0], [1, 1, 0, 0, 1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0],
         [1, 1, 0, 0, -1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0], [1, 1, 0, 0, -1, -1, 0, 0],
         [1, 1, 0, 0, -1, -1, 0, 0]]


# paramS：二维列表
def reverseS(paramS):
    return (np.array(paramS)*-1).tolist()


Search_M = initial_board
tmp_S = initial_board


# 棋局的裁判函数
def judge(paramSp, paramS, a):
    global tmp_S  # 修改中的棋局
    global Search_M
    pass_flag = 0
    paramSp = reverseS(paramSp)
    if paramSp == paramS:
        pass_flag = 1
    # 判断是否结束
    if a == 64 and pass_flag:
        Search_M = paramS
        score = count()
        return score, None
    if a == 64:
        return -2, paramS
    x, y = int(a / 8), a % 8
    if paramS[x][y] != 0:
        return -1, None
    tmp_S = paramS
    tmp_S[x][y] = 1
    # 提子
    for d in direct:
        tx, ty = l[0] + d[0], l[1] + d[1]
        if tx < 0 or ty < 0 or tx > 7 or ty > 7:
            continue;
        if tmp_S[tx][ty] == -1:
            group = slice_group(tmp_S, tx, ty)
            if judge_liberty(tmp_S, group) == 0:
                for l in group:
                    tx, ty = l[0], l[1]
                    tmp_S[tx][ty] = 0

    group = slice_group(tmp_S, x, y)
    if judge_liberty(tmp_S, group) == 0 or tmp_S == paramSp:
        return -1, None
    return -2, tmp_S


direct = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # 上下左右


# 分块函数
def slice_group(board, x, y):
    visit = initial_board
    color = board[x][y]
    q = Queue()
    record = [[x, y]]
    visit[x][y] = 1
    q.put([x, y])
    while not q.empty():
        here = q.get()
        for d in direct:
            tx, ty = here[0] + d[0], here[1] + d[1]
            if tx < 0 or ty < 0 or tx > 7 or ty > 7 or visit[tx][ty] != 0 or board[tx][ty] != color:
                continue
            visit[tx][ty] = 1
            q.put([tx, ty])
            record.append([tx, ty])
    return record


# 判断死活函数
def judge_liberty(board, group):
    for l in group:
        for d in direct:
            tx, ty = l[0] + d[0], l[1] + d[1]
            if tx < 0 or ty < 0 or tx > 7 or ty > 7:
                continue
            if board[tx][ty] == 0:
                return 1
    return 0


# 判断胜负函数
def count():
    global Search_M
    score = 0
    for i in range(8):
        for j in range(8):
            if Search_M[i][j] == 1 or Search_M[i][j] == -1:
                score += Search_M[i][j]
            if Search_M[i][j] == 0:
                tmp_score = search(i, j)
                if tmp_score != 2:
                    score += tmp_score
    if score > 0:
        return 1
    if score < 0:
        return -1
    else:
        return 0


def judge_color(board, group):
    flag1, flag2 = 0, 0
    for l in group:
        for d in direct:
            tx, ty = l[0] + d[0], l[1] + d[1]
            if tx < 0 or ty < 0 or tx > 7 or ty > 7:
                continue
            if board[tx][ty] == 1:
                flag1 = 1
            if board[tx][ty] == -1:
                flag2 = -1
    return flag1 + flag2


# 判断每个位置归属
def search(x, y):
    group = slice_group(Search_M, x, y)
    color = judge_color(Search_M, group)
    for l in group:
        if color == 1:
            Search_M[l[0]][l[1]] = 1
        if color == -1:
            Search_M[l[0]][l[1]] = -1
        if color == 0:
            Search_M[l[0]][l[1]] = -2
    if color != 0:
        return color
    else:
        return -2


"""
def search(x, y):
    global Search_M
    if Search_M[x][y] != 0:
        return Search_M[x][y]
    r1, r2, r3, r4, flag1, flag2, flag3 = 0, 0, 0, 0, 0, 0, 0
    if x > 0:
        r1 = search(x - 1, y)
        if r1 == -1:
            flag1 = 1
        if r1 == 1:
            flag2 = 1
        if r1 == 2:
            flag3 = 1
    if x < 7:
        r2 = search(x + 1, y)
        if r2 == -1:
            flag1 = 1
        if r2 == 1:
            flag2 = 1
        if r2 == 2:
            flag3 = 1
    if y > 0:
        r3 = search(x, y - 1)
        if r3 == -1:
            flag1 = 1
        if r3 == 1:
            flag2 = 1
        if r3 == 2:
            flag3 = 1
    if y < 7:
        r4 = search(x, y + 1)
        if r4 == -1:
            flag1 = 1
        if r4 == 1:
            flag2 = 1
        if r4 == 2:
            flag3 = 1
    if flag3:
        Search_M[x][y] = 2
        return 2
    if flag1 and not flag2:
        Search_M[x][y] = -1
        return -1
    if flag2 and not flag1:
        Search_M[x][y] = 1
        return 1
    else:
        Search_M[x][y] = 2
        return
    """

# print(judge(testS, testS, 64))


