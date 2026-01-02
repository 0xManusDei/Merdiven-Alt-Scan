import socket
import threading
from queue import Queue
import time
import sys

# Terminal renkleri
RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def print_banner():
    # Merdiven ve Merdiven Altı Scan yazısı
    banner = f"""
{CYAN}          _
        _|_|_
      _|_|_|_|_
    _|_|_|_|_|_|_
  _|_|_|_|_|_|_|_|_
{RED}    0xManusDei {RESET}| {GREEN}Merdiven Altı Scan{CYAN}
########################################################
#                                                      #
#   {RESET}The Digital Hand in the Machine                    {CYAN}#
#   Hazırsanız Başlıyoruz                              #
#                                                      #
########################################################{RESET}
    """
    print(banner)

def port_scan(target, port, open_ports):
    try:
        # bağlantı seçenekleri ıpv4 ve tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Kapı kapalıysa es geçilir
        sock.settimeout(0.5)
        
        # portlar taranır
        result = sock.connect_ex((target, port))
        if result == 0:
            # açık portlar yakalanır
            print(f"{GREEN}[+] Yakaladık! Port {port} açık.{RESET}")
            open_ports.append(port)
        sock.close()
    except Exception:
        # Bir aksilik olursa görmezden gel, taramaya devam et
        pass

def worker(target, queue, open_ports):
    # bütün portları tara
    while not queue.empty():
        port = queue.get()
        port_scan(target, port, open_ports)
        queue.task_done()

def main():
    print_banner()
    
    try:
        target = input(f"{CYAN} Kime tarama yapıyoruz? (IP/Domain): {RESET}")
        # Yazılan adresi sistemin anlayacağı IP formatına çevirelim
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{RED}[!] Çok zor ya, kontrol edip tekrar dene.{RESET}")
        return

    print(f"\n{CYAN}[*] {target_ip} Hazırsanız Başlıyoruz...")
    print(f"[*] 65.535 portun hepsine bakacağız, sen relax ol...{RESET}\n")

    queue = Queue()
    open_ports = []
    
    # Tüm portları listeye dizelim
    for port in range(1, 65536):
        queue.put(port)

    start_time = time.time()

    # İşi hızlandırmak için 500 koldan (thread) bakıyoruz
    threads = []
    for _ in range(500):
        t = threading.Thread(target=worker, args=(target_ip, queue, open_ports))
        t.daemon = True # Programı kapatırsak bunlar da kapansın
        threads.append(t)
        t.start()

    # Tüm işlerin bitmesini bekle
    queue.join()
    
    end_time = time.time()

    print("\n" + "-" * 45)
    if open_ports:
        print(f"{GREEN}[BİTTİ] Bulduğumuz açık kapılar: {sorted(open_ports)}{RESET}")
    else:
        print(f"{RED}[!] Maalesef, adamın Arrrkası sağlam.{RESET}")
    
    print(f"{CYAN}[*] Bu tarama toplam {round(end_time - start_time, 2)} saniye sürdü.{RESET}")
    print("-" * 45)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C yapılırsa nazikçe veda edelim
        print(f"\n{RED}[!] sıkıntı çıktı, merdiven altından çıkıyoruz!{RESET}")
        sys.exit()