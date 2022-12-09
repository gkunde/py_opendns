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
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainActivityRecord:

    rank: int = None

    report_period: datetime = None

    hostname: str = None
    requests: int = None

    is_blocked_hostname: bool = None
    is_blocked_category: bool = None
    is_blocked_malware: bool = None
    is_blocked_botnet: bool = None
    is_blocked_phishing: bool = None
    is_smartcache_resolved: bool = None

    is_academic_fraud: bool = None
    is_adult_themes: bool = None
    is_advertisements: bool = None
    is_adware: bool = None
    is_alcohol: bool = None
    is_anime_manga_webcomic: bool = None
    is_auctions: bool = None
    is_automotive: bool = None
    is_blogs: bool = None
    is_business_services: bool = None
    is_chat: bool = None
    is_classifieds: bool = None
    is_dating: bool = None
    is_drugs: bool = None
    is_ecommerce_shopping: bool = None
    is_educational_institutions: bool = None
    is_file_storage: bool = None
    is_financial_institutions: bool = None
    is_forums_message_boards: bool = None
    is_gambling: bool = None
    is_games: bool = None
    is_german_youth_protection: bool = None
    is_government: bool = None
    is_hate_discrimination: bool = None
    is_health_and_fitness: bool = None
    is_humor: bool = None
    is_instant_messaging: bool = None
    is_jobs_employment: bool = None
    is_lingerie_bikini: bool = None
    is_movies: bool = None
    is_music: bool = None
    is_news_media: bool = None
    is_non_profits: bool = None
    is_nudity: bool = None
    is_p2p_file_sharing: bool = None
    is_parked_domains: bool = None
    is_photo_sharing: bool = None
    is_podcasts: bool = None
    is_politics: bool = None
    is_pornography: bool = None
    is_portals: bool = None
    is_proxy_anonymizer: bool = None
    is_radio: bool = None
    is_religious: bool = None
    is_research_reference: bool = None
    is_search_engines: bool = None
    is_sexuality: bool = None
    is_social_networking: bool = None
    is_software_technology: bool = None
    is_sports: bool = None
    is_tasteless: bool = None
    is_television: bool = None
    is_tobacco: bool = None
    is_travel: bool = None
    is_video_sharing: bool = None
    is_visual_search_engines: bool = None
    is_weapons: bool = None
    is_web_spam: bool = None
    is_webmail: bool = None

@dataclass
class UniqueIpAddressRecord:

    report_period: datetime = None
    ip_addresses: int = None

@dataclass
class TotalRequestsRecord:

    report_period: datetime = None
    requests: int = None

@dataclass
class TotalUniqueDomainsRecord:

    report_period: datetime = None
    unique_domains: int = None

@dataclass
class RequestTypesRecord:

    report_period: datetime = None

    request_type: str = None
    requests: int = None