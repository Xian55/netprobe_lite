import os
from dotenv import load_dotenv

# Load configs from env

try: # Try to load env vars from file, if fails pass
    load_dotenv()
except Exception:
    pass


# Create class for each

class Config_Netprobe():
    probe_interval = int(os.getenv('PROBE_INTERVAL', '30'))
    probe_count = int(os.getenv('PROBE_COUNT', '10'))
    sites = os.getenv('SITES', 'google.com,facebook.com,twitter.com,youtube.com,amazon.com').split(',')
    dns_test_site = os.getenv('DNS_TEST_SITE', 'google.com')
    speedtest_enabled = os.getenv("SPEEDTEST_ENABLED", 'False').lower() in ('true', '1', 't')
    speedtest_interval = int(os.getenv('SPEEDTEST_INTERVAL', '937'))

    DNS_NAMESERVER_1 = os.getenv('DNS_NAMESERVER_1', 'Google_DNS')
    DNS_NAMESERVER_1_IP = os.getenv('DNS_NAMESERVER_1_IP', '8.8.8.8')
    DNS_NAMESERVER_2 = os.getenv('DNS_NAMESERVER_2', 'Quad9_DNS')
    DNS_NAMESERVER_2_IP = os.getenv('DNS_NAMESERVER_2_IP', '9.9.9.9')
    DNS_NAMESERVER_3 = os.getenv('DNS_NAMESERVER_3', 'CloudFlare_DNS')
    DNS_NAMESERVER_3_IP = os.getenv('DNS_NAMESERVER_3_IP', '1.1.1.1')
    DNS_NAMESERVER_4 = os.getenv('DNS_NAMESERVER_4', 'My_DNS_Server')
    DNS_NAMESERVER_4_IP = os.getenv('DNS_NAMESERVER_4_IP', '8.8.8.8')

    nameservers = [
        (DNS_NAMESERVER_1,DNS_NAMESERVER_1_IP),
        (DNS_NAMESERVER_2,DNS_NAMESERVER_2_IP),
        (DNS_NAMESERVER_3,DNS_NAMESERVER_3_IP),
        (DNS_NAMESERVER_4,DNS_NAMESERVER_4_IP),
    ]

class Config_Redis():
    redis_url = os.getenv('REDIS_URL', 'netprobe-redis')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_password = os.getenv('REDIS_PASSWORD', None)

class Config_Presentation():
    presentation_port = int(os.getenv('PRESENTATION_PORT', '5000'))
    presentation_interface = os.getenv('PRESENTATION_INTERFACE', '0.0.0.0')
    device_id = os.getenv('DEVICE_ID', 'netprobe')

    weight_loss = float(os.getenv('weight_loss', '.6'))
    weight_latency = float(os.getenv('weight_latency', '.15'))
    weight_jitter = float(os.getenv('weight_jitter', '.2'))
    weight_dns_latency = float(os.getenv('weight_dns_latency', '0.05'))

    threshold_loss = int(os.getenv('threshold_loss', '5')) or 5
    threshold_latency = int(os.getenv('threshold_latency', '100')) or 100
    threshold_jitter = int(os.getenv('threshold_jitter', '30')) or 30
    threshold_dns_latency = int(os.getenv('threshold_dns_latency', '100')) or 100
