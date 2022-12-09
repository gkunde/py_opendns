"""
MIT License

Copyright (c) 2022 Garrett Kunde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from contextlib import contextmanager
from html.parser import HTMLParser
from io import IOBase
from urllib.parse import SplitResult, urlsplit

import requests
import requests.utils

from .interfaces.i_data_source import IDataSource
from .rate_limiter import RateLimiter


class DataSource(IDataSource):
    """
    A DataSource class for connecting to OpenDNS and establishing a session
    with the service providers website.

    :param username: A string value of the account's username to
        authenticate with. This value should be the email address associated
        to the account.

    :param password: A string value of the account's password to authenticate
        with.
    """

    # 1 MiB
    FILE_CHUNKSIZE = 1048576

    DEFAULT_ENCODING = "UTF-8"

    _CLIENT_NAME = "dashboard-browser"
    _CLIENT_VERSION = "0.5.0"

    _USERNAME_FIELD = "username"
    _PASSWORD_FIELD = "password"

    _LOGIN_URL = "https://login.opendns.com/?return_to=https%3A%2F%2Fdashboard.opendns.com%2F"
    _LOGOUT_URL = "https://login.opendns.com/logout/?source=&return_to=https%3A%2F%2Fdashboard.opendns.com%2F"
    _ROOT_URL = "https://dashboard.opendns.com/"

    _USER_AGENT_FIELD = "User-Agent"

    def __init__(self, username: str, password: str) -> None:

        self.chunk_size = self.FILE_CHUNKSIZE

        self.user_agent = self._get_user_agent()

        self._username = username
        self._password = password

        # Not intended for use, here to make changing the values easier.
        self._login_url = self._LOGIN_URL
        self._logout_url = self._LOGOUT_URL
        self._root_url_split = urlsplit(self._ROOT_URL)
        self._username_field = self._USERNAME_FIELD
        self._password_field = self._PASSWORD_FIELD

        self._rate_limiter = RateLimiter(
            num_requests=19,
            period=120)

        self.__is_connected = False
        self.__session = requests.Session()

    def get_endpoint(
            self,
            endpoint: str,
            params: list[tuple[str, str | None]] = None,
            file: IOBase = None) -> str | None:
        """
        Fetches data from the given endpoint. Data return will be return as-is
        per the website being connected to. Data may be represented as HTML,
        plain text, or formatted as a CSV document.

        :param endpoint: A string path to the endpoint to retrieve data for.

        :param params: A collection of query string values to include with the
            endpoint.

        :param file: An IOBase object for capturing larger data files or
            streams.

        :returns: A string value containing the retrieved content. If the file
            param is specified, no value is returned.
        """

        self._rate_limiter.check()

        split_url = SplitResult(
            self._root_url_split.scheme, self._root_url_split.netloc, endpoint, None, None)

        is_stream = (file is not None)

        content = None
        with self._make_connection() as connection:
            
            response = connection.get(split_url.geturl(), params=params, stream=is_stream)

            response.raise_for_status()

            response.encoding = self._determine_encoding(response.encoding)

            if not is_stream:
                content = response.content

            else:
                for file_chunk in response.iter_content(chunk_size=self.chunk_size, decode_unicode=True):
                    file.write(file_chunk)

        return content

    def post_endpoint(self, endpoint: str, params: list[tuple[str, str | None]] = None) -> str | None:
        """
        Allows data to be posted to given endpoint. Not currently implemented.
        """

        self._rate_limiter.check()

        return super().post_endpoint(endpoint, params)

    def _determine_encoding(self, response_encoding: str) -> str:
        """
        Returns the encoding or default encoding if the provided value is None

        :param response_encoding: A encoding value obtained from an HTTP
            response.

        :returns: Returns the DEFAULT_ENCODING, unless response_encoding
            contains a value.
        """

        return response_encoding if response_encoding else self.DEFAULT_ENCODING

    @contextmanager
    def _make_connection(self) -> requests.Session:
        """
        Manages the requests.Session object used to communicate with the
        provider.

        :raises RuntimeError: If the site is reporting error messages or an
            authentication token cannot be obtained.
        """

        if not self.__is_connected:

            self.__session.headers.update(
                {self._USER_AGENT_FIELD: self.user_agent})

            response = self.__session.get(self._login_url)
            response.raise_for_status()

            login_page = LoginPageParser()
            login_page.feed(response.text)

            if login_page.error_msg is not None:
                raise RuntimeError(login_page.error_msg)

            params = []
            for field in login_page.fields:

                if field[0] == self._username_field:
                    params.append((field[0], self._username, ))

                elif field[0] == self._password_field:
                    params.append((field[0], self._password, ))

                else:
                    params.append(field)

            if not params:
                raise RuntimeError(
                    "Service Unavailable. Check https://login.opendns.com for more information.")

            if login_page.form_method != "POST":
                raise RuntimeError(
                    "Unable to login, invalid submission method.")

            response = self.__session.post(login_page.form_action, data=params)
            response.raise_for_status()

            login_page = LoginPageParser()
            login_page.feed(response.text)

            if login_page.error_msg is not None:
                raise RuntimeError(login_page.error_msg)

            self.__is_connected = True

        yield self.__session

    def _get_user_agent(self) -> str:
        """
        Generates an User-Agent string for the HTTP client.
        """

        return requests.utils.default_headers()[self._USER_AGENT_FIELD] + f" {self._CLIENT_NAME}/{self._CLIENT_VERSION}"


class LoginPageParser(HTMLParser):
    """
    A OpenDNS login page parser.

    Attributes:
    error_msg: A string value containing any error message scraped from the
        returned page.

    fields: A collection of form input fields used for authentication.

    form_action: The URL to post back values in fields to.

    form_method: The appropriate method to send authentication fields to the
        provider.
    """

    FORM_NAME = "signin"

    def __init__(self) -> None:

        super().__init__()

        self.error_msg = None

        self.fields = []

        self.form_action = None
        self.form_method = "GET"

        self.__enable_capture = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:

        if tag == "form":

            for name, val in attrs:

                if name == "name" and val == self.FORM_NAME:
                    self.__enable_capture = True

                elif name == "method":
                    self.form_method = val.strip().upper() if val is not None else self.form_method

                elif name == "action":
                    self.form_action = val.strip() if val is not None else None

        elif tag == "input":

            field_name = None
            field_value = None

            is_capture = self.__enable_capture

            for name, val in attrs:

                if name == "name":
                    field_name = val.strip() if val is not None else None

                elif name == "value":
                    field_value = val.strip() if val is not None else None

                elif name == "form":
                    is_capture = (val == self.FORM_NAME)

            if is_capture:

                self.fields.append((field_name, field_value, ))

        elif tag == "div":

            for name, val in attrs:

                if name == "class" and "error-text" in val:
                    self.error_msg = "Login failed. Check your username and/or password. Check https://login.opendns.com for more information."

    def handle_endtag(self, tag: str) -> None:

        if tag == "form":
            self.__enable_capture = False
