from copy import deepcopy


class LobbyAnalyzer:
    def __init__(self, match_details: list) -> None:
        self.team1 = []
        self.team2 = []
        # we can get current god, its mastery, player names and IDs from match details
        for player_details in match_details:
            player_data_entry = {}
            player_data_entry['god'] = player_details['GodName']
            player_data_entry['god_mastery'] = player_details['Mastery_Level']
            player_data_entry['player_id'] = player_details['playerId']
            player_data_entry['player_name'] = player_details['playerName']

            if player_details['taskForce'] == 1:
                self.team1.append(deepcopy(player_data_entry))
            else:
                self.team2.append(deepcopy(player_data_entry))

    def print_lobby_stats(self) -> None:
        print("Team 1:")
        for player in self.team1:
            self._print_fullplayer_data(player_data=player)

        print("\nTeam 2:")
        for player in self.team2:
            self._print_fullplayer_data(player_data=player)

    def _print_player_data(self, player_data) -> None:
        print(f'Player "{player_data["player_name"]}"({player_data["player_id"]}) with {player_data["god"]} mastery {player_data["god_mastery"]}')

    def get_player_id_list(self) -> list:
        return [player_data['player_id'] for player_data in self.team1 + self.team2]

    def analyze_player_background(self, batch_player_info: dict):
        for player_data in self.team1 + self.team2:
            # only for player that did not hide their account
            if player_data['player_id'] != '0':
                this_player_account = batch_player_info[player_data['player_id']][0]
                # convert string minutes to hours
                player_data['playtime'] = str(round(int(this_player_account['MinutesPlayed']) / 60, 2)) + 'h'
                player_data['wins'] = this_player_account['Wins']
                player_data['losses'] = this_player_account["Losses"]
                player_data['winrate'] = LobbyAnalyzer._calc_winrate(player_data)
                player_data['account_level'] = this_player_account["Level"]
            else:
                player_data['player_name'] = '<hidden>'
                player_data['playtime'] = '0'
                player_data['wins'] = '0'
                player_data['losses'] = '0'
                player_data['winrate'] = '0'
                player_data['account_level'] = '0'

    @staticmethod
    def _print_fullplayer_data(player_data) -> None:
        info_template = "[{id:9}] {name:15} {god:12}({mastery}) | Playtime: {playtime:8} | Winrate {winrate}"
        print(info_template.format(id=player_data['player_id'], name=player_data['player_name'],
                                   god=player_data['god'], mastery=player_data['god_mastery'],
                                   playtime=player_data['playtime'], winrate=player_data['winrate']))

    @staticmethod
    def _calc_winrate(player_data) -> None:
        print(f'Wins: {player_data["wins"]}, losses: {player_data["losses"]}')
        winrate_d = int(player_data['wins']) / (1 + int(player_data['wins']) + int(player_data['losses']))
        return str(round(100*winrate_d, 2)) + '%'