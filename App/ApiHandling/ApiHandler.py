import requests
import Common.Utils as cuts
import Common.TimeHelper as timeh

class ApiHandler:
    creds = cuts.json_contents('dev_creds.json')
    api_endpoint = 'https://api.smitegame.com/smiteapi.svc'
    response_format = 'JSON'

    def create_session() -> dict:
        # explicitly fill session and custom params with empty strings as these values are not used for session creation
        return ApiHandler.__request_internal(method='createsession', session='', custom_params='')

    def common_request(method_name, session, custom_params) -> dict:
        return ApiHandler.__request_internal(method=method_name, session=session, custom_params=custom_params)

    def get_player_id(session_id, nickname='xGoodGodx') -> str:
        player_id = ApiHandler.common_request(method_name='getplayer', session=session_id,
                                        custom_params=f'/{nickname}')[0]['ActivePlayerId']
        print(f"Player Id for {nickname} is '{player_id}'")
        return player_id

    def get_match_id(session_id, nickname='xGoodGodx') -> str:
        match_id = ApiHandler.common_request(method_name='getplayerstatus', session=session_id,
                                        custom_params = f'/{nickname}')[0]['Match']
        print(f"Match Id for {nickname} is '{match_id}'")
        return match_id

    def get_match_details(session_id, match_id) -> dict:
        print(f'Getting match details for {match_id}...')
        match_details = ApiHandler.common_request(method_name='getmatchplayerdetails', session=session_id, custom_params=f'/{match_id}')
        return match_details

    def get_player_batch(session_id, player_ids) -> dict:
        player_data = {}
        for player_id in player_ids:
            player_data.update({player_id: ApiHandler.common_request(method_name='getplayer', session=session_id, custom_params=f'/{player_id}')})
        return player_data

    def show_resources(ApiHandler):
        pass #getdataused

    def __request_internal(method, session, custom_params):
        # prepare data to fill f-strings
        timestamp = timeh.make_timestamp()
        dev_id = ApiHandler.creds['devId']
        api_endpoint = ApiHandler.api_endpoint
        response_format = ApiHandler.response_format
        signature = cuts.generate_md5(dev_id, method, ApiHandler.creds['authKey'], timestamp)

        # fill needed pattern
        resulting_endpoint = f'{api_endpoint}/{method}{response_format}/{dev_id}/{signature}'
        # Create session is the only API method that (obviously) does not requre session id so
        #   there is a dedicated pattern for it
        if method == 'createsession':
            resulting_endpoint = f'{resulting_endpoint}/{timestamp}'
        else:
            resulting_endpoint = f'{resulting_endpoint}/{session}/{timestamp}{custom_params}'

        print(resulting_endpoint)
        response = requests.get(resulting_endpoint)
        print(response)
        return response.json()
