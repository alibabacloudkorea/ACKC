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

## Key findings
1. Standard Deviation(stdv) standpoint: 
The t1.gg access over internet shows the larger range of fluctuation which is between thousands of ms and over tens of thousands of ms. On the other hand, the access over GA shows a little fluctuation which is at most over 3000 ms. 
2. Average latency standpoint:
The t1.gg access over internet shows that 21.73% of entire measurement is over 1500 ms. On the other hand, the access over GA shows that 99.66% of the entire measurement is below 1350 ms.
3. For more details, see cloud monitor console:
https://cms-intl.console.aliyun.com/?spm=a2c8b.12215442.products-recent.dcms.76393c2ffJRS5i#/newSite/list/

<!--stackedit_data:
eyJoaXN0b3J5IjpbODgxMjgyMDY1LDY1NjEwMjY0MSwtMTYzMT
g4NTMyMywtMTM1MTg1ODg2LC0xOTM1ODUwNzc2LC03NDM2Mzk3
ODUsNzU4MTM1MjQ0LDE0Nzc2MjAyNzEsLTE3OTg3NzMxNTFdfQ
==
-->