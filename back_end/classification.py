import re
import string

KEYWORD_MAP = {
    "ransomware": [
        "ransomware", "encrypt", "decryptor", "ransom note",
        "double extortion", "data exfiltrated", "lockbit", "blackcat",
        "alphv", "clop", "babuk", "revil", "darkside", "royal",
        "black basta", "conti", "hive ransomware"
    ],

    "data-breach": [
        "data breach", "data leak", "exposed records", "exposed data",
        "compromised data", "stolen database", "database leak",
        "information leak", "unauthorized access", "breach",
        "s3 bucket leak", "publicly exposed data", "leaked database"
    ],

    "zero-day": [
        "zero-day", "0day", "0-day", "actively exploited",
        "exploit in the wild", "weaponized exploit", "poc exploit",
        "proof of concept", "drive-by exploit"
    ],

    "vulnerability": [
        "cve-", "security flaw", "critical vulnerability",
        "high severity vulnerability", "security patch",
        "advisory released", "patch tuesday"
    ],

    "exploit": [
        "remote code execution", "rce", "privilege escalation", "escalate", "privileges", "privilege"
        "pe", "command injection", "sql injection", "sqli",
        "xss", "csrf", "ssrf", "deserialization", "buffer overflow",
        "heap overflow", "memory corruption", "sandbox escape", 'exploit'
    ],

    "malware": [
        "malware", "trojan", "worm", "virus", "rootkit",
        "backdoor", "dropper", "loader", "infostealer",
        "stealer", "keylogger", "spyware", "adware",
        "botnet", "c2 server", "command and control", 'malicious'
    ],

    "trojan": [
        "trojan", "banking trojan", "password stealer",
        "spyware trojan"
    ],

    "botnet": [
        "botnet", "bot-herder", "mirai", "ddos botnet",
        "infected devices", "zombie network"
    ],

    "phishing": [
        "phishing", "spearphishing", "whaling", "credential harvest",
        "fake login", "smishing", "vishing", "impersonation",
        "spoofed email", "malicious attachment"
    ],

    "social-engineering": [
        "social engineering", "scam", "fraud email", "impersonation",
        "deception campaign"
    ],

    "ddos": [
        "ddos", "denial of service", "traffic flood", "udp flood",
        "syn flood", "layer 7 attack"
    ],

    "supply-chain": [
        "supply chain attack", "dependency hijack",
        "typosquatting package", "malicious update",
        "third party compromise", "vendor compromise"
    ],

    "apt": [
        "apt", "apt29", "apt28", "lazarus", "fancy bear",
        "cozy bear", "sandworm", "nation-state", "state sponsored",
        "cyber espionage", "government-backed hackers"
    ],

    "critical-infrastructure": [
        "ics", "scada", "pipeline", "power grid", "utility attack",
        "hospital cyberattack", "industrial control systems",
        "water treatment plant"
    ],

    "cloud-security": [
        "aws breach", "azure breach", "gcp breach", "oauth compromise",
        "misconfigured bucket", "container escape", "kubernetes breach", 
        'aws', 'azure', 'google cloud', 'gcp'
    ],

    "identity": [
        "credential stuffing", "password attack", "session hijack",
        "token leak", "oauth token steal", "mfa bypass",
        "password sprayed", "brute force attack", "token"
    ],

    "dark-web": [
        "dark web", "hacker forum", "sold on dark web",
        "underground marketplace", "criminal marketplace"
    ],

    "cryptojacking": [
        "crypto mining", "cryptojacking", "miner malware",
        "mining campaign", "coinminer"
    ],

    "crypto": [
        "ethereum", "bitcoin", "cryptocurrency"
    ],

    "mobile": [
        "android malware", "ios malware", "malicious app",
        "fake app", "apk trojan", "mobile spyware"
    ],

    "iot": [
        "iot", "smart device hack", "camera hack", "router exploit",
        "iot botnet", "mirai variant"
    ],

    "database-exposure": [
        "database exposed", "open database", "unprotected database",
        "elastic search leak", "mysql leak"
    ],

    "financial": [
        "banking trojan", "payment card leak", "credit card stolen",
        "financial fraud", "bank breach"
    ],

    "insider-threat": [
        "insider", "employee stole data", "internal actor",
        "disgruntled employee"
    ]
}

SEVERITY_MAP = {
    "zero-day": "Critical",
    "apt": "High",
    "ransomware": "High",
    "data-breach": "High",
    "supply-chain": "High",
    "vulnerability": "Medium",
    "exploit": "Medium",
    "malware": "Medium",
    "botnet": "Medium",
    "critical-infrastructure": "High",
    "ddos": "Medium",
    "phishing": "Low",
    "social-engineering": "Low",
    "database-exposure": "Medium",
    "cryptojacking": "Medium",
    "cloud-security": "Medium",
    "financial": "Medium",
    "identity": "Medium",
    "mobile": "Medium",
    "iot": "Medium",
    "dark-web": "Low",
    "insider-threat": "Medium"
}

def extract_cves(title: str, text: str) -> list:
    """Used to extract the CVES from the title and body using regex"""
    regex = r"CVE-\d{4}-\d{4,7}"
    cves = set(re.findall(regex, title.upper() +' ' + text.upper()))
    return list(cves)

def extract_tags(title: str, text:str, matched_tags: list = []) -> list:
    """Used to extract relevant tags based on predetermined keywords"""
    title = title.lower().split(' ')
    text = text.lower().split(' ')

    for index in range(len(title)):
        title[index] = remove_punctuation(title[index])

    for index in range(len(text)):
        text[index] = remove_punctuation(text[index])

    matched_tags = set(matched_tags)
    for tag, keyword in KEYWORD_MAP.items():
        for word in keyword:
            word 
            if word in text or word in title:
                matched_tags.add(tag.strip())
                break
    return list(matched_tags)

def remove_punctuation(text: str) -> str:
    """Used to remove punctuation from words"""
    translator = str.maketrans("","",string.punctuation)
    return text.translate(translator)

def determine_severity(tags: list, cves: list) -> str:
    """Used to determine severity based on the tags and cves for the given article"""

    order = ['Low', 'Medium', 'High', 'Critical']
    current_tier = 'Low'

    for tag in tags:
        if tag in SEVERITY_MAP:
            current_severity = SEVERITY_MAP[tag]
            if order.index(current_severity) > order.index(current_tier):
                current_tier = current_severity
    
    if cves:
        index = max(order.index(current_tier), order.index('Medium'))
        current_tier = order[index]

        if len(cves) >= 2:
            index = max(order.index(current_tier), order.index('High'))
            current_tier = order[index]
    
    return current_tier