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
MXMXAXMASX
"""

data = open("p4.input.txt").read()

matrix = [list(line.strip()) for line in data.splitlines()]

tot = 0
# i = row
for i in range(1, len(matrix) - 1):
    # j = column
    for j in range(1, len(matrix[i]) - 1):
        if matrix[i][j] != "A":
            continue
        sm = [
            matrix[i - 1][j - 1],  # up left
            matrix[i - 1][j + 1],  # up right
            matrix[i + 1][j - 1],  # down left
            matrix[i + 1][j + 1],  # down right
        ]
        if sm in [
            ["M", "S", "M", "S"],
            ["S", "S", "M", "M"],
            ["S", "M", "S", "M"],
            ["M", "M", "S", "S"],
        ]:
            tot += 1


print(tot)
