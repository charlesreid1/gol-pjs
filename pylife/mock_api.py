class API(object):
    @classmethod
    def get_game(self, gameId):
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
          columns = 80,
          rows = 100,
          cellSize = 7
        )
        return map_api_result

    @classmethod
    def get_default_game(self):
        default_game_api_result = dict(
          id = '0000-0000-0000',
          team1Name = 'Purple',
          team1Color = '#9963AB',
          team2Name = 'Orange',
          team2Color = '#E86215'
        )
        return default_game_api_result

    @classmethod
    def get_map(self, mapId):
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


