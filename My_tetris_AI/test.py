gridHeight = 5
gridWidth = 5
grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0]
]

filledRowCount = 0

for x in range(gridHeight):  # Iterate over rows (height)
    currcellcount = 0
    for y in range(gridWidth):  # Iterate over columns (width)
        if grid[x][y] == 1:
            currcellcount += 1
    if currcellcount == gridWidth:
        filledRowCount += 1

print("Filled_rows:", filledRowCount)

        