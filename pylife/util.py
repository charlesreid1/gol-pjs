import random
import os
import re

def pattern2url(pattern, xoffset=0, yoffset=0):
    rows = len(pattern)
    cols = len(pattern[0])
    listLife = []
    for i in range(rows):
        listLifeRow = {}
        for j in range(cols):
            if pattern[i][j]=='o':
                y = str(i+1+yoffset)
                x = j+1+xoffset
                if y in listLifeRow.keys():
                    listLifeRow[y].append(x)
                else:
                    listLifeRow[y] = [x]
        if len(listLifeRow.keys())>0:
            listLife.append(listLifeRow)
    
    s = str(listLife)
    s = s.split(" ")
    listLife = "".join(s)
    listLife = re.sub('\'', '"', listLife)
    return listLife


def random_twocolor(rows, cols):
    """
    Generate a random two-color list life initialization.

    Returns: two listlife strings, state1 and state2,
    with the random initializations.
    (12% of all cells are alive).

    Strategy: generate a set of (x,y) tuples,
    convert to list, split in half. Use those
    point sets to create listLife URL strings.
    """
    ncells = rows*cols
    nlivecells = ncells*0.12
    points = set()
    while len(points)<nlivecells:
        randy = random.randint(0, rows-1)
        randx = random.randint(0, cols-1) 
        points.add((randx,randy))

    points = list(points)
    points1 = set(points[:len(points)//2])
    points2 = set(points[len(points)//2:])
    pattern1 = []
    pattern2 = []
    for y in range(rows):
        row1 = []
        row2 = []

        # row 1
        for x in range(cols):
            if (x,y) in points1:
                row1.append('o')
            else:
                row1.append('.')
        row1str = "".join(row1)
        pattern1.append(row1str)

        # row 2
        for x in range(cols):
            if (x,y) in points2:
                row2.append('o')
            else:
                row2.append('.')
        row2str = "".join(row2)
        pattern2.append(row2str)

    pattern1_url = pattern2url(pattern1)
    pattern2_url = pattern2url(pattern2)

    return pattern1_url, pattern2_url


def twoacorn_twocolor(rows, cols):
    """
    Generate a map wth an acorn on the top and an acorn on the bottom.

    Returns: two listlife strings, state1 and state2,
    with the acorn initializations.

    Strategy:
    - grid size doesn't matter when getting pattern
    - use grid size to determine centerpoints
    - get size of acorn pattern
    - ask for acorn at particular offset
    """
    for i in range(2):
        die = random.randint(1,3)
        if die1 == 1:
            # zone 1
            centerx = (cols//2) + (cols//4)
            centery = cols//4
        elif die == 2:
            # zone 2
            centerx = cols//4
            centery = cols//4
        else:
            # middle of zone 1 and 2
            centerx = cols//2
            centery = cols//4


def hflip_pattern(pattern):
    """Flip a pattern horizontally"""
    newpattern = [j for j in reversed(pattern)]
    return newpattern


def vflip_pattern(pattern):
    """Flip a pattern vertically"""
    newpattern = ["".join(reversed(j)) for j in pattern]
    return newpattern


def rot_pattern(pattern, deg):
    """Rotate a pattern 90, 180, or 270 degrees"""
    newpattern = pattern[:]
    if deg in [90, 180, 270]:
        for i in range(deg//90):
            newpattern_tup = zip(*list(reversed(newpattern)))
            newpattern = ["".join(j) for j in newpattern_tup]
    return newpattern


def get_pattern_size(pattern_name, **kwargs):
    """
    Returns: (nrows, ncols)
    """
    pattern = get_pattern(pattern_name, **kwargs)
    return (len(pattern), len(pattern[0]))


def get_pattern(pattern_name, hflip=False, vflip=False, rotdeg=0):
    """
    For a given pattern, return the .o diagram
    as a list of strings, one string = one row
    """
    fname = 'patterns/' + pattern_name + '.txt'
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            pattern = f.readlines()
        pattern = [r.strip() for r in pattern]
        if hflip:
            pattern = hflip_pattern(pattern)
        if vflip:
            pattern = vflip_pattern(pattern)
        if rotdeg:
            pattern = rot_pattern(pattern, rotdeg)
        return pattern
    else:
        raise Exception(f"Error: pattern {fname} does not exist!")


def get_grid_pattern(pattern_name, rows, columns, xoffset=0, yoffset=0, hflip=False, vflip=False, rotdeg=0):
    # convert list of strings to list of lists (for convenience)
    ogpattern = get_pattern(pattern_name, hflip=hflip, vflip=vflip, rotdeg=rotdeg)
    ogpattern = [list(j) for j in ogpattern]
    blank_column = ["."]*columns
    newpattern = [blank_column[:] for r in range(rows)]
    (pattern_h, pattern_w) = (len(ogpattern), len(ogpattern[0]))

    # given offset is offset for the center of the pattern,
    # so do some algebra to determine where we should start
    xstart = xoffset - pattern_w//2
    xend = xstart + pattern_w
    ystart = yoffset - pattern_h//2
    yend = ystart + pattern_h

    # iterate through the pattern and copy over the cells that are in the final grid
    for iy, y in enumerate(range(ystart, yend)):
        if y > 0 and y < len(newpattern):
            for ix, x in enumerate(range(xstart, xend)):
                if x > 0 and x < len(newpattern[iy]):
                    newpattern[y][x] = ogpattern[iy][ix]
    
    newpattern = ["".join(j) for j in newpattern]
    return newpattern


def print_pattern_url(p1=None, p2=None,
        xoff=[0, 0], 
        yoff=[0, 0], 
        hflip=[False, False],
        vflip=[False, False],
        rot=[0,0],
    ):

    url = ""
    for ip, pattern_name in enumerate([p1, p2]):
        if pattern_name != None:
            pattern = get_pattern(pattern_name)

            if hflip[ip]:
                pattern = [j for j in reversed(pattern)]

            if vflip[ip]:
                pattern = ["".join(reversed(j)) for j in pattern]

            if rot[ip] in [90, 180, 270]:
                for i in range(rot[ip]//90):
                    pattern_tup = zip(*list(reversed(pattern)))
                    pattern = ["".join(j) for j in pattern_tup]

            listLife = pattern2url(pattern)

            if len(url)>0:
                url += "&"
            url += f"s{ip+1}={listLife}"
    print(url)


if __name__=="__main__":
    print("\n".join(get_grid_pattern('acorn', 80, 80, xoffset=10, yoffset=20)))

