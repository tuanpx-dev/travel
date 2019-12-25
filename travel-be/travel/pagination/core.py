DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0

class Paginator:
    def __init__(self, content=None, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, total_length=DEFAULT_LIMIT):
        if content is None:
            content = []
        self.content = content
        self.limit = limit
        self.offset = offset
        self.total_length = total_length
        self.page_length = len(content)

    @property
    def data(self):
        serializer = {'content': self.content, 'limit': self.limit, 'offset': self.offset,
                      'page_length': self.page_length,
                      'total_length': self.total_length}
        return serializer