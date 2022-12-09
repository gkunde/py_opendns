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
from datetime import datetime
from io import IOBase
import unittest

from opendns.data_repository import ReportDataRepository
from opendns.interfaces.i_data_source import IDataSource
from opendns.models import DomainActivityRecord, RequestTypesRecord, TotalRequestsRecord, TotalUniqueDomainsRecord, UniqueIpAddressRecord


class TestDataRepository(unittest.TestCase):

    class _DataSource(IDataSource):

        def get_endpoint(self, endpoint: str, params: list[tuple[str, str | None]] = None, file: IOBase = None) -> None:

            if "topdomains" in endpoint:
                file.write('Rank,Domain,Total,Blacklisted,"Blocked by Category","Blocked as Botnet","Blocked as Malware","Blocked as Phishing","Resolved by SmartCache","Academic Fraud","Adult Themes",Advertisements,Adware,Alcohol,Anime/Manga/Webcomic,Auctions,Automotive,Blogs,"Business Services",Chat,Classifieds,Dating,Drugs,Ecommerce/Shopping,"Educational Institutions","File Storage","Financial Institutions","Forums/Message boards",Gambling,Games,"German Youth Protection",Government,Hate/Discrimination,"Health and Fitness",Humor,"Instant Messaging",Jobs/Employment,Lingerie/Bikini,Movies,Music,News/Media,Non-Profits,Nudity,"P2P/File sharing","Parked Domains","Photo Sharing",Podcasts,Politics,Pornography,Portals,Proxy/Anonymizer,Radio,Religious,Research/Reference,"Search Engines",Sexuality,"Social Networking",Software/Technology,Sports,Tasteless,Television,Tobacco,Travel,"Video Sharing","Visual Search Engines",Weapons,"Web Spam",Webmail')
                file.write("\n")
                file.write(
                    '1,www.example.com,4321,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
                file.write("\n")

            if "uniqueips" in endpoint:
                file.write('Date,IP Addresses')
                file.write("\n")
                file.write('2005-11-01 00:00:00,1')
                file.write("\n")

            if "requesttypes" in endpoint:
                file.write('Request Type,Requests')
                file.write("\n")
                file.write('A,4321')
                file.write("\n")

            if "totalrequests" in endpoint:
                file.write('Date,Requests')
                file.write("\n")
                file.write('2005-11-01 00:00:00 ,4321')
                file.write("\n")

            if "uniquedomains" in endpoint:
                file.write('Date,Requests')
                file.write("\n")
                file.write('2005-11-01 00:00:00 ,4321')
                file.write("\n")

        def post_endpoint(self, endpoint: str, params: list[tuple[str, str | None]] = None) -> None:
            return super().post_endpoint(endpoint, params)

    def test_init(self):

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        self.assertIs(obj.data_source, ds)
        self.assertEqual(obj.data_source, ds)

    def test_get_domain_activity_records(self):

        reportdate = datetime(2005, 11, 1, 0, 0, 0)

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        records = list(obj.get_domain_activity_records("1", reportdate.date()))

        self.assertEqual(len(records), 1)

        self.assertIsInstance(records[0], DomainActivityRecord)

        self.assertEqual(records[0].rank, 1)
        self.assertEqual(records[0].report_period, reportdate)
        self.assertEqual(records[0].hostname, "www.example.com")
        self.assertEqual(records[0].requests, 4321)

        self.assertTrue(records[0].is_blocked_hostname)
        self.assertFalse(records[0].is_blocked_category)
        self.assertFalse(records[0].is_blocked_malware)
        self.assertFalse(records[0].is_blocked_botnet)
        self.assertFalse(records[0].is_blocked_phishing)
        self.assertFalse(records[0].is_smartcache_resolved)

        self.assertFalse(records[0].is_academic_fraud)
        self.assertFalse(records[0].is_adult_themes)
        self.assertFalse(records[0].is_advertisements)
        self.assertFalse(records[0].is_adware)
        self.assertFalse(records[0].is_alcohol)
        self.assertFalse(records[0].is_anime_manga_webcomic)
        self.assertFalse(records[0].is_auctions)
        self.assertFalse(records[0].is_automotive)
        self.assertFalse(records[0].is_blogs)
        self.assertFalse(records[0].is_business_services)
        self.assertFalse(records[0].is_chat)
        self.assertFalse(records[0].is_classifieds)
        self.assertFalse(records[0].is_dating)
        self.assertFalse(records[0].is_drugs)
        self.assertFalse(records[0].is_ecommerce_shopping)
        self.assertFalse(records[0].is_educational_institutions)
        self.assertFalse(records[0].is_file_storage)
        self.assertFalse(records[0].is_financial_institutions)
        self.assertFalse(records[0].is_forums_message_boards)
        self.assertFalse(records[0].is_gambling)
        self.assertFalse(records[0].is_games)
        self.assertFalse(records[0].is_german_youth_protection)
        self.assertFalse(records[0].is_government)
        self.assertFalse(records[0].is_hate_discrimination)
        self.assertFalse(records[0].is_health_and_fitness)
        self.assertFalse(records[0].is_humor)
        self.assertFalse(records[0].is_instant_messaging)
        self.assertFalse(records[0].is_jobs_employment)
        self.assertFalse(records[0].is_lingerie_bikini)
        self.assertFalse(records[0].is_movies)
        self.assertFalse(records[0].is_music)
        self.assertFalse(records[0].is_news_media)
        self.assertFalse(records[0].is_non_profits)
        self.assertFalse(records[0].is_nudity)
        self.assertFalse(records[0].is_p2p_file_sharing)
        self.assertFalse(records[0].is_parked_domains)
        self.assertFalse(records[0].is_photo_sharing)
        self.assertFalse(records[0].is_podcasts)
        self.assertFalse(records[0].is_politics)
        self.assertFalse(records[0].is_pornography)
        self.assertFalse(records[0].is_portals)
        self.assertFalse(records[0].is_proxy_anonymizer)
        self.assertFalse(records[0].is_radio)
        self.assertFalse(records[0].is_religious)

        self.assertTrue(records[0].is_research_reference)

        self.assertFalse(records[0].is_search_engines)
        self.assertFalse(records[0].is_sexuality)
        self.assertFalse(records[0].is_social_networking)
        self.assertFalse(records[0].is_software_technology)
        self.assertFalse(records[0].is_sports)
        self.assertFalse(records[0].is_tasteless)
        self.assertFalse(records[0].is_television)
        self.assertFalse(records[0].is_tobacco)
        self.assertFalse(records[0].is_travel)
        self.assertFalse(records[0].is_video_sharing)
        self.assertFalse(records[0].is_visual_search_engines)
        self.assertFalse(records[0].is_weapons)
        self.assertFalse(records[0].is_web_spam)
        self.assertFalse(records[0].is_webmail)

    def test_get_request_types_records(self):

        reportdate = datetime(2005, 11, 1, 0, 0, 0)

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        records = list(obj.get_request_types_records("1", reportdate.date()))

        self.assertEqual(len(records), 1)

        self.assertIsInstance(records[0], RequestTypesRecord)

        self.assertEqual(records[0].report_period, reportdate)
        self.assertEqual(records[0].request_type, "A"),
        self.assertEqual(records[0].requests, 4321)

    def test_get_total_requests_records(self):

        reportdate = datetime(2005, 11, 1, 0, 0, 0)

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        records = list(obj.get_total_requests_records("1", reportdate.date()))

        self.assertEqual(len(records), 1)

        self.assertIsInstance(records[0], TotalRequestsRecord)

        self.assertEqual(records[0].report_period, reportdate)
        self.assertEqual(records[0].requests, 4321)

    def test_get_total_unique_domains_records(self):

        reportdate = datetime(2005, 11, 1, 0, 0, 0)

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        records = list(
            obj.get_total_unique_domains_records("1", reportdate.date()))

        self.assertEqual(len(records), 1)

        self.assertIsInstance(records[0], TotalUniqueDomainsRecord)

        self.assertEqual(records[0].report_period, reportdate)
        self.assertEqual(records[0].unique_domains, 4321)

    def test_get_unique_ipaddress_records(self):

        reportdate = datetime(2005, 11, 1, 0, 0, 0)

        ds = self._DataSource()

        obj = ReportDataRepository(ds)

        records = list(obj.get_unique_ipaddress_records(
            "1", reportdate.date()))

        self.assertEqual(len(records), 1)

        self.assertIsInstance(records[0], UniqueIpAddressRecord)

        self.assertEqual(records[0].report_period, reportdate)
        self.assertEqual(records[0].ip_addresses, 1)
