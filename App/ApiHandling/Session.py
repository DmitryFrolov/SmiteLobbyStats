import time
import threading
import sys

from ApiHandling.ApiHandler import ApiHandler
import Common.Utils as cuts


class Session:
    """
    Container-class for session
    """
    LIFETIME_LIMIT = 15*60 # 15minutes is a session lifetime limited by HiRez API
    CACHE_LOCATION = 'tmp/cache_session_data.json'
    def __init__(self):
        self.id = None
        self.creation_time = None

    def update_with_sid(self, sid):
        self.id = sid
        self.creation_time = time.time()

class SessionManager:
    """
    Class resposible for keeping the session fresh and juicy
    """
    def __init__(self):
        self._session = Session()
        # blocks __str__ method call (called when someone wants to obtain session id) in case session is reloading
        self.session_reload_lock = threading.Lock()

        self.load_cached_session()
        if not SessionManager.is_session_valid(self._session):
            # create a new session
            self.update_session(self._session)
            # and cache it
            SessionManager.cache_session(self._session)
        self.create_session_refresh_timer()

    def __str__(self) -> str:
        with self.session_reload_lock:
            return self._session.id

    @staticmethod
    def is_session_valid(session) -> bool:
        """Checks if the session is valid.
        Session is considered valid only if it was successfully loaded it and its lifetime has not expired yet

        Returns:
            bool: Whether or not session could be considered as a valid one
        """
        print("Validating session...")
        session_valid = False
        if session.creation_time is not None:
            # check if session lifetime has not expired
            # {current time} - {session create time} < {LIFETIME_LIMIT}
            session_valid = time.time() - session.creation_time < Session.LIFETIME_LIMIT
        print(f"Session is {'' if session_valid else 'not '}valid.")
        return session_valid

    def update_session(self, session) -> None:
        with self.session_reload_lock:
            session.update_with_sid(ApiHandler.create_session()['session_id'])

######
# Context management functionality
######
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if hasattr(self, 'timer'):
            self.timer.cancel()

######
# Session refresh functionality
######
    def create_session_refresh_timer(self):
        # session should be refreshed 5s before its expiration time
        backup_time = 5
        planned_session_refresh_time = self._session.creation_time + Session.LIFETIME_LIMIT - backup_time
        refresh_after = max([0, planned_session_refresh_time - time.time()])
        print(f"Session will be refreshed after {int(refresh_after)}sec")
        self.timer = threading.Timer(interval=refresh_after, function=self._timer_callback)
        self.timer.start()

    def _timer_callback(self):
        # create a new session
        self.update_session(self._session)
        # and cache it
        SessionManager.cache_session(self._session)
        # set new timer
        self.create_session_refresh_timer()

######
# Session cache functionality
######
    def load_cached_session(self) -> None:
        try:
            with self.session_reload_lock:
                # update instead of assign to avoid accidental data erase
                self._session.__dict__.update(cuts.json_contents(Session.CACHE_LOCATION))
                print(f"Data was successfully loaded from cache: {self._session.__dict__}")
        except:
            print(f"No cached session found")

    @staticmethod
    def cache_session(session) -> None:
        print(f"Session cached to {Session.CACHE_LOCATION} as {session.__dict__}")
        cuts.dump_to_json(Session.CACHE_LOCATION, session.__dict__)
