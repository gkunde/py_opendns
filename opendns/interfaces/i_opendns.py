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
from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Generator

from ..models import (DomainActivityRecord, RequestTypesRecord, TotalRequestsRecord,
                      TotalUniqueDomainsRecord, UniqueIpAddressRecord)


class IOpenDns(metaclass=ABCMeta):
    """
    An interface class for creating an OpenDns instance that provides methods
    fetching information from OpenDNS's website.
    """

    @abstractmethod
    def get_domain_activity_report(
            self,
            reportdate: date) -> Generator[DomainActivityRecord, None, None]:
        """
        Retrieve the Domain Activity report.

        :param reportdate: A date object that represents the reporting period.

        :returns: A generator object containing the report records.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_request_types_report(
            self,
            reportdate: date) -> Generator[RequestTypesRecord, None, None]:
        """
        Retrieve the Request Types report.

        :param reportdate: A date object that represents the reporting period.

        :returns: A generator object containing the report records.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_total_requests_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalRequestsRecord, None, None]:
        """
        Retrieve the Total Requests report.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reoirtdate_end: A date object that represents the reporting period end.

        :returns: A generator object containing the report records.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_total_unique_domains_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalUniqueDomainsRecord, None, None]:
        """
        Retrieve the Total Unique Domains report.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reoirtdate_end: A date object that represents the reporting period end.

        :returns: A generator object containing the report records.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_unique_ipaddress_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[UniqueIpAddressRecord, None, None]:
        """
        Retrieve the Unique IP Address report.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reoirtdate_end: A date object that represents the reporting period end.

        :returns: A generator object containing the report records.
        """
        raise NotImplementedError()
