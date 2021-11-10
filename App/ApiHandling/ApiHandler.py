import requests
import Common.Utils as cuts


class ApiHandler:
    def __init__(self) -> None:
        self.creds = cuts.json_contents('dev_creds.json')
        self.api_endpoint = 'https://api.smitegame.com/smiteapi.svc'
        self.response_format = 'JSON'

    def create_session(self) -> dict:
        cur_ts = cuts.make_timestamp()
        endpoint = "{api_endpoint}/{method}{response_format}/{dev_id}/{signature}/{timestamp}"
        endpoint = endpoint.format(api_endpoint=self.api_endpoint, method='createsession',
                                   response_format=self.response_format, dev_id=self.creds['devId'],
                                   signature=cuts.generate_md5(dev_id=self.creds['devId'], method_name='createsession',
                                                                auth_key=self.creds['authKey'], utc_timestamp=cur_ts),
                                   timestamp=cur_ts)
        return requests.get(endpoint).json()['session_id']

    def custom_request(self, method_name, session, custom_params) -> dict:
        cur_ts = cuts.make_timestamp()
        endpoint = "{api_endpoint}/{method}{response_format}/{dev_id}/{signature}/{session}/{timestamp}{custom_params}"
        endpoint = endpoint.format(api_endpoint=self.api_endpoint, method=method_name,
                                   response_format=self.response_format, dev_id=self.creds['devId'],
                                   signature=cuts.generate_md5(dev_id=self.creds['devId'], method_name=method_name,
                                                                auth_key=self.creds['authKey'], utc_timestamp=cur_ts),
                                   session=session, timestamp=cur_ts, custom_params=custom_params)
        response = requests.get(endpoint)
        print(endpoint)
        print(response)
        # print(response.json())
        return response.json()

    def get_player_id(self, session_id, nickname='xGoodGodx') -> str:
        player_id = self.custom_request(method_name='getplayer', session=session_id,
                                        custom_params=f'/{nickname}')[0]['ActivePlayerId']
        print(f"Player Id for {nickname} is '{player_id}'")
        return player_id

    def get_match_id(self, session_id, nickname='xGoodGodx') -> str:
        match_id = self.custom_request(method_name='getplayerstatus', session=session_id,
                                        custom_params = f'/{nickname}')[0]['Match']
        # match_id = self.custom_request(method_name='getplayerstatus', session=session_id,
                                        # custom_params = f'/{nickname}')[0]['match_queue_id']
        print(f"Match Id for {nickname} is '{match_id}'")
        return match_id

    def get_match_details(self, session_id, match_id) -> dict:
        print(f'Getting match details for {match_id}...')
        match_details = self.custom_request(method_name='getmatchplayerdetails', session=session_id, custom_params=f'/{match_id}')
        return match_details

    def get_player_batch(self, session_id, player_ids) -> dict:
        player_data = {}
        for player_id in player_ids:
            player_data.update({player_id: self.custom_request(method_name='getplayer', session=session_id, custom_params=f'/{player_id}')})
        return player_data

    def show_resources(self):
        pass #getdataused