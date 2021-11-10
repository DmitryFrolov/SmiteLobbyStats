import time
import sys

from ApiHandling.ApiHandler import ApiHandler
import Common.Utils as cuts


class Session:
    SESSION_LIFETIME_LIMIT = 15*60 # 15minutes is a session lifetime limited by HiRez API
    SESSION_CACHE_LOCATION = 'tmp/cache_session_data.json'

    def __init__(self):
        self.load_cached_session()

        if not self.is_session_valid():
            # create a new session
            self.refresh_session()
            # and cache it
            self.cache_session()

    def __str__(self) -> str:
        return self.session_id

    def is_session_valid(self) -> bool:
        """Checks if the session could be considered as valid, handles scenarios when session was or was not loaded
            from cache

        Session is considered valid only if we successfully loaded it and its lifetime is still valid

        Returns:
            bool: Whether or not session could be considered as a valid one
        """
        print("Validating session...")
        session_valid = False
        # self.session_creation_time will be created in case session was loaded successfully from cache
        if hasattr(self, "session_creation_time"):
            # {current time} - {session create time} < {SESSION_LIFETIME_LIMIT}
            session_valid = time.time() - self.session_creation_time < Session.SESSION_LIFETIME_LIMIT
        print(f"Session is {'not ' if not session_valid else ''}valid.")
        return session_valid

    def load_cached_session(self) -> None:
        try:
            self.__dict__ = cuts.json_contents(Session.SESSION_CACHE_LOCATION)
            print(f"Data was successfully loaded from cache: {self.__dict__}")
        except:
            print("No cached session found.")

    def cache_session(self) -> None:
        print(f"Session cached to {Session.SESSION_CACHE_LOCATION} as {self.__dict__}")
        cuts.dump_to_json(Session.SESSION_CACHE_LOCATION, self.__dict__)

    def refresh_session(self) -> None:
        self.session_creation_time = time.time()
        self.session_id = ApiHandler.create_session()['session_id']
