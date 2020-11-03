from util import (
    random_twocolor, 
    twoacorn_twocolor,
    timebomb_oscillators_twocolor,
    fourrabbits_twocolor,
    twospaceshipgenerators_twocolor,
    eightr_twocolor,
    eightpi_twocolor,
)
import random

class API(object):
    @classmethod
    def get_game(cls, gameId):
        default_game_api_result = dict(
          id = '0000-0000-0000',
          team1Name = 'Purple',
          team1Color = '#9963AB',
          team2Name = 'Orange',
          team2Color = '#E86215',
          map = cls.get_default_map(),
        )
        return default_game_api_result
    
    @classmethod
    def get_default_map(cls):
        map_api_result = dict(
          id = 1,
          mapName = 'Default Map',
          mapZone1Name = 'Zone 1',
          mapZone2Name = 'Zone 2',
          mapZone3Name = 'Zone 3',
          mapZone4Name = 'Zone 4',
          initialConditions1 = '[{"39":[60]},{"40":[62]},{"41":[59,60,63,64,65]}]',
          initialConditions2 = '[{"21":[29,30,33,34,35]},{"22":[32]},{"23":[30]}]',
          columns = 10,
          rows = 10,
          cellSize = 7
        )
        return map_api_result

    @classmethod
    def get_default_game(cls):
        default_game_api_result = dict(
          id = '0000-0000-0000',
          team1Name = 'Purple',
          team1Color = '#9963AB',
          team2Name = 'Orange',
          team2Color = '#E86215'
        )
        return default_game_api_result

    @classmethod
    def get_map(cls, mapId):
        """
        Get a map by ID

        Example API result:
        dict(
          id = 1,
          mapName = 'Default Map',
          mapZone1Name = 'Zone 1',
          mapZone2Name = 'Zone 2',
          mapZone3Name = 'Zone 3',
          mapZone4Name = 'Zone 4',
          initialConditions1 = ic1,
          initialConditions2 = ic2,
          columns = 80,
          rows = 100,
          cellSize = 7
        )
        """
        cols = 120
        rows = 100
        if mapId == 1:
            # random pattern
            s1, s2 = random_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 1,
                mapName = "East Hellmouth",
                mapZone1Name = "Containment Zone 1",
                mapZone2Name = "Containment Zone 2",
                mapZone3Name = "Containment Zone 3",
                mapZone4Name = "Containment Zone 4",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 2:
            # two-acorn pattern
            s1, s2 = twoacorn_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 2,
                mapName = "The Quad",
                mapZone1Name = "Quadrant I",
                mapZone2Name = "Quadrant II",
                mapZone3Name = "Quadrant III",
                mapZone4Name = "Quadrant IV",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 3:
            # time bomb and oscillators
            s1, s2 = timebomb_oscillators_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 3,
                mapName = "HCC Superfund Site",
                mapZone1Name = "Hot Rock Piles",
                mapZone2Name = "Colorful Ponds",
                mapZone3Name = "Slag Heap",
                mapZone4Name = "Bottomless Hole",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 4:
            # rabbit in each quadrant
            s1, s2 = fourrabbits_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 4,
                mapName = "Food Court",
                mapZone1Name = "Sandwich Zone",
                mapZone2Name = "Beans Zone",
                mapZone3Name = "Freezer Zone",
                mapZone4Name = "Kitchen Zone",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 5:
            # two spaceship generators
            # backrake 2 laying a trail of glider ships
            # squares in the middle of alternating colors
            s1, s2 = twospaceshipgenerators_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 5,
                mapName = "Spacetime Complex",
                mapZone1Name = "spacetime",
                mapZone2Name = "spaceyo",
                mapZone3Name = "froyo",
                mapZone4Name = "frotime",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 6:
            # eight r pentominoes
            s1, s2 = eightr_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 6,
                mapName = "Site 500",
                mapZone1Name = "Gammatron Accelerator",
                mapZone2Name = "Radiobaric Chamber",
                mapZone3Name = "Cryogenics Facility",
                mapZone4Name = "Mysterious Landing Pad",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

        elif mapId == 7:
            # eight pi pentominoes
            s1, s2 = eightpi_twocolor(rows, cols)
            url = f"?s1={s1}&s2={s2}"
            result = dict(
                id = 6,
                mapName = "Site 500",
                mapZone1Name = "Gammatron Accelerator",
                mapZone2Name = "Radiobaric Chamber",
                mapZone3Name = "Cryogenics Facility",
                mapZone4Name = "Mysterious Landing Pad",
                initialConditions1 = s1,
                initialConditions2 = s2,
                url = url,
                rows = rows,
                columns = cols,
                cellSize = 7
            )
            return result

