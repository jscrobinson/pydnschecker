import dns.resolver
from dns.exception import DNSException
import json
import os
import re
from .util import classproperty
class DnsChecker:
    def __init__(self, dns_config_source, output):
        self.dns_config_source = dns_config_source
        self.output = output

    @property
    def dnsconfig(self):
        if not hasattr(self, "_dnsconfig"):
            self._dnsconfig = json.load(self.dns_config_source)
        return self._dnsconfig

    def filter_dns(self, countries):
        if not countries:
            return self.dnsconfig
        return [x for x in self.dnsconfig if x['country'] in countries]

    @classproperty
    def dns_types(self):
        return [
            attr for attr in dir(dns.rdatatype) 
            if attr[0] != "_" 
            and attr[:2] + attr[-2:] != "____" 
            and not callable(getattr(dns.rdatatype,attr)) 
            and not re.match("[a-z]+", attr)
        ]

    def check_host(self, hostname, countries, record_type):
        for dns_source in self.filter_dns(countries):
            self.output.info("%s, %s (%s)" % (dns_source["provider"], dns_source['location'], dns_source["ip"]))
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_source["ip"]]
            try:
                result = resolver.query(qname=hostname, rdtype=record_type)
                for val in result:
                    self.output.success(val)
            except DNSException as e:
                self.output.error(str(e))
        # print("%s,%s,%s" % (hostname, " ".join(countries), record_type))