from operator import indexOf
import json

class API(object):
    @classmethod
    def get_game(self):
        default_game_api_result = dict(
          id = '0000-0000-0000',
          team1Name = 'Purple',
          team1Color = '#9963AB',
          team2Name = 'Orange',
          team2Color = '#E86215',
          map = self.get_default_map(),
        )
        return default_game_api_result

    @classmethod
    def get_default_game(self):
        default_game_api_result = dict(
          id = '0000-0000-0000',
          team1Name = 'Purple',
          team1Color = '#9963AB',
          team2Name = 'Orange',
          team2Color = '#E86215',
          map = self.get_default_map(),
        )
        return default_game_api_result

    @classmethod
    def get_default_map(self):
        map_api_result = dict(
          id = 1,
          mapName = 'Default Map',
          mapZone1Name = 'Zone 1',
          mapZone2Name = 'Zone 2',
          mapZone3Name = 'Zone 3',
          mapZone4Name = 'Zone 4',
          initialConditions1 = '[{"39":[60]},{"40":[62]},{"41":[59,60,63,64,65]}]',
          initialConditions2 = '[{"21":[29,30,33,34,35]},{"22":[32]},{"23":[30]}]',
          columns = 120,
          rows = 100,
          cellSize = 7
        )
        return map_api_result

