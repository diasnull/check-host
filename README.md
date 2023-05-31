<p align="center">
	<img src="/assests/check-host.png">
</p>

Check-Host is a utility for monitoring websites and checking the availability of hosts, DNS records and IP addresses. Created based on API: https://check-host.net/about/api

## view:
```
          __           __       __            __ 
     ____/ /  ___ ____/ /______/ /  ___  ___ / /_
    / __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
    \__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v1.2 / https://github.com/diasnull                                  
                        ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ
                        
 iplook: website location search
 usage:
 | python3 check-host.py --iplook -t <target>
 examples:
 | python3 check-host.py --iplook -t 1.1.1.1
 | python3 check-host.py --iplook -t example.com
 only for domain, IP address!

 ping: testing the integrity and quality of connections
 usage:
 | python3 check-host.py --ping -t <target>
 examples:
 | python3 check-host.py --ping -t 1.1.1.1
 | python3 check-host.py --ping -t http://example.com
 | python3 check-host.py --ping -t https://example.com
 | python3 check-host.py --ping -t example.com

 http: testing website availability and performance
 usage:
 | python3 check-host.py --http -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --http -t https://1.1.1.1:443
 | python3 check-host.py --http -t http://example.com
 | python3 check-host.py --http -t https://example.com
 | python3 check-host.py --http -t example.com:80

 tcp: testing TCP connection
 usage:
 | python3 check-host.py --tcp -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --tcp -t 1.1.1.1:53
 | python3 check-host.py --tcp -t http://example.com
 | python3 check-host.py --tcp -t ssmtp://smtp.gmail.com

 udp: testing UDP connection
 usage:
 | python3 check-host.py --udp -t <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py --udp -t 1.1.1.1:53
 | python3 check-host.py --udp -t http://example.com
 | python3 check-host.py --udp -t example.com:4444

 dns: website domain monitoring
 usage:
 | python3 check-host.py --dns -t <target>
 examples:
 | python3 check-host.py --dns -t 1.1.1.1
 | python3 check-host.py --dns -t http://example.com
 | python3 check-host.py --dns -t https://example.com
 | python3 check-host.py --dns -t example.com
```

## methods:
iplook: website location search, IP address<br>
ping: testing the integrity and quality of connections<br>
http: testing website availability and performance<br>
tcp: testing TCP connection<br>
udp: testing UDP connection<br>
dns: website domain monitoring<br>

## requirements:
```
pip3 install requests
```
```
pip3 install prettytable
```

## install:
``` bash
git clone https://github.com/diasnull/check-host.git
cd check-host/
```

## run:
``` bash
python3 check-host.py -h
```


