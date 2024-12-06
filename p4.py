import re

data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

matrix = [list(line) for line in data.splitlines()]

matrix = [list(line.strip()) for line in open("p4.input.txt").readlines()]

tot = 0


def count_in_rows(matrix):
    tot = 0
    for line in matrix:
        if len(line) < 4:
            continue
        line = str.join("", line)
        prevtot = tot
        tot += line.count("XMAS")
        tot += line.count("SAMX")
        if prevtot < tot:
            print(f'{line} {line.count("XMAS")} {line.count("SAMX")}')
    return tot


def transpose(matrix):
    t = []
    for i in range(len(matrix[0])):
        t.append([matrix[j][i] for j in range(len(matrix))])
    return t


def diagonals(matrix):
    diagonals = []
    # horizontal diagonals
    for i in range(len(matrix[0])):
        x = [matrix[j][i + j] for j in range(len(matrix[0]) - i)]
        diagonals.append(x)
    # vertical diagonals
    for i in range(1, len(matrix)):
        diagonals.append([matrix[i + j][j] for j in range(len(matrix) - i)])

    return diagonals


def printMatrix(matrix):
    print(str.join("\n", [str.join("", line) for line in matrix]))


## Count rows
tot += count_in_rows(matrix)

## Count columns
tot += count_in_rows(transpose(matrix))

## Count diagonals
tot += count_in_rows(diagonals(matrix))

tot += count_in_rows(diagonals([list(reversed(line)) for line in matrix]))

print(tot)

