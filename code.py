import os, sys, time, requests, threading, random, re, json, warnings
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class Grad:
    @staticmethod
    def party_mode(): return f"\033[38;2;{random.randint(100,255)};{random.randint(100,255)};{random.randint(100,255)}m"
    @staticmethod
    def hot_gradient(): return "\033[38;5;202m"
RESET = "\033[0m"

class AutoV5:
    def __init__(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{Grad.hot_gradient()}--- VĂN ANH HỮU DUYÊN BL ---{RESET}")
        
        self.api_token = "f7434c18-242e-4fe2-8da0-3e61df7e45b3"
        self.long_url = "https://web-rut-gon.com"
        
        self.earned = 0
        self.used_ips = set()
        self.lock = threading.Lock()
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; K) Chrome/122.0.0.0 Mobile"
        ]

    def rut_gon_link(self):
        """Xử lý bóc tách JSON chuẩn từ API"""
        print(f"{Grad.hot_gradient()}[+] Đang tạo link rút gọn mới...{RESET}")
        try:
            rand_url = f"{self.long_url}?t={random.randint(100000, 999999)}"
            api_url = f"https://vuotnhanh.com/api?api={self.api_token}&url={rand_url}"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                # Phân tích cú pháp JSON thay vì cắt chuỗi thủ công
                data = response.json()
                if data.get("status") == "success":
                    short_link = data.get("shortenedUrl").replace("\\/", "/") # Fix dấu gạch chéo
                    alias = short_link.split('/')[-1]
                    print(f"{Grad.party_mode()}[!] Đã tạo: {short_link} | Alias: {alias}{RESET}")
                    return short_link, alias
                else:
                    print(f"[-] API báo lỗi: {data.get('message')}")
        except Exception as e:
            print(f"[-] Lỗi xử lý JSON: {e}")
        return None, None

    def proxy_free(self):
        sources = [ "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt" ]
        ips = []
        for s in sources:
            try:
                r = requests.get(s, timeout=5)
                ips.extend(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text))
            except: pass
        return list(set(ips))

    def click_worker(self, proxy, target_url, alias):
        try:
            ip = proxy.split(':')[0]
            if ip in self.used_ips: return

            p_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            session = requests.Session()
            session.proxies = p_dict
            session.headers.update({'User-Agent': random.choice(self.ua_list)})

            resp = session.get(target_url, timeout=8, verify=False)
            csrf = re.search(r'name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)', resp.text)
            
            if csrf:
                api_resp = session.post(
                    'https://vuotnhanh.com/go/sf',
                    headers={
                        'X-CSRF-TOKEN': csrf.group(1),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': target_url
                    },
                    data={'alias': alias},
                    timeout=8,
                    verify=False
                )
                
                if api_resp.status_code == 200:
                    res_data = api_resp.json()
                    if res_data.get('status') == 'success':
                        with self.lock:
                            self.earned += 12
                            self.used_ips.add(ip)
                            print(f"{Grad.party_mode()}[SUCCESS] {ip} | +12đ | Tổng: {self.earned}đ{RESET}")
        except: pass

    def run(self):
        while True:
            short_url, alias = self.rut_gon_link()
            if not short_url:
                time.sleep(10)
                continue

            raw_proxies = self.proxy_free()
            random.shuffle(raw_proxies)
            
            print(f"[*] Đang đẩy view cho Alias sạch: {alias}...")
            with ThreadPoolExecutor(max_workers=50) as executor:
                for p in raw_proxies[:150]:
                    executor.submit(self.click_worker, p, short_url, alias)
            
            print(f"{Grad.hot_gradient()}[√] Hoàn thành đợt. Đang làm mới link...{RESET}")
            time.sleep(3)

if __name__ == "__main__":
    try:
        AutoV5().run()
    except KeyboardInterrupt:
        sys.exit()
