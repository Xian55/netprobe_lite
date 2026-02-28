# Network tests
import subprocess
import json
import time
from threading import Thread
import dns.resolver
import speedtest


class NetworkCollector(object): # Main network collection class

    def __init__(self,sites,count,dns_test_site,nameservers_external):
        self.sites = sites # List of sites to ping
        self.count = str(count) # Number of pings
        self.stats = [] # List of stat dicts
        self.dnsstats = [] # List of stat dicts
        self.dns_test_site = dns_test_site # Site used to test DNS response times
        self.nameservers = []
        self.nameservers = nameservers_external


    def pingtest(self,count,site):

        try:
            result = subprocess.run(
                ["ping", "-n", "-i", "0.1", "-c", count, site],
                capture_output=True, text=True, timeout=30
            )
            ping = result.stdout
            # Extract rtt and loss lines
            lines = [l for l in ping.split('\n') if 'rtt' in l or 'loss' in l]
            ping = '\n'.join(lines)
        except subprocess.TimeoutExpired:
            print(f"Ping timed out for {site}")
            return False
        except Exception as e:
            print(f"Error running ping for {site}: {e}")
            return False

        try:
            loss = ping.split(' ')[5].strip('%')
            latency=ping.split('/')[4]
            jitter=ping.split('/')[6].split(' ')[0]

            netdata = {
                "site":site,
                "latency":latency,
                "loss":loss,
                "jitter":jitter
            }

            self.stats.append(netdata)

        except Exception as e:
            print(f"Error parsing ping output for {site}: {e}")
            return False

        return True

    def dnstest(self,site,nameserver,retries=3):

        server = [nameserver[1]]

        for attempt in range(1, retries + 1):
            my_resolver = dns.resolver.Resolver()
            my_resolver.nameservers = server
            my_resolver.timeout = 5       # Per-request timeout in seconds
            my_resolver.lifetime = 10     # Total time allowed for all attempts

            try:
                answers = my_resolver.resolve(site,'A')

                dns_latency = round(answers.response.time * 1000,2)

                dnsdata = {
                    "nameserver":nameserver[0],
                    "nameserver_ip":nameserver[1],
                    "latency":dns_latency
                }

                self.dnsstats.append(dnsdata)
                return True

            except Exception as e:
                print(f"DNS attempt {attempt}/{retries} failed for {nameserver[0]} ({nameserver[1]}): {e}")

                if attempt < retries:
                    time.sleep(1)

        # All retries exhausted
        print(f"DNS resolution failed for {nameserver[0]} ({nameserver[1]}) after {retries} attempts")

        dnsdata = {
            "nameserver":nameserver[0],
            "nameserver_ip":nameserver[1],
            "latency":5000
        }

        self.dnsstats.append(dnsdata)

        return True

    def collect(self):

        # Empty preveious results
        self.stats = []
        self.dnsstats = []

        # Create threads, start them
        threads = []

        for item in self.sites:
            t = Thread(target=self.pingtest, args=(self.count,item,))
            threads.append(t)
            t.start()

        # Wait for threads to complete
        for t in threads:
            t.join()

        # Create threads, start them
        threads = []

        for item in self.nameservers:
            s = Thread(target=self.dnstest, args=(self.dns_test_site,item,))
            threads.append(s)
            s.start()

        # Wait for threads to complete
        for s in threads:
            s.join()

        results = json.dumps({
            "stats":self.stats,
            "dns_stats":self.dnsstats
        })

        return results


class Netprobe_Speedtest(object): # Speed test class

    def __init__(self):
        self.speedtest_stats = {"download": None, "upload": None}

    def netprobe_speedtest(self):

        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            download = s.download()
            upload = s.upload()

            self.speedtest_stats = {
                "download": download,
                "upload": upload
            }
        except Exception as e:
            print(f"Speedtest failed: {e}")
            self.speedtest_stats = {"download": None, "upload": None}

    def collect(self):

        self.netprobe_speedtest()

        results = json.dumps({
            "speed_stats":self.speedtest_stats
        })

        return results
