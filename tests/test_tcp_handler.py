from pygelf import GelfTcpHandler
import logging
import json
import pytest
import mock


@pytest.fixture
def handler():
    return GelfTcpHandler(host='127.0.0.1', port=12000, version='2.2')


@pytest.yield_fixture
def send(handler):
    with mock.patch.object(handler, 'send') as mock_send:
        yield mock_send


@pytest.yield_fixture
def logger(handler):
    logger = logging.getLogger('test')
    logger.addHandler(handler)
    yield logger


def log_and_decode(_logger, _send, text, *args):
    _logger.exception(text) if isinstance(text, Exception) else _logger.warning(text, *args)
    message = _send.call_args[0][0].replace(b'\x00', b'').decode('utf-8')
    return json.loads(message)


def test_null_character(logger, send):
    logger.warning('null termination')
    message = send.call_args[0][0].decode('utf-8')
    assert message[-1] == '\x00'


def test_version(logger, send):
    message = log_and_decode(logger, send, 'custom version')
    assert message['version'] == '2.2'
