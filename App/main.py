import Common.TimeHelper as timeh

from ApiHandling.Session import SessionManager
from ApiHandling.ApiHandler import ApiHandler
from ApiHandling.QueueIds import Queue
from LobbyAnalyzer.LobbyAnalyzer import LobbyAnalyzer


def get_ongoing_mid() -> str:
    print("Loading random match data for test sake")
    matches = ApiHandler.common_request(method_name='getmatchidsbyqueue', session=session_inst,
                                    custom_params=f'/{Queue.Conquest}/{timeh.make_date()}/{timeh.get_hour()}')
    # retrun mid for first found ongoing match
    for match in matches:
        is_ongoing = match["Active_Flag"] == "y"
        if is_ongoing:
            return match["Match"]
    raise RuntimeError("No ongoing matches found")


if __name__ == '__main__':
    with SessionManager() as session_inst:
        mid = ApiHandler.get_match_id(session_inst)
        if mid == 0: # if not in lobby
            mid = get_ongoing_mid()
        if mid != 0:
            match_details = ApiHandler.get_match_details(session_inst, mid)
            analyzer = LobbyAnalyzer(match_details)
            analyzer.analyze_player_background(ApiHandler.get_player_batch(session_inst, analyzer.get_player_id_list()))
            analyzer.print_lobby_stats()
        else:
            print("Match has not started yet!")
