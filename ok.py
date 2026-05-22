
import requests, time, random, os, threading
from colorama import init, Fore, Style
from queue import Queue

init(autoreset=True)

def fetch_live_proxies():
    print(Fore.CYAN + "🔄 Mengambil & Testing proxy hidup...")
    urls = [
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/https/data.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt"
    ]
    
    all_proxies = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                all_proxies.extend([line.strip() for line in r.text.splitlines() if line.strip()])
        except:
            pass

    live = []
    test_url = "https://httpbin.org/ip"
    
    print(Fore.YELLOW + "Testing proxy (bisa 20-50 detik)...")
    random.shuffle(all_proxies)
    
    for proxy in all_proxies[:400]:   # test maksimal 400
        try:
            r = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=8)
            if r.status_code == 200:
                live.append(proxy)
                print(f"{Fore.GREEN}[LIVE] {proxy}")
                if len(live) >= 120:      # target 120 proxy hidup
                    break
        except:
            continue
    
    print(Fore.GREEN + f"\n✅ Proxy hidup ditemukan: {len(live)}\n")
    return live

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + """
    ███╗   ██╗ ██████╗ ██╗     ███████╗██████╗  █████╗  ██████╗███████╗
    ████╗  ██║██╔═══██╗██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██╔██╗ ██║██║   ██║██║     █████╗  ██████╔╝███████║██║     █████╗  
    """)
    print(Fore.YELLOW + "          FULL BYPASS NGL SPAMMER\n")

def spam_worker(username, message, queue, success_count, proxies):
    while not queue.empty():
        i = queue.get()
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ]),
            "Accept": "application/json",
            "Origin": "https://ngl.link",
            "Referer": "https://ngl.link/"
        }

        payload = {
            "username": username,
            "question": message,
            "deviceId": f"web-{random.randint(100000000000000,999999999999999)}",
            "gameSlug": "",
            "referrer": ""
        }

        try:
            r = requests.post("https://ngl.link/api/submit", 
                            json=payload, 
                            headers=headers, 
                            proxies=proxy_dict, 
                            timeout=12)
            
            if r.status_code == 200:
                success_count[0] += 1
                print(f"{Fore.GREEN}[✓] {i:3d} | SUCCESS")
            elif r.status_code == 429:
                print(f"{Fore.RED}[!] {i:3d} | Rate Limit")
                time.sleep(3)
            else:
                print(f"{Fore.RED}[✗] {i:3d} | Failed {r.status_code}")
        except:
            print(f"{Fore.YELLOW}[!] {i:3d} | Proxy mati")

        queue.task_done()
        time.sleep(random.uniform(0.8, 2.0))   # delay lebih natural

# ================== MAIN ==================
banner()
proxies = fetch_live_proxies()

if len(proxies) < 10:
    print(Fore.RED + "Proxy hidup terlalu sedikit.")
    exit()

username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah Spam: " + Fore.YELLOW))
threads = int(input(Fore.WHITE + "Thread (5-25): " + Fore.YELLOW) or "15")

print(Fore.MAGENTA + f"\n🚀 Mulai Full Bypass Spam...\n")

queue = Queue()
success = [0]

for i in range(1, amount + 1):
    queue.put(i)

for _ in range(threads):
    t = threading.Thread(target=spam_worker, args=(username, message, queue, success, proxies))
    t.daemon = True
    t.start()

queue.join()

print(Fore.CYAN + f"\n{'='*60}")
print(Fore.GREEN + f"SELESAI! Berhasil Dikirim: {success[0]}/{amount}")
print(Fore.CYAN + f"{'='*60}")
