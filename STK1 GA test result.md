# SKT1 Test result

## Test goal
For SKT1 website acceleration from China, we have been testing Alibaba Global Accelerator(GA) by dividing China into 4 quadrant, east/west/north/south and measuring the access latency in order to see the accelerated result.

## Test overview

 * Test period
3 days, 2021/03/05 (Fri) 19:00 - 2021/03/08 (Mon) 16:00
 
 * Test tool and environment
Alibaba Cloud site monitor
For more information on site monitoring, see https://www.alibabacloud.com/help/doc-detail/67907.htm?spm=a2c63.l28256.b99.72.6d2e2129UQNZ3J

 * Test region
China Sichuan > Korea (AWS)
China Beijing > Korea (AWS)
China Shandong > Korea (AWS)
China Shanghai > Korea (AWS)
China Zhejiang > Korea (AWS)

 * Test URLs
	 * Over internet: https://t1.gg
	 * Over GA: https://47.57.4.53

* Test method and measuring metric
	* monitoring type: HTTP(s)
	* Monitoring frequency: 5 minutes
	* didn't set advanced settings which contains request method, match response method, http request header, cookie etc.

* DNS
	* In this test, didn't set a DNS record for the GA accelerated IP (47.57.4.53)
	* In production env, need to set GA accelerated IP (47.57.4.53) for China ISPs through geoDNS or global traffic manager(GTM) in DNS features.
	* For more information on GTM in DNS, see
https://www.alibabacloud.com/help/doc-detail/206111.htm?spm=a2c63.p38356.b99.107.64ef47dba3pK7k

## Test result
* Indicator Trends: can view the trend charts of different metrics.
	1. Indicator trend over **public internet**
![](https://github.com/rnlduaeo/alibaba/blob/master/indicator_trend_internet.png?raw=true)

	2. Indicator trend over **GA**
![](https://github.com/rnlduaeo/alibaba/blob/master/indicator_trend_ga.png?raw=true)

* Operator Trends: can view the trend chars of different carriers.
	1. Operator trends over **public internet**
![](https://github.com/rnlduaeo/alibaba/blob/master/operator_trend_internet.png?raw=true)

	2. Operator trends over **GA**
![](https://github.com/rnlduaeo/alibaba/blob/master/operator_trend_ga.png?raw=true)

** Key findings
1. The t1.gg access over internet shows the larger range of fluctuation which is between thousands of ms to over tends of thousands of ms. On the other hand, 
2. 

<!--stackedit_data:
eyJoaXN0b3J5IjpbMjQ5MzMyOTEsLTEzNTE4NTg4NiwtMTkzNT
g1MDc3NiwtNzQzNjM5Nzg1LDc1ODEzNTI0NCwxNDc3NjIwMjcx
LC0xNzk4NzczMTUxXX0=
-->