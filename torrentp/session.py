class Session:
    def __init__(self, libtorrent):
        self._user_agent = 'python client v0.1'
        self._listen_interfaces = '0.0.0.0'
        self._port = '6881'
        self._download_rate_limit = 0
        self._download_rate_limit = 0
        self._lt = libtorrent

    def create_session(self):
        return self._lt.session({'listen_interfaces':f'{self._listen_interfaces}:{self._port}'})
        
    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        return self.create_session()
