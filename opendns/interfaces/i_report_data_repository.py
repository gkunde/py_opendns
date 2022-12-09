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

from ..models import (DomainActivityRecord, RequestTypesRecord, TotalRequestsRecord, TotalUniqueDomainsRecord,
                      UniqueIpAddressRecord)


class IReportDataRepository(metaclass=ABCMeta):
    """
    An interface class for creating a data repository that provides methods
    returning normalized data from a data source.
    """

    @abstractmethod
    def get_domain_activity_records(
            self,
            network_refid: str,
            reportdate: date) -> Generator[DomainActivityRecord, None, None]:
        """
        Retrieves domain activity report records.

        :param network_refid: A string to identify a network to capture
            records for.

        :param reportdate: A date object that represents the reporting period.

        :returns: A Generator object providing DomainActivityRecord objects.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_request_types_records(
            self,
            network_refid: str,
            reportdate: date) -> Generator[RequestTypesRecord, None, None]:
        """
        Retrieves Request Types Report Records.

        :param network_refid: A string to identify a network to capture
            records for.

        :param reportdate: A date object that represents the reporting period.

        :returns: A Generator object providing RequestTypesRecord objects.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_total_requests_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalRequestsRecord, None, None]:
        """
        Retrieves Total Request Report Records. Date ranges less than 1 week
        will return hourly data.

        :param network_ref_id: A string to identify a network to capture
            records for.

        :param reportdate_start: A date object that represents the reporting
            period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing TotalRequestsRecord objects.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_total_unique_domains_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalUniqueDomainsRecord, None, None]:
        """
        Retrieves Total Unique Domain Report Records. Date ranges less than 1
        week will return hourly data.

        :param network_ref_id: A string to identify a network to capture
            records for.

        :param reportdate_start: A date object that represents the reporting
            period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing TotalUniqueDomainsRecord objects.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_unique_ipaddress_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[UniqueIpAddressRecord, None, None]:
        """
        Retrieves Unique IP Address Report Records. Date ranges less than 1
        week will return hourly data.

        :param network_ref_id: A string to identify a network to capture
            records for.

        :param reportdate_start: A date object that represents the reporting
            period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing UniqueIpAddressRecord objects.
        """
        raise NotImplementedError()
