import random
import os
import re


def shuffle(test_list):
    # shuffle list with Fisher–Yates algorithm 
    # don't include the back element
    for i in range(len(test_list)-1, 0, -1): 
        # swap random element with back element
        j = random.randint(0, i + 1)  
        test_list[i], test_list[j] = test_list[j], test_list[i]  
    return test_list


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


def twoacorn_twocolor(rows, cols, seed=None):
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
    # set rng seed (optional)
    if seed is not None:
        random.seed(seed)

    die1 = random.randint(1,3)
    if die1 == 1:
        # zone 1
        centerx1 = cols//2 + cols//4
        centery1 = rows//4
    elif die1 == 2:
        # zone 2
        centerx1 = cols//4
        centery1 = rows//4
    else:
        # middle of zone 1 and 2
        centerx1 = cols//2
        centery1 = rows//4

    centerx1 += random.randint(-5, 5)

    die2 = random.randint(1,3)
    if die2 == 1:
        # zone 3
        centerx2 = cols//4
        centery2 = rows//2 + rows//4
    elif die2 == 2:
        # zone 4
        centerx2 = cols//2 + cols//4
        centery2 = rows//2 + rows//4
    else:
        # middle of zone 3 and 4
        centerx2 = cols//2
        centery2 = rows//2 + rows//4

    centerx2 += random.randint(-5, 5)

    pattern1 = get_grid_pattern('acorn', rows, cols, xoffset=centerx1, yoffset=centery1, vflip=True)
    pattern2 = get_grid_pattern('acorn', rows, cols, xoffset=centerx2, yoffset=centery2)

    pattern1_url = pattern2url(pattern1)
    pattern2_url = pattern2url(pattern2)

    return pattern1_url, pattern2_url


def timebomb_oscillators_twocolor(rows, cols, seed=None):
    # set rng seed (optional)
    if seed is not None:
        random.seed(seed)

    centerx1a = cols//2 + cols//4
    centerx1b = cols//4
    centery1a = rows//4
    centery1b = centery1a

    centerx1a += random.randint(-10, 10)
    centerx1b += random.randint(-10, 10)
    centery1a += random.randint(-10, 10)
    centery1b += random.randint(-10, 10)

    osc1a = get_grid_pattern('quadrupleburloaferimeter', rows, cols, xoffset=centerx1a, yoffset=centery1a)
    osc1b = get_grid_pattern('quadrupleburloaferimeter', rows, cols, xoffset=centerx1b, yoffset=centery1b)

    osc_pattern = pattern_union([osc1a, osc1b])

    centerx2 = cols//2
    centery2 = rows//2 + rows//4

    centerx2 += random.randint(-5, 5)
    centery2 += random.randint(-5, 5)

    timebomb = get_grid_pattern('timebomb', rows, cols, xoffset=centerx2, yoffset=centery2)

    pattern1_url = pattern2url(osc_pattern)
    pattern2_url = pattern2url(timebomb)

    return pattern1_url, pattern2_url


def fourrabbits_twocolor(rows, cols, seed=None):
    # set rng seed (optional)
    if seed is not None:
        random.seed(seed)

    rabbit_locations1 = [
        (cols//4, rows//4),
        (cols//2 + cols//4, rows//4),
    ]
    rabbits1 = []
    for (x,y) in rabbit_locations1:
        x += random.randint(-5,5)
        y += random.randint(-5,5)
        vflipopt = bool(random.getrandbits(1))
        hflipopt = bool(random.getrandbits(1))
        rabbit = get_grid_pattern('rabbit', rows, cols, xoffset=x, yoffset=y, vflip=vflipopt, hflip=hflipopt)
        rabbits1.append(rabbit)

    rabbit_locations2 = [
        (cols//4, rows//2 + rows//4),
        (cols//2 + cols//4, rows//2 + rows//4),
    ]
    rabbits2 = []
    for (x,y) in rabbit_locations2:
        x += random.randint(-5,5)
        y += random.randint(-5,5)
        vflipopt = bool(random.getrandbits(1))
        hflipopt = bool(random.getrandbits(1))
        rabbit = get_grid_pattern('rabbit', rows, cols, xoffset=x, yoffset=y, vflip=vflipopt, hflip=hflipopt)
        rabbits2.append(rabbit)

    rabbits_pattern1 = pattern_union(rabbits1)
    rabbits_pattern2 = pattern_union(rabbits2)

    pattern1_url = pattern2url(rabbits_pattern1)
    pattern2_url = pattern2url(rabbits_pattern2)

    return pattern1_url, pattern2_url


def twospaceshipgenerators_twocolor(rows, cols):
    # backrake 2 laying trail of glider ships
    # both backrakes start at very bottom
    # squares in middle, of alternating colors
    (xdim, ydim) = get_pattern_size('backrake2')

    spaceship1x = cols//4;
    spaceship2x = cols//2 + cols//4;
    spaceshipy = rows - 1 - ydim;

    spaceship1x += random.randint(-5,5)
    spaceship2x += random.randint(-5,5)

    generator1 = get_grid_pattern('backrake2', rows, cols, xoffset=spaceship1x, yoffset=spaceshipy, hflip=True)
    generator2 = get_grid_pattern('backrake2', rows, cols, xoffset=spaceship2x, yoffset=spaceshipy)

    nboxes = 15
    interval_height = rows//(nboxes+1)
    box_patterns1 = []
    box_patterns2 = []
    for i in range(nboxes):
        box_x = cols//2
        box_y = (i+1)*(rows//(nboxes+1))

        box_x += random.randint(-5,5)
        box_y += random.randint(-1,1)

        box_pattern = get_grid_pattern('block', rows, cols, xoffset=box_x, yoffset=box_y)
        if (i%2==0):
            box_patterns1.append(box_pattern)
        else:
            box_patterns2.append(box_pattern)

    boxship_pattern1 = pattern_union([generator1] + box_patterns1)
    boxship_pattern2 = pattern_union([generator2] + box_patterns2)

    pattern1_url = pattern2url(boxship_pattern1)
    pattern2_url = pattern2url(boxship_pattern2)

    return pattern1_url, pattern2_url


def eightr_twocolor(rows, cols):

    centerx = cols//2
    centery = rows//2

    # color 1
    r1a = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(5,10), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r1b = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(15,20), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r1c = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(25,30),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r1d = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(35,40),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    s1 = pattern_union([r1a, r1b, r1c, r1d])

    # color 2
    r2a = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(5,10), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r2b = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(15,20), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r2c = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(25,30),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    r2d = get_grid_pattern(
        'rpentomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(35,40),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    s2 = pattern_union([r2a, r2b, r2c, r2d])

    pattern1_url = pattern2url(s1)
    pattern2_url = pattern2url(s2)

    return pattern1_url, pattern2_url


def eightpi_twocolor(rows, cols):
    centerx = cols//2
    centery = rows//2

    # color 1
    p1a = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(5,10), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p1b = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(15,20), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p1c = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(25,30),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p1d = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx - random.randint(35,40),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    s1 = pattern_union([p1a, p1b, p1c, p1d])

    # color 2
    p2a = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(5,10), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p2b = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(15,20), 
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p2c = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(25,30),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    p2d = get_grid_pattern(
        'piheptomino', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(35,40),
        yoffset=centery + random.randint(-10, 10),
        hflip=bool(random.getrandbits(1)),
        vflip=bool(random.getrandbits(1)),
    )
    s2 = pattern_union([p2a, p2b, p2c, p2d])

    pattern1_url = pattern2url(s1)
    pattern2_url = pattern2url(s2)

    return pattern1_url, pattern2_url


def twomultum_twocolor(rows, cols):
    centerx = cols//2
    centery1 = rows//2
    centery2 = rows//2 #2*rows//3

    p1 = get_grid_pattern(
        'multuminparvo', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(-10,10), 
        yoffset=centery1 + random.randint(10,30),
        vflip=False
    )

    p2 = get_grid_pattern(
        'multuminparvo', 
        rows, 
        cols, 
        xoffset=centerx + random.randint(-10,10), 
        yoffset=centery2 - random.randint(10,30),
        vflip=True
    )

    pattern1_url = pattern2url(p1)
    pattern2_url = pattern2url(p2)

    return pattern1_url, pattern2_url


def hflip_pattern(pattern):
    """Flip a pattern horizontally"""
    newpattern = ["".join(reversed(j)) for j in pattern]
    return newpattern


def vflip_pattern(pattern):
    """Flip a pattern vertically"""
    newpattern = [j for j in reversed(pattern)]
    return newpattern


def rot_pattern(pattern, deg):
    """Rotate a pattern 90, 180, or 270 degrees"""
    newpattern = pattern[:]
    if deg in [90, 180, 270]:
        for i in range(deg//90):
            newpattern_tup = zip(*list(reversed(newpattern)))
            newpattern = ["".join(j) for j in newpattern_tup]
    return newpattern


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
    fname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'patterns',
        pattern_name + '.txt'
    )
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
    blank_row = ["."]*columns
    newpattern = [blank_row[:] for r in range(rows)]
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


def pattern_union(patterns):
    for i in range(1, len(patterns)):
        axis0different = len(patterns[i-1]) != len(patterns[i])
        axis1different = len(patterns[i-1][0]) != len(patterns[i][0])
        if axis0different or axis1different:
            err = "Error: cannot perform pattern_union on patterns of dissimilar size"
            err += "\n"
            for i in range(patterns):
                err += "Pattern {i+1}: rows = {len(patterns[i])}, cols = {len(patterns[i][0]}\n"
            raise Exception(err)
    
    # Turn all patterns into lists of lists (for convenience)
    rows = len(patterns[0])
    cols = len(patterns[0][0])
    newpatterns = []
    for pattern in patterns:
        newpatterns.append([list(j) for j in pattern])
    patterns = newpatterns
    blank_row = ["."]*cols
    newpattern = [blank_row[:] for r in range(rows)]
    for iy in range(rows):
        for ix in range(cols):
            alive = False
            for ip, pattern in enumerate(patterns):
                if pattern[iy][ix] == 'o':
                    alive = True
                    break
            if alive:
                newpattern[iy][ix] = 'o'

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
    #print("\n".join(get_grid_pattern('acorn', 80, 80, xoffset=10, yoffset=20)))
    a1 = get_grid_pattern('acorn', 80, 80, xoffset=10, yoffset=20)
    a2 = get_grid_pattern('acorn', 80, 80, xoffset=30, yoffset=20)
    print("\n".join(pattern_union([a1, a2])))
