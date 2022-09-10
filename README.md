<p align="center">
	<img src="/image/check-host.png">
</p>

Check-Host is a utility for monitoring websites and checking the availability of hosts, DNS records and IP addresses. Created based on API: https://check-host.net/about/api

## view:
```
	      __           __       __            __ 
	 ____/ /  ___ ____/ /______/ /  ___  ___ / /_
	/ __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
	\__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v1.0 / https://github.com/diasnull
	                    ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ

 iplook: website location search, IP address
 usage:
 | python3 check-host.py iplook <target>
 examples:
 | python3 check-host.py iplook 1.1.1.1
 | python3 check-host.py iplook example.com
 only for domain, IP address!

 ping: checking the integrity and quality of connections
 usage:
 | python3 check-host.py ping <target>
 examples:
 | python3 check-host.py ping 1.1.1.1
 | python3 check-host.py ping http://example.com
 | python3 check-host.py ping https://example.com
 | python3 check-host.py ping example.com 

 http: website availability and performance check
 usage:
 | python3 check-host.py http <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py http https://1.1.1.1:443
 | python3 check-host.py http http://example.com
 | python3 check-host.py http https://example.com
 | python3 check-host.py http example.com:80

 tcp: testing TCP connection of any port of an IP address, website
 usage:
 | python3 check-host.py tcp <target>:<port> <-- automatically port 80
 examples:
 | python3 check-host.py tcp 1.1.1.1:53
 | python3 check-host.py tcp http://example.com
 | python3 check-host.py tcp ssmtp://smtp.gmail.com

 dns: website domain monitoring
 usage:
 | python3 check-host.py dns <target>
 examples:
 | python3 check-host.py dns 1.1.1.1
 | python3 check-host.py dns http://example.com
 | python3 check-host.py dns https://example.com
 | python3 check-host.py dns example.com
```

## methods:
iplook: website location search, IP address<br>
ping: checking the integrity and quality of connections<br>
http: website availability and performance check<br>
tcp: testing TCP connection of any port of an IP address, website<br>
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
python3 check-host.py help
```


