from logging.handlers import SocketHandler
from pygelf.gelfmessage import GelfMessage


class GelfTcpHandler(SocketHandler):

    def __init__(self, host, port, debug=False, **kwargs):
        """
        :param host: gelf tcp input host
        :param port: gelf tcp input port
        :param debug: include debug fields, e.g. line number
        :param kwargs: additional fields that will be included in the log message, e.g. app name
        """

        super(GelfTcpHandler, self).__init__(host, port)
        self.additional_fields = kwargs
        self.debug = debug
        self.additional_fields.pop('_id', None)

    def makePickle(self, record):
        message = GelfMessage(record, self.debug, self.additional_fields)
        return message.pack() + b'\x00'
