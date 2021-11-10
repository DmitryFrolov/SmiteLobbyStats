import Common.Utils as cuts
from ApiHandling.Session import Session
from ApiHandling.ApiHandler import ApiHandler
from ApiHandling.QueueIds import Queue
from LobbyAnalyzer.LobbyAnalyzer import LobbyAnalyzer


if __name__ == '__main__':
    session_id = Session()
    # TODO: autofetch lobby data for development
    # mid = ApiHandler.custom_request(method_name='getmatchidsbyqueue', session=session_id,
                            #  custom_params=f'/{Queue.Conquest}/{cuts.make_date()}/18,30')[0]['Match']
    mid = ApiHandler.get_match_id(session_id)
    if mid != 0:
        match_details = ApiHandler.get_match_details(session_id, mid)
        analyzer = LobbyAnalyzer(match_details)
        analyzer.analyze_player_background(ApiHandler.get_player_batch(session_id, analyzer.get_player_id_list()))
        analyzer.print_lobby_stats()
    else:
        print("Match has not started yet!")
