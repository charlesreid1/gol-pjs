import re

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

            rows = len(pattern)
            cols = len(pattern[0])
            listLife = []
            xoffset = xoff[ip]
            yoffset = yoff[ip]
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
            if len(url)>0:
                url += "&"
            url += f"s{ip+1}={listLife}"
    print(url)


def get_pattern(pattern_name):
    with open(pattern_name + '.txt', 'r') as f:
        pattern = f.readlines()
    pattern = [r.strip() for r in pattern]
    return pattern


if __name__=="__main__":
    #print("baseline:")
    #print_pattern_url(
    #    p1='timebomb',
    #    xoff=[40,0],
    #    yoff=[30,0],
    #)
    #print("hflip:")
    #print_pattern_url(
    #    p1='timebomb',
    #    xoff=[40,0],
    #    yoff=[30,0],
    #    hflip=[True,False]
    #)
    #print("vflip:")
    #print_pattern_url(
    #    p1='timebomb',
    #    xoff=[40,0],
    #    yoff=[30,0],
    #    vflip=[True,False]
    #)
    print("rot90:")
    print_pattern_url(
        p1='timebomb',
        xoff=[40,0],
        yoff=[30,0],
        rot=[90,0]
    )
    print("rot270:")
    print_pattern_url(
        p1='timebomb',
        xoff=[40,0],
        yoff=[30,0],
        rot=[270,0]
    )

