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
