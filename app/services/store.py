class ComicStore:
    def __init__(self):
        self._store = {}

    def save(self, session_id: str, data: dict):
        self._store[session_id] = data

    def get(self, session_id: str) -> dict:
        return self._store.get(session_id, {})

store = ComicStore()
