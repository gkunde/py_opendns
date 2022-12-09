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
from csv import DictReader
from datetime import date, datetime
from io import StringIO
from typing import Any, Generator

from .interfaces.i_data_source import IDataSource
from .interfaces.i_report_data_repository import IReportDataRepository
from .models import (DomainActivityRecord, RequestTypesRecord, TotalRequestsRecord, TotalUniqueDomainsRecord,
                     UniqueIpAddressRecord)


class ReportDataRepository(IReportDataRepository):
    """
    Provides methods for retrieving and normalizing reporting data provided
    by an object implementing the IDataSource interface.

    :param data_source: An IDataSource object.
    """

    MAX_PAGES = 1000000

    RPT_DOMAIN = "topdomains"
    RPT_IPADDR = "uniqueips"
    RPT_REQUESTTYPE = "requesttypes"
    RPT_REQUESTS = "totalrequests"
    RPT_UNQDOMAIN = "uniquedomains"

    def __init__(self, data_source: IDataSource) -> None:

        self.data_source = data_source

        self._max_pages = self.MAX_PAGES

        self._report_domain = self.RPT_DOMAIN

        self._report_ipaddress = self.RPT_IPADDR

        self._report_requesttypes = self.RPT_REQUESTTYPE

        self._report_requests = self.RPT_REQUESTS

        self._report_unique_domains = self.RPT_UNQDOMAIN

        self._multipage_report_types = (self._report_domain)

    def get_domain_activity_records(
            self,
            network_refid: str,
            reportdate: date) -> Generator[DomainActivityRecord, None, None]:
        """
        Retrieves domain activity report records.

        :param network_refid: A string to identify a network to capture records for.

        :param reportdate: A date object that represents the reporting period.

        :returns: A Generator object providing DomainActivityRecord objects.
        """

        for entry in self._get_report_records(self._report_domain, network_refid, reportdate, None):

            record = DomainActivityRecord(
                rank=int(entry["Rank"]),
                report_period=datetime(reportdate.year, reportdate.month, reportdate.day),
                hostname=entry["Domain"],
                requests=int(entry["Total"]),
                is_blocked_hostname=entry["Blacklisted"] != "0",
                is_blocked_category=entry["Blocked by Category"] != "0",
                is_blocked_botnet=entry["Blocked as Botnet"] != "0",
                is_blocked_malware=entry["Blocked as Malware"] != "0",
                is_blocked_phishing=entry["Blocked as Phishing"] != "0",
                is_smartcache_resolved=entry["Resolved by SmartCache"] != "0",
                is_academic_fraud=entry["Academic Fraud"] != "0",
                is_adult_themes=entry["Adult Themes"] != "0",
                is_advertisements=entry["Advertisements"] != "0",
                is_adware=entry["Adware"] != "0",
                is_alcohol=entry["Alcohol"] != "0",
                is_anime_manga_webcomic=entry["Anime/Manga/Webcomic"] != "0",
                is_auctions=entry["Auctions"] != "0",
                is_automotive=entry["Automotive"] != "0",
                is_blogs=entry["Blogs"] != "0",
                is_business_services=entry["Business Services"] != "0",
                is_chat=entry["Chat"] != "0",
                is_classifieds=entry["Classifieds"] != "0",
                is_dating=entry["Dating"] != "0",
                is_drugs=entry["Drugs"] != "0",
                is_ecommerce_shopping=entry["Ecommerce/Shopping"] != "0",
                is_educational_institutions=entry["Educational Institutions"] != "0",
                is_file_storage=entry["File Storage"] != "0",
                is_financial_institutions=entry["Financial Institutions"] != "0",
                is_forums_message_boards=entry["Forums/Message boards"] != "0",
                is_gambling=entry["Gambling"] != "0",
                is_games=entry["Games"] != "0",
                is_german_youth_protection=entry["German Youth Protection"] != "0",
                is_government=entry["Government"] != "0",
                is_hate_discrimination=entry["Hate/Discrimination"] != "0",
                is_health_and_fitness=entry["Health and Fitness"] != "0",
                is_humor=entry["Humor"] != "0",
                is_instant_messaging=entry["Instant Messaging"] != "0",
                is_jobs_employment=entry["Jobs/Employment"] != "0",
                is_lingerie_bikini=entry["Lingerie/Bikini"] != "0",
                is_movies=entry["Movies"] != "0",
                is_music=entry["Music"] != "0",
                is_news_media=entry["News/Media"] != "0",
                is_non_profits=entry["Non-Profits"] != "0",
                is_nudity=entry["Nudity"] != "0",
                is_p2p_file_sharing=entry["P2P/File sharing"] != "0",
                is_parked_domains=entry["Parked Domains"] != "0",
                is_photo_sharing=entry["Photo Sharing"] != "0",
                is_podcasts=entry["Podcasts"] != "0",
                is_politics=entry["Politics"] != "0",
                is_pornography=entry["Pornography"] != "0",
                is_portals=entry["Portals"] != "0",
                is_proxy_anonymizer=entry["Proxy/Anonymizer"] != "0",
                is_radio=entry["Radio"] != "0",
                is_religious=entry["Religious"] != "0",
                is_research_reference=entry["Research/Reference"] != "0",
                is_search_engines=entry["Search Engines"] != "0",
                is_sexuality=entry["Sexuality"] != "0",
                is_social_networking=entry["Social Networking"] != "0",
                is_software_technology=entry["Software/Technology"] != "0",
                is_sports=entry["Sports"] != "0",
                is_tasteless=entry["Tasteless"] != "0",
                is_television=entry["Television"] != "0",
                is_tobacco=entry["Tobacco"] != "0",
                is_travel=entry["Travel"] != "0",
                is_video_sharing=entry["Video Sharing"] != "0",
                is_visual_search_engines=entry["Visual Search Engines"] != "0",
                is_weapons=entry["Weapons"] != "0",
                is_web_spam=entry["Web Spam"] != "0",
                is_webmail=entry["Webmail"] != "0")

            yield record

    def get_request_types_records(
            self,
            network_refid: str,
            reportdate: date) -> Generator[RequestTypesRecord, None, None]:
        """
        Retrieves Request Types Report Records.

        :param network_refid: A string to identify a network to capture records for.

        :param reportdate: A date object that represents the reporting period.

        :returns: A Generator object providing RequestTypesRecord objects.
        """

        for entry in self._get_report_records(self._report_requesttypes, network_refid, reportdate, None):

            record = RequestTypesRecord(
                report_period=datetime(reportdate.year, reportdate.month, reportdate.day),
                request_type=entry["Request Type"],
                requests=int(entry["Requests"])
            )

            yield record

    def get_total_requests_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalRequestsRecord, None, None]:
        """
        Retrieves Total Request Report Records. Date ranges less than 1 week
        will return hourly data.

        :param network_ref_id: A string to identify a network to capture records for.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing TotalRequestsRecord objects.
        """

        for entry in self._get_report_records(self._report_requests, network_refid, reportdate_start, reportdate_end):

            report_period = self._parse_reportperiod(entry["Date"])

            record = TotalRequestsRecord(
                report_period=report_period,
                requests=int(entry["Requests"]))

            yield record

    def get_total_unique_domains_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[TotalUniqueDomainsRecord, None, None]:
        """
        Retrieves Total Unique Domain Report Records. Date ranges less than 1
        week will return hourly data.

        :param network_refid: A string to identify a network to capture records for.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing TotalUniqueDomainsRecord objects.
        """

        for entry in self._get_report_records(self._report_unique_domains, network_refid, reportdate_start, reportdate_end):

            report_period = self._parse_reportperiod(entry["Date"])

            record = TotalUniqueDomainsRecord(
                report_period=report_period,
                unique_domains=int(entry["Requests"]))

            yield record

    def get_unique_ipaddress_records(
            self,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date = None) -> Generator[UniqueIpAddressRecord, None, None]:
        """
        Retrieves Unique IP Address Report Records. Date ranges less than 1
        week will return hourly data.

        :param network_refid: A string to identify a network to capture records for.

        :param reportdate_start: A date object that represents the reporting period start.

        :param reportdate_end: A date object that represents the reporting
            period end, if not provided a single day report is requested.

        :returns: A Generator object providing UniqueIpAddressRecord objects.
        """

        for entry in self._get_report_records(self._report_ipaddress, network_refid, reportdate_start, reportdate_end):

            report_period = self._parse_reportperiod(entry["Date"])

            record = UniqueIpAddressRecord(
                report_period=report_period,
                ip_addresses=int(entry["IP Addresses"]))

            yield record

    def _get_report_records(
            self,
            report_type: str,
            network_refid: str,
            reportdate_start: date,
            reportdate_end: date) -> Generator[dict[str, Any], None, None]:
        """
        Makes calls to the data_source object to retrieve data from service
        provider.

        :param report_type: A string to identify when reporting data to
            retrieve.

        :param network_refid: A string to identify a network to retrieve data
            for.
        
        :param reportdate_start: A date object that represents the reporting
            period start.

        :param reportdate_end: A date object that represents the reporting
            period end. If None or matches reportdate_start, this value is
            ignored.
        
        :returns: A Generator object containing dictionary objects of string
            keys for field names and objects for field values as provided by
            csv.DictReader parsing.
        """

        max_pages = self._max_pages if report_type in self._multipage_report_types else 1
        # adjust for off-by-one (using cardinal counting)
        max_pages += 1

        report_range = reportdate_start.isoformat()
        if reportdate_end is not None and reportdate_end != reportdate_start:
            report_range = f"{report_range}to{reportdate_end.isoformat()}"

        for page in range(1, max_pages):

            page_segment = f"/page{page}"
            if page == 1:
                page_segment = ""

            opendns_path = f"/stats/{network_refid}/{report_type}/{report_range}{page_segment}.csv"

            has_data = False
            record_count = 0

            with StringIO() as file:

                self.data_source.get_endpoint(opendns_path, None, file)

                file.seek(0)

                reader = DictReader(file)

                for entry in reader:

                    has_data = True
                    record_count += 1

                    yield entry

            if not has_data or record_count <= 2:
                break

    def _parse_reportperiod(self, report_period: str) -> datetime:
        """
        A datetime object normalizing method.

        :param report_period: A string representation of a date object.
        """

        return datetime.strptime(report_period.strip(), "%Y-%m-%d %H:%M:%S")
