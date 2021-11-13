import Common.Utils as cuts
from ApiHandling.Session import SessionManager
from ApiHandling.ApiHandler import ApiHandler
from ApiHandling.QueueIds import Queue
from LobbyAnalyzer.LobbyAnalyzer import LobbyAnalyzer


if __name__ == '__main__':
    with SessionManager() as session_inst:
        # TODO: autofetch lobby data for development
        mid = ApiHandler.get_match_id(session_inst)
        if mid == 0: # if not in lobby
            print("Loading random match data for test sake")
            mid = ApiHandler.common_request(method_name='getmatchidsbyqueue', session=session_inst,
                                                 custom_params=f'/{Queue.Conquest}/{cuts.make_date()}/19,50')[0]['Match']
        if mid != 0:
            match_details = ApiHandler.get_match_details(session_inst, mid)
            analyzer = LobbyAnalyzer(match_details)
            analyzer.analyze_player_background(ApiHandler.get_player_batch(session_inst, analyzer.get_player_id_list()))
            analyzer.print_lobby_stats()
        else:
            print("Match has not started yet!")
