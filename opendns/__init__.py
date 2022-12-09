"""
MIT License

Copyright (c) 2022 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_opendns
"""
from datetime import date
from typing import Generator

from .data_repository import ReportDataRepository
from .data_source import DataSource
from .interfaces.i_opendns import IOpenDns
from .models import (DomainActivityRecord, RequestTypesRecord, TotalRequestsRecord, TotalUniqueDomainsRecord,
                     UniqueIpAddressRecord)


class OpenDns(IOpenDns):
    """
    A class to enable access to OpenDNS's reporting data and account
    information.

    :param username: A string value of the account's username to
        authenticate with. This value should be the email address associated
        to the account.

    :param password: A string value of the account's password to authenticate
        with.

    :param network_refid: A string value of the netowrk reference id provided
        by OpenDNS. This should be a numeric value that is displayed in the
        URL from OpenDNS's network settings page for a selected network.
    """

    def __init__(self, username: str, password: str, network_refid: str) -> None:

        self.network_refid = network_refid

        self.data_source = DataSource(username, password)

        self.report_data_repository = ReportDataRepository(self.data_source)

    def get_domain_activity_report(self, reportdate: date) -> Generator[DomainActivityRecord, None, None]:
        """
        Fetches the data for the Domain report.

        :param reportdate: A date object to specify the reporting period.

        :returns: A Generator object that returns DomainActivityRecord objects.
        """

        for record in self.report_data_repository.get_domain_activity_records(self.network_refid, reportdate):
            yield record

    def get_request_types_report(self, reportdate: date) -> Generator[RequestTypesRecord, None, None]:
        """
        Fetches the data for the Request Types report.

        :param reportdate: A date object to specify the reporting period.

        :returns: A Generator object that returns RequestTypesRecord objects.
        """

        for record in self.report_data_repository.get_request_types_records(self.network_refid, reportdate):
            yield record

    def get_total_requests_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalRequestsRecord, None, None]:
        """
        Fetches the data for the Total Requests report. Note that report
        ranges less a week will return hourly data.

        :param reportdate_start: A date object to specify the reporting period
            start.

        :param reportdate_end: A date objet to specify the rpeorting period
            end. If not provided, a single day report will be retrieved.

        :returns: A Generator object that reeturn TotalRequestsRecord objects.
        """

        for record in self.report_data_repository.get_total_requests_records(
                self.network_refid,
                reportdate_start,
                reportdate_end):
            yield record

    def get_total_unique_domains_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalUniqueDomainsRecord, None, None]:
        """
        Fetchs the data for the Total Unique Domains report. Note that report
        ranges less a week will return hourly data.

        :param reportdate_start: A date object to specify the reporting period
            start.

        :param reportdate_end: A date objet to specify the rpeorting period
            end. If not provided, a single day report will be retrieved.

        :returns: A Generator object that reeturn TotalUniqueDomainsRecord
            objects.
        """

        for record in self.report_data_repository.get_total_unique_domains_records(
                self.network_refid,
                reportdate_start,
                reportdate_end):
            yield record

    def get_unique_ipaddress_report(
            self,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[UniqueIpAddressRecord, None, None]:
        """
        Fetchs the data for the Total Unique IPs report. Note that report
        ranges less a week will return hourly data.

        :param reportdate_start: A date object to specify the reporting period
            start.

        :param reportdate_end: A date objet to specify the rpeorting period
            end. If not provided, a single day report will be retrieved.

        :returns: A Generator object that reeturn UniqueIpAddressRecord
            objects.
        """

        for record in self.report_data_repository.get_unique_ipaddress_records(
                self.network_refid,
                reportdate_start,
                reportdate_end):
            yield record