class GOL(object):
    team_names = []
    generation = 0
    columns = 0
    rows = 0
    livecells = 0
    livecells1 = 0
    livecells2 = 0
    victory = 0.0
    coverage = 0.0
    territory1 = 0.0
    territory2 = 0.0
    actual_state = []
    actual_state1 = []
    actual_state2 = []

    def __init__(self, **kwargs):
        """Constructor just sets everything up"""
        self.load_config(**kwargs)
        self.load_state()

    def __repr__(self):
        s = []
        s.append("+" + "-"*(self.columns) + "+")
        for i in range(self.rows):
            row = "|"
            for j in range(self.columns):
                if self.is_alive(j, i):
                    color = self.get_cell_color(j, i)
                    if color == 1:
                        row += "#"
                    elif color == 2:
                        row += "o"
                    else:
                        row += "?"
                else:
                    row += "."
            row += "|"
            s.append(row)
        s.append("+" + "-"*(self.columns) + "+")
        rep = "\n".join(s)
        rep += "\n"

        livecounts = gol.get_live_counts()

        rep += "\nGeneration: %d"%(self.generation)
        rep += "\nLive cells, color 1: %d"%(livecounts[1])
        rep += "\nLive cells, color 2: %d"%(livecounts[2])
        rep += "\nLive cells, total: %d"%(livecounts[0])
        rep += "\nVictory Percent: %0.1f %%"%(livecounts[3])
        rep += "\nCoverage: %0.2f %%"%(livecounts[4])
        rep += "\nTerritory, color 1: %0.2f %%"%(livecounts[5])
        rep += "\nTerritory, color 2: %0.2f %%"%(livecounts[6])

        return rep

    def load_config(self, **kwargs):
        """Load configuration from user-provided input params"""
        if gameId in kwargs:
            self.game_api_result = API.get_game(kwargs['gameId'])
            self.game_map = self.game_api_result['map']
        elif mapId in kwargs:
            self.game_api_result = API.get_default_game()
            self.game_map = API.get_map(kwargs['mapId'])

        # Extract team info
        self.team_names = [self.game_api_result['team1Name'], self.game_api_result['team2Name']]

        # Extract map info
        self.ic1 = self.game_map['initialConditions1']
        self.ic2 = self.game_map['initialConditions2']
        self.columns = self.game_map['columns']
        self.rows = self.game_map['rows']

    def load_state(self):
        """
        Load the listlife state from the initial conditions.
        Initial conditions are set in the load_config() function
        and are specified as part of the map.
        """
        s1 = json.loads(self.ic1)
        s2 = json.loads(self.ic2)

        for s1row in s1:
            for y in s1row.keys():
                yy = int(y)
                for xx in s1row[y]:
                    self.actual_state = self.add_cell(xx, yy, self.actual_state)
                    self.actual_state1 = self.add_cell(xx, yy, self.actual_state1)

        for s2row in s2:
            for y in s2row.keys():
                yy = int(y)
                for xx in s2row[y]:
                    self.actual_state = self.add_cell(xx, yy, self.actual_state)
                    self.actual_state2 = self.add_cell(xx, yy, self.actual_state2)
        
    def is_alive(self, x, y):
        """
        Boolean function: is the cell at x, y alive
        """
        for row in self.actual_state:
            if (row[0] == y):
                for c in row[1:]:
                    if c==x:
                        return True

        return False

    def get_cell_color(self, x, y):
        """
        Get the color of the given cell (1 or 2, 0 for dead)
        """
        for row in self.actual_state1:
            if (row[0] == y):
                for c in row[1:]:
                    if c==x:
                        return 1
            elif (row[0] > y):
                break

        for row in self.actual_state2:
            if (row[0] == y):
                for c in row[1:]:
                    if c==x:
                        return 2
            elif (row[0] > y):
                break

        return 0

    def remove_cell(self, x, y, state):
        """
        Remove the given cell from the given listlife state
        """
        for i, row in enumerate(state):
            if row[0]==y:
                if len(row)==2:
                    # Remove the entire row
                    state = state[:i] + state[i+1:]
                    return
                else:
                    j = indexOf(row, x)
                    state[i] = row[:j] + row[j+1:]


    def add_cell(self, x, y, state):
        """
        State is a list of arrays, where the y-coordinate is the first element,
        and the rest of the elements are x-coordinates:
          [y1, x1, x2, x3, x4]
          [y2, x5, x6, x7, x8, x9]
          [y3, x10]
        """
        # Empty state case
        if len(state)==0:
            state.append([y, x])
            return state

        # figure out where in the list to insert the new cell
        if (y < state[0][0]):
            # y is smaller than any existing y,
            # so put this point at beginning
            new_state = [[y, x]]
            for row in state:
                new_state.append(row)
            return new_state

        elif (y > state[-1][0]):
            # y is larger than any existing y,
            # so put this point at end
            state.append([y,x])
            return state

        else:
            # Adding to the middle
            new_state = []
            added = False
            for row in state:
                if (not added) and (row[0]==y):
                    # This level exists
                    new_row = [y]
                    for c in row[1:]:
                        if (not added) and (x < c):
                            new_row.append(x)
                            added = True
                        new_row.append(c)
                    if not added:
                        new_row.append(x)
                        added = True
                    new_state.append(new_row)
                elif (not added) and (y < row[0]):
                    # State does not include this row,
                    # so create a new row
                    new_row = [y,x]
                    new_state.append(new_row)
                    added = True
                    # Also append the existing row
                    new_state.append(row)
                else:
                    new_state.append(row)

            if added==False:
                raise Exception(f"Error adding cell ({xx},{yy}): new_state = {new_state}")

            return new_state

    def get_neighbors_from_alive(self, x, y, i, state, possible_neighbors_list):
        neighbors = 0
        neighbors1 = 0
        neighbors2 = 0

        # 1 row above current cell
        if i >= 1:
            if state[i-1][0] == (y-1):
                for k in range(self.top_pointer, len(state[i-1])):
                    if state[i-1][k] >= (x-1):

                        # NW
                        if state[i-1][k] == (x-1):
                            possible_neighbors_list[0] = None
                            self.top_pointer = k + 1
                            neighbors += 1
                            xx = state[i-1][k]
                            yy = state[i-1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # N
                        if state[i-1][k] == x:
                            possible_neighbors_list[1] = None
                            self.top_pointer = k
                            neighbors += 1
                            xx = state[i-1][k]
                            yy = state[i-1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # NE
                        if state[i-1][k] == (x+1):
                            possible_neighbors_list[2] = None
                            if k==1:
                                self.top_pointer = 1
                            else:
                                self.top_pointer = k - 1
                            neighbors += 1
                            xx = state[i-1][k]
                            yy = state[i-1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # Break it off early
                        if state[i-1][k] > (x+1):
                            break

        # The row of the current cell
        for k in range(1,len(state[i])):
            if (state[i][k] >= (x-1)):

                # W
                if (state[i][k] == (x-1)):
                    possible_neighbors_list[3] = None
                    neighbors += 1
                    xx = state[i][k]
                    yy = state[i][0]
                    neighborcolor = self.get_cell_color(xx, yy)
                    if neighborcolor == 1:
                        neighbors1 += 1
                    elif neighborcolor == 2:
                        neighbors2 += 1
                    else:
                        print("?????")

                # E
                if (state[i][k] == (x+1)):
                    possible_neighbors_list[4] = None
                    neighbors += 1
                    xx = state[i][k]
                    yy = state[i][0]
                    neighborcolor = self.get_cell_color(xx, yy)
                    if neighborcolor == 1:
                        neighbors1 += 1
                    elif neighborcolor == 2:
                        neighbors2 += 1
                    else:
                        print("?????")

                # Break it off early
                if (state[i][k] > (x+1)):
                    break

        # 1 row below current cell
        if i+1 < len(state):
            if state[i+1][0] == (y+1):
                for k in range(self.bottom_pointer, len(state[i+1])):
                    if (state[i+1][k] >= (x-1)):

                        # SW
                        if (state[i+1][k] == (x-1)):
                            possible_neighbors_list[5] = None
                            self.bottom_pointer = k + 1
                            neighbors += 1
                            xx = state[i+1][k]
                            yy = state[i+1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # S
                        if (state[i+1][k] == x):
                            possible_neighbors_list[6] = None
                            self.bottom_pointer = k
                            neighbors += 1
                            xx = state[i+1][k]
                            yy = state[i+1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # SE
                        if (state[i+1][k] == (x+1)):
                            possible_neighbors_list[7] = None
                            if k==1:
                                self.bottom_pinter = 1
                            else:
                                self.bottom_pointer = k-1
                            neighbors += 1
                            xx = state[i+1][k]
                            yy = state[i+1][0]
                            neighborcolor = self.get_cell_color(xx, yy)
                            if neighborcolor == 1:
                                neighbors1 += 1
                            elif neighborcolor == 2:
                                neighbors2 += 1
                            else:
                                print("?????")

                        # Break it off early
                        if state[i+1][k] > (x+1):
                            break

        color = 0
        if neighbors1 >= neighbors2:
            color = 1
        else:
            color = 2

        return dict(neighbors = neighbors, color = color)

    def get_color_from_alive(self, x, y):
        """
        This function seems redundant, but is slightly different.
        The above function is for dead cells that become alive.
        This function is for dead cells that come alive because of THOSE cells.
        """
        state1 = self.actual_state1
        state2 = self.actual_state2

        color1 = 0
        color2 = 0

        # color1
        for i in range(len(state1)):
            yy = state1[i][0]
            if yy == (y-1):
                # 1 row above current cell
                for j in range(1,len(state1[i])):
                    xx = state1[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # NW
                            color1 += 1
                        elif xx == x:
                            # N
                            color1 += 1
                        elif xx == (x+1):
                            # NE
                            color1 += 1
                    if xx >= (x+1):
                        break

            elif yy == y:
                # Row of current cell
                for j in range(1,len(state1[i])):
                    xx = state1[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # W
                            color1 += 1
                        elif xx == (x+1):
                            # E
                            color1 += 1
                    if xx >= (x+1):
                        break

            elif yy == (y+1):
                # 1 row below current cell
                for j in range(1,len(state1[i])):
                    xx = state1[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # SW
                            color1 += 1
                        elif xx == x:
                            # S
                            color1 += 1
                        elif xx == (x+1):
                            # SE
                            color1 += 1
                    if xx >= (x+1):
                        break

        # color2
        for i in range(len(state2)):
            yy = state2[i][0]
            if yy == (y-1):
                # 1 row above current cell
                for j in range(1,len(state2[i])):
                    xx = state2[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # NW
                            color2 += 1
                        elif xx == x:
                            # N
                            color2 += 1
                        elif xx == (x+1):
                            # NE
                            color2 += 1
                    if xx >= (x+1):
                        break

            elif yy == y:
                # Row of current cell
                for j in range(1,len(state2[i])):
                    xx = state2[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # W
                            color2 += 1
                        elif xx == (x+1):
                            # E
                            color2 += 1
                    if xx >= (x+1):
                        break

            elif yy == (y+1):
                # 1 row below current cell
                for j in range(1,len(state2[i])):
                    xx = state2[i][j]
                    if xx >= (x-1):
                        if xx == (x-1):
                            # SW
                            color2 += 1
                        elif xx == x:
                            # S
                            color2 += 1
                        elif xx == (x+1):
                            # SE
                            color2 += 1
                    if xx >= (x+1):
                        break

        if color1 > color2:
            return 1
        elif color1 < color2:
            return 2
        else:
            return 0

    def next_generation(self):
        """
        Evolve the actual_state list life state to the next generation.
        """
        all_dead_neighbors = {}
        all_dead_neighbors1 = {}
        all_dead_neighbors2 = {}

        new_state = []
        new_state1 = []
        new_state2 = []

        self.redraw_list = []

        for i in range(len(self.actual_state)):
            self.top_pointer = 1
            self.bottom_pointer = 1

            for j in range(1, len(self.actual_state[i])):
                x = self.actual_state[i][j]
                y = self.actual_state[i][0]

                # create a list of possible dead neighbors
                # get_neighbors_from_alive() will pare this down
                dead_neighbors = [
                    [x-1, y-1, 1],
                    [x,   y-1, 1],
                    [x+1, y-1, 1],
                    [x-1, y,   1],
                    [x+1, y,   1],
                    [x-1, y+1, 1],
                    [x,   y+1, 1],
                    [x+1, y+1, 1]
                ]

                result = self.get_neighbors_from_alive(x, y, i, self.actual_state, dead_neighbors)
                neighbors = result['neighbors'];
                color = result['color']

                # join dead neighbors remaining to check list
                for dead_neighbor in dead_neighbors:
                    if dead_neighbor != None:
                        # this cell is dead
                        xx = dead_neighbor[0]
                        yy = dead_neighbor[1]
                        key = str(xx) + ',' + str(yy)

                        # counting number of dead neighbors
                        if key not in all_dead_neighbors.keys():
                            all_dead_neighbors[key] = 1
                        else:
                            all_dead_neighbors[key] += 1

                if not (neighbors==0 or neighbors==1 or neighbors>3):
                    new_state = self.add_cell(x, y, new_state)
                    if color==1:
                        new_state1 = self.add_cell(x, y, new_state1)
                    elif color==2:
                        new_state2 = self.add_cell(x, y, new_state2)
                    # Keep cell alive
                    self.redraw_list.append([x, y, 2])
                else:
                    # Kill cell
                    self.redraw_list.append([x, y, 0])

        # Process dead neighbors
        for key in all_dead_neighbors.keys():
            if all_dead_neighbors[key] == 3:
                # This cell is dead, but has enough neighbors
                # that are alive that it will make new life
                key = key.split(',')
                t1 = int(key[0])
                t2 = int(key[1])

                # Get color from neighboring parent cells
                color = self.get_color_from_alive(t1, t2)

                new_state = self.add_cell(t1, t2, new_state)
                if color==1:
                    new_state1 = self.add_cell(t1, t2, new_state1)
                elif color==2:
                    new_state2 = self.add_cell(t1, t2, new_state2)

                self.redraw_list.append([t1, t2, 1])

        self.actual_state = new_state
        self.actual_state1 = new_state1
        self.actual_state2 = new_state2

        return self.get_live_counts()

    def get_live_counts(self):
        """
        Get live counts of cells of each color, and total.
        Compute statistics.
        """

        def count_live_cells(state):
            livecells = 0
            for i in range(len(state)):
                if (state[i][0] >= 0) and (state[i][0] < self.rows):
                    for j in range(1, len(state[i])):
                        if (state[i][j] >= 0) and (state[i][j] < self.columns):
                            livecells += 1
            return livecells

        livecells  = count_live_cells(self.actual_state)
        livecells1 = count_live_cells(self.actual_state1)
        livecells2 = count_live_cells(self.actual_state2)

        self.livecells  = livecells
        self.livecells1 = livecells1
        self.livecells2 = livecells2

        victory = 0.0
        if livecells1 > livecells2:
            victory = livecells1/(1.0*livecells1 + livecells2)
        else:
            victory = livecells2/(1.0*livecells1 + livecells2)
        victory = victory * 100
        self.victory = victory

        total_area = self.columns * self.rows
        coverage = livecells/(1.0*total_area)
        coverage = coverage * 100
        self.coverage = coverage

        territory1 = livecells1/(1.0*total_area)
        territory1 = territory1 * 100
        territory2 = livecells2/(1.0*total_area)
        territory2 = territory2 * 100
        self.territory1 = territory1
        self.territory2 = territory2

        return [
          livecells,
          livecells1,
          livecells2,
          victory,
          coverage,
          territory1,
          territory2
        ]

    def next_step(self):
        live_counts = self.next_generation()
        self.generation += 1


if __name__=="__main__":
    gol = GOL(gameId='5')
    print(gol)
    for i in range(500):
        gol.next_step()
    print(gol)
