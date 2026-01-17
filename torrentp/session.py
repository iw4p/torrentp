from pedros import get_logger

logger = get_logger(__name__)


class Session:
    def __init__(self, libtorrent, port='6881'):
        self._user_agent = 'python client v0.1'
        self._listen_interfaces = '0.0.0.0'
        self._port = port
        self._download_rate_limit = 0
        self._upload_rate_limit = 0
        self._lt = libtorrent
        self._session = None

    def create_session(self):
        self._session = self._lt.session({'listen_interfaces':f'{self._listen_interfaces}:{self._port}'})
        logger.info(f"Session created on port {self._port}")
        return self._session

    def set_download_limit(self, rate=0):
        self._download_rate_limit = int(-1 if rate == 0 else (1 if rate == -1 else rate * 1024))
        self._session.set_download_rate_limit(self._download_rate_limit)
        if rate > 0:
            logger.info(f"Download rate limit set to {rate} kB/s")

    def set_upload_limit(self, rate=0):
        self._upload_rate_limit = int(-1 if rate == 0 else (1 if rate == -1 else rate * 1024))
        self._session.set_upload_rate_limit(self._upload_rate_limit)
        if rate > 0:
            logger.info(f"Upload rate limit set to {rate} kB/s")

    def get_upload_limit(self):
        return self._session.upload_rate_limit()

    def get_download_limit(self):
        return self._session.download_rate_limit()

    def shutdown(self):
        if self._session:
            self._session.pause()
            del self._session
            self._session = None
            logger.info("Session shutdown successfully.")

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        return self.create_session()
