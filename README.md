<p align="center">
	<img src="src/assest/check-host.png">
</p>

Check-Host is a utility for monitoring websites and checking the availability of hosts, DNS records and IP addresses. Created based on API: https://check-host.net/about/api

## view:
```
          __           __       __            __ 
     ____/ /  ___ ____/ /______/ /  ___  ___ / /_
    / __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
    \__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v2 / https://github.com/diasnull                                  
                        ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ

	usage:
		python3 check-host.py -m { method } -t { target } -mx { count of nodes }
	example:
		python3 check-host.py -m http -t example.com -mx 3
		python3 check-host.py -m dns -t https://example.com
		python3 check-host.py -m ip-lookup -t example.com

	methods:
		ip-lookup, whois, ping, http, tcp, udp, dns

	accepts:
		ip-lookup -> domain, ip
		whois -> url, domain, ip
		ping -> url, domain, ip
		http -> url, domain, ip
		tcp -> url, domain, ip
		udp -> url, domain, ip
		dns -> url, domain, ip
```

## methods:
ip-lookup: retrieves information about an IP address, including geolocation and owner details;<br>
whois: provides registration details for a domain name;<br>
ping: tests the reachability of a host (layer4);<br>
http: tests the reachability of a host (layer7);<br>
tcp: tests arbitrary TCP port connectivity;<br>
udp: tests arbitrary UDP port connectivity;<br>
dns: queries DNS records for a domain<br>


## requirements:
``` bash
pip3 install -r requirements.txt
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

## showcase:
### method -> ping:
``` bash
>> python3 check-host.py -t example.com -m ping -mx 3

2020-01-01 12:50:01.000001 ping ~ ( info ): runned.
   country       city result             rtt min / avg / max     ip address
0  Germany  Frankfurt    4/4  151.572 / 151.693 / 151.834 ms  23.192.228.80
1    Japan      Tokyo    4/4  103.674 / 104.473 / 105.038 ms   96.7.128.175
2      USA     Dallas    4/4     45.076 / 45.137 / 45.178 ms  23.192.228.84
2020-01-01 12:50:01.000001 ping ~ ( info ): ended.
```
### method -> http:
``` bash
>> python3 check-host.py -t example.com -m http -mx 3

2020-01-01 12:50:01.000001 http ~ ( info ): runned.
  country       city result      time code     ip address
0   Spain  Barcelona     OK  0.327032  200  23.192.228.84
1   Japan      Tokyo     OK  0.226112  200   96.7.128.175
2  Poland     Poznan     OK  0.354360  200   96.7.128.175
2020-01-01 12:50:01.000001 http ~ ( info ): ended.
```
### method -> tcp:
``` bash
>> python3 check-host.py -t example.com -m tcp -mx 3

2020-01-01 12:50:01.000001 tcp ~ ( info ): runned.
  country       city     result      time     ip address
0   Spain  Barcelona  connected  0.182928   96.7.128.198
1    Iran     Tehran  connected  0.244705  23.192.228.80
2  Turkey   Istanbul  connected  0.201446  23.192.228.80
2020-01-01 12:50:01.000001 tcp ~ ( info ): ended.
```
### method -> udp:
``` bash
>> python3 check-host.py -t example.com -m udp -mx 3

2020-01-01 12:50:01.000001 udp ~ ( info ): runned.
   country             city            result     ip address
0   Israel          Netanya  open or filtered   96.7.128.198
1   Poland           Poznan  open or filtered   96.7.128.198
2  Ukraine  SpaceX Starlink  open or filtered  23.192.228.84
2020-01-01 12:50:01.000001 udp ~ ( info ): ended.
```
### method -> dns:
``` bash
>> python3 check-host.py -t example.com -m dns -mx 3

2020-01-01 12:50:01.000001 dns ~ ( info ): runned.
  country      city                                                  a                                               aaaa  ttl
0     UAE     Dubai  [23.215.0.138, 96.7.128.175, 96.7.128.198, 23....  [2600:1406:3a00:21::173e:2e65, 2600:1406:3a00:...  176
1  France     Paris  [23.215.0.138, 96.7.128.175, 96.7.128.198, 23....  [2600:1406:bc00:53::b81e:94c8, 2600:1406:bc00:...   74
2  Turkey  Istanbul  [96.7.128.198, 23.215.0.138, 23.215.0.136, 23....  [2600:1408:ec00:36::1736:7f24, 2600:1406:3a00:...  121
2020-01-01 12:50:01.000001 dns ~ ( info ): ended.
```
### method -> ip-lookup:
``` bash
>> python3 check-host.py -t example.com -m ip-lookup

2020-01-01 12:50:01.000001 ip-lookup ~ ( info ): runned.
           name                              value
0        status                            success
1       country                      United States
2   countryCode                                 US
3        region                                 CA
4    regionName                         California
5          city                        Santa Clara
6           zip                              95052
7           lat                             37.353
8           lon                          -121.9544
9      timezone                America/Los_Angeles
10          isp          Akamai International B.V.
11          org                Akamai Technologies
12           as  AS20940 Akamai International B.V.
13        query       2600:1406:3a00:21::173e:2e65
2020-01-01 12:50:01.000001 ip-lookup ~ ( info ): ended.
```
### method -> whois:
``` bash
>> python3 check-host.py -t example.com -m whois

2020-01-01 12:50:01.000001 whois ~ ( info ): runned.
% IANA WHOIS server
% for more information on IANA, visit http://www.iana.org
% This query returned 1 object

domain:       EXAMPLE.COM

organisation: Internet Assigned Numbers Authority

created:      1992-01-01
source:       IANA


2020-01-01 12:50:01.000001 whois ~ ( info ): ended.
```