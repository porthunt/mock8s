class MockV1ServiceList:
    def __init__(self, api_version=None, items=None, kind=None, metadata=None):
        self._api_version = None
        self._items = None
        self._kind = None
        self._metadata = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
        self.items = items
        if kind is not None:
            self.kind = kind
        if metadata is not None:
            self.metadata = metadata
