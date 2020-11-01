from util import random_twocolor
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
          columns = 80,
          rows = 100,
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
        """
        #map_api_result = dict(
        #  id = 1,
        #  mapName = 'Default Map',
        #  mapZone1Name = 'Zone 1',
        #  mapZone2Name = 'Zone 2',
        #  mapZone3Name = 'Zone 3',
        #  mapZone4Name = 'Zone 4',
        #  initialConditions1 = ic1,
        #  initialConditions2 = ic2,
        #  columns = 80,
        #  rows = 100,
        #  cellSize = 7
        #)
        if mapId == 1:
            # random pattern
            rows = 120
            cols = 100
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
            pass

