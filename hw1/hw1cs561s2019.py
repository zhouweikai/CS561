import sys

EMPTY = "0"
KEVIN = "1"
OPPONENT = "2"
BLOCK = "3"
BOTH = "4"
# DIRS = [[-1, 0], [-2, 0], [-3, 0], [1, 0], [2, 0], [3, 0],
#         [0, 1], [0, 2], [0, 3], [0, -1], [0, -2], [0, -3],
#         [-1, 1], [-2, 2], [-3, 3], [1, -1], [2, -2], [3, -3],
#         [1, 1], [2, 2], [3, 3], [-1, -1], [-2, -2], [-3, -3]]
UP = [[0, 1], [0, 2], [0, 3]]
DOWN = [[0, -1], [0, -2], [0, -3]]
LEFT = [[-1, 0], [-2, 0], [-3, 0]]
RIGHT = [[1, 0], [2, 0], [3, 0]]
LEFT_UP = [[-1, 1], [-2, 2], [-3, 3]]
RIGHT_UP = [[1, 1], [2, 2], [3, 3]]
LEFT_DOWN = [[-1, -1], [-2, -2], [-3, -3]]
RIGHT_DOWN = [[1, -1], [2, -2], [3, -3]]


def data_to_matrix(row_len, lines):
    # print(rows_list)
    matrix = [None] * row_len
    for i in range(row_len):
        matrix[i] = [0] * row_len
    for i in range(row_len):
        line = lines[i + 1].strip('\n')
        for j in range(row_len):
            matrix[i][j] = int(line[j])
    # print(matrix)
    return matrix


# def sweep(matrix):
#     swept_board = []
#     for i in range(3):
#
#     print(swept_board)
#     return swept_board


def process_matrix(matrix):
    ones = []
    twos = []
    covered = [None] * len(matrix)
    for i in range(len(matrix)):
        covered[i] = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == int(KEVIN):
                ones.append([i, j])
            elif matrix[i][j] == int(OPPONENT):
                twos.append([i, j])
            elif matrix[i][j] == int(BLOCK):
                covered[i][j] = int(BLOCK)
    # print(ones)
    # print(twos)
    for point in ones:
        covered = cover(covered, matrix, point, KEVIN)
    for point in twos:
        covered = cover(covered, matrix, point, OPPONENT)
    # print(covered)
    # print('---------------')
    return covered


def cover(covered, matrix, point, player):
    x = point[0]
    y = point[1]
    covered[x][y] = int(player)
    all_dir = [UP, DOWN, LEFT, RIGHT, LEFT_UP, RIGHT_UP, LEFT_DOWN, RIGHT_DOWN]
    for dirc in all_dir:
        one_dir(x, y, matrix, covered, player, dirc)
    return covered


def one_dir(x, y, matrix, covered, player, dirc):
    for i in range(len(dirc)):
        newX = x + dirc[i][0]
        newY = y + dirc[i][1]
        if newX < 0 or newX >= len(matrix) or newY < 0 or newY >= len(matrix):
            continue
        if matrix[newX][newY] == int(BLOCK):
            break
        if covered[newX][newY] == 3 - int(player):
            covered[newX][newY] = int(BOTH)
            continue
        covered[newX][newY] = int(player)


def count_zero(covered):
    candi = []
    for i in range(len(covered)):
        for j in range(len(covered)):
            if covered[i][j] == 0:
                candi.append([i, j])
    return candi


def get_score(covered):
    count = 0
    for i in range(len(covered)):
        for j in range(len(covered)):
            if covered[i][j] == int(KEVIN) or covered[i][j] == int(BOTH):
                count += 1
    return count


# def minimax(matrix, depth, isMax, alpha, beta):
#     covered = process_matrix(matrix)
#     candi = count_zero(covered)
#     if len(candi) == 0:
#         return [-1, -1, score(covered)]
#     if isMax:
#         bestVal = [-1, -1, -sys.maxint]
#         for point in candi:
#             matrix[point[0]][point[1]] = int(KEVIN)
#             value = minimax(matrix, depth + 1, False, alpha, beta)
#             matrix[point[0]][point[1]] = int(EMPTY)
#             value[0], value[1] = point[0], point[1]
#             if value[2] > bestVal[2]:
#                 bestVal = value
#             # bestVal = max(bestVal, value[2])
#             # alpha = max(alpha, bestVal[2])
#             if bestVal[2] > alpha[2]:
#                 alpha = bestVal
#             if beta[2] <= alpha[2]:
#                 break
#         return bestVal
#     else:
#         bestVal = [-1, -1, sys.maxint]
#         for point in candi:
#             matrix[point[0]][point[1]] = int(OPPONENT)
#             value = minimax(matrix, depth + 1, True, alpha, beta)
#             matrix[point[0]][point[1]] = int(EMPTY)
#             value[0], value[1] = point[0], point[1]
#             if value[2] < bestVal[2]:
#                 bestVal = value
#             # bestVal = min(bestVal, value)
#             # beta = min(beta, bestVal[2])
#             if bestVal[2] < beta[2]:
#                 beta = bestVal
#             if beta[2] <= alpha[2]:
#                 break
#         return bestVal


def minimax(matrix, depth, player):
    covered = process_matrix(matrix)
    candi = count_zero(covered)
    if player == KEVIN:
        if depth == 0 or len(candi) == 0:
            return [-1, -1, get_score(covered)]
        result = [-1, -1, -sys.maxint]
        for point in candi:
            x = point[0]
            y = point[1]
            matrix[x][y] = int(player)
            score = minimax(matrix, depth - 1, OPPONENT)
            matrix[x][y] = int(EMPTY)
            score[0] = x
            score[1] = y
            if score[2] > result[2]:
                result = score
    else:
        if depth == 0 or len(candi) == 0:
            return [-1, -1, get_score(covered)]
        result = [-1, -1, -sys.maxint]
        for point in candi:
            x = point[0]
            y = point[1]
            matrix[x][y] = int(player)
            score = minimax(matrix, depth - 1, OPPONENT)
            matrix[x][y] = int(EMPTY)
            score[0] = x
            score[1] = y
            if score[2] > result[2]:
                result = score
    return result


if __name__ == "__main__":
    f = open('input.txt', 'r')
    # print(data)
    lines = []
    for line in f.readlines():
        lines.append(line)
    row_len = int(lines[0])
    # print(row_len)
    matrix = data_to_matrix(row_len, lines)
    # print(matrix)
    result = minimax(matrix, 3, KEVIN)
    target = [result[0], result[1]]
    output = open("output.txt", "w")
    output.write(str(target[0]) + " " + str(target[1]))
    output.close()
