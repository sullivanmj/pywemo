"""Configuration for pyWeMo's use of the aiohttp library"""

import aiohttp
import atexit

_async_client_session: aiohttp.ClientSession
_initialized_async_client_session = False


def _get_async_client_session() -> aiohttp.ClientSession:
    """Get a client session that can be used to make async http requests"""
    global _async_client_session

    if _async_client_session is None:
        initialize_async_client_session()

    return _async_client_session


def initialize_async_client_session(client_session: aiohttp.ClientSession = None
        ) -> None:
    """Initialize the client session that pyWeMo uses.

    If a client_session is not passed in, then one will be created. On
    subsequent calls, if the previous call resulted in the creation of a new
    ClientSession, then that session will be closed, before a new ClientSession
    is initialized."""
    global _async_client_session, _initialized_async_client_session

    if _initialized_async_client_session:
        _async_client_session.close()

    if client_session is not None:
        _async_client_session = client_session
    else:
        _async_client_session = aiohttp.ClientSession()
        _initialized_async_client_session = True


def _cleanup_async_client_session():
    global _async_client_session, _initialized_async_client_session

    if _initialized_async_client_session:
        _async_client_session.close()


atexit.register(_cleanup_async_client_session)
