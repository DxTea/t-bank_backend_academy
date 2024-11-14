class LogRecord:
    def __init__(self, ip: str, user: str, date: str, request: str,
                 status: int, size: int, referrer: str, agent: str):
        """
        Класс, представляющий запись лога.

        :param ip: IP-адрес клиента.
        :param user: Имя пользователя.
        :param date: Дата и время запроса.
        :param request: Запрос, сделанный клиентом.
        :param status: HTTP статус-код ответа.
        :param size: Размер ответа в байтах.
        :param referrer: URL реферера.
        :param agent: User-Agent клиента.
        """
        self.ip = ip
        self.user = user
        self.date = date
        self.request = request
        self.status = status
        self.size = size
        self.referrer = referrer
        self.agent = agent

    def __eq__(self, other):
        if isinstance(other, LogRecord):
            return (
                    self.ip == other.ip and self.user == other.user and
                    self.date == other.date and
                    self.request == other.request and self.status ==
                    other.status and
                    self.size == other.size and self.referrer ==
                    other.referrer and self.agent == other.agent)
        return False
