#!/usr/bin/python3
"""Define island perimeter function."""

def island_perimeter(grid):
    """Return the perimeter of an island.
    The grid represents water by 0 and land by 1.
    
    Args:
        grid (list): List of list of integers representing an island.
    
    Returns:
        int: The perimeter of the island in grid.
    """
    height = len(grid)
    width = len(grid[0])
    perimeter = 0

    for i in range(height):
        for j in range(width):
            if grid[i][j] == 1:
                # Each land cell starts with 4 sides
                perimeter += 4

                # Check above cell
                if i > 0 and grid[i - 1][j] == 1:
                    perimeter -= 2

                # Check left cell
                if j > 0 and grid[i][j - 1] == 1:
                    perimeter -= 2

    return perimeter

if __name__ == "__main__":
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    print(island_perimeter(grid))
