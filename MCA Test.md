# MCA Test 

## MCA Overview
MCA는 알리바바에서 제공하는 Anti-DDos Premium 제품의 일부 기능이다. Anti-DDos는 DDos 공격으로 의심되는 트래픽을 사전에 차단하고 완화해주는 Security Service이다. 이 Anti-DDos에는 MCA라는 Mainland China Accelerator라는 기능이 있다. 이 기능을 사용하면 비정상(DDos 공격으로 의심되는) 트래픽은 Anti-DDos instance로 라우팅 되어 scrubbing되고, 정상 트래픽은 MCA instance로 라우팅 되어 중국과 그밖의 지역 간 네트워크 전송속도를 향상 시킨다. 

![](http://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/assets/img/79672/154692909135306_en-US.png)

그림을 보면 Security Traffic Manager(STM)이 그 역할을 하는데 정상트래픽은 MCA accelerate line을, 비정상트래픽은 Anti-DDos scrubbing center로 라우팅하는 역할을 한다. Anti-ddos 설정을 하다보면 Security Traffic Manager의 rule을 생성하고 나오는 CNAME을 DNS record에 추가하는 부분이 있는데, 이 설정을 통해 origin server에 라우팅되는 모든 트래픽이 STM을 먼저 거치게 되는 것이다. 

MCA설정은 알리바바 공식 메뉴얼([https://www.alibabacloud.com/help/doc-detail/92502.htm](https://www.alibabacloud.com/help/doc-detail/92502.htm))을 참고하길 바란다. 
> **Note** 이 문서에서 사용되는 용어는 모두 알리바바 공식 가이드 문서의 English 버전과 알리바바 클라우드 콘솔의 English 버전을 참고합니다. 용어에 혼선 없으시기 바랍니다. 

## MCA 설정 시 주의사항
공식 메뉴얼을 참고하는데 주의사항이 있다. 많은 경우에 설정을 잘못하여 MCA가 제대로 동작하지 않는 것을 보았다. 혹시 메뉴얼을 따라 했는대도 제대로 동작하지 않는 다면 다음과 같은 경우가 아닌지 의심해 볼 필요가 있다.

- 한국에 origin server가 위치한 경우, Anti-DDos Premium 을 선택해야 한다. Anti-DDos Pro는 origin server가 중국에 위치한 경우(도메인을 사용할 경우 ICP인증을 받아야 한다.)에 사용하는 서비스이다. 
- 인스턴스를 2개 구매하여야 한다. 
	- Insurance(또는 Unlimited): Cache기능을 사용하려면 Enhanced, 그렇지 않다면 Standard를 구매하면 된다. Standard를 구매해도 추후에 Enhanced로 업그레이드 가능하다. 다만, 다운그레이드는 불가하니 참고하자.
	- MCA
- Provisioning 메뉴에서 웹사이트를 추가할 때, 위에서 생성한 2개의 인스턴스를 모두 선택해야 한다. 
- **Provisioning 메뉴에서 웹사이트를 추가하고 나온 CNAME은 무시해야 한다. Sec-Traffic Manager에서 rule을 설정하고 나온 CNAME을 DNS 레코드에 추가하여야 한다. (이 부분에서 가장 실수가 많다. 참고하자.)** Sec-Traffic Manager를 적용하지 않고 Provisioning 메뉴에서 나온 CNAME을 적용할 경우, 도메인 이름으로 요청을 보낼 때 provisioning시 선택한 인스턴스 IP 중 무작위 방식으로 IP가 선택되어 요청이 라우팅되기 때문에 트래픽 전송 라우팅이 예측 불가능하게 된다. 테스트 결과, Anti DDos와 MCA인스턴스 IP가 번갈아가며 선택되어, Anti DDos쪽이 선택되는 경우 전송 속도가 현저히 느리며, MCA쪽이 선택되는 경우 전송 속도가 빠르다. 따라서 Sec-Traffic Manager 설정을 통해 문제가 있는 비정상 트래픽만 Anti DDos로, 문제가 없는 정상 트래픽은 반드시 MCA로 라우팅 될 수 있도록 설정해야 예측 가능한 성능을 보장할 수 있다. 
- '410 Gone' 에러가 나올 경우, 동일 도메인에 여러 CNAME을 중복 적용했을 경우, 또는 동일 CNAME을 여러 도메인에 중복 적용했을 경우에 주어진 도메인 이름으로 타겟 주소를 찾아가지 못하여 발생하는 에러이다. 내 도메인에 MCA cname을 하나만 적용했는지, 다수 적용했는지, 또는 MCA cname을 여러 도메인에 적용하지는 않았는지 확인해 보자. 
- Cache 기능을 사용할 경우 .css, .js, .txt 파일을 제외한 파일의 캐싱일 경우, static page caching을 Enhanced로 해주어야 캐싱된다. (Mitigation Setting > Web acceleration Policies > static page caching (Enhanced))

## Test Overview
Test는 다음과 같이 진행 되었다.

*  Test 기간
	* 2020-01-04 12:00(PM) ~ 2020-01-06 12:00(PM)

*  Test Region
	* Beijing -> Seoul(목동 KT IDC)
	* Shanghai -> Seoul(목동 KT IDC)
	
* Test 방법 및 측정 Metric
	* Ping Test
		* avg pingtime(s)
		* pingloss-%
	* Web object load 
		* DownloadSpeed(MBps)
		* ResponseTime(s)
* Test Object
	* Static content - 500k, 1M, 4M size
	* Dynamic content - php
* Test Groups
	* Direct(MCA 적용 X)
	* AntiDDos(Enhanced) + MCA with Cache function enabled
	* AntiDDos(Standard) + MCA without Cache 
* Test URLs
	* Direct (MCA 적용 X)
	http://nonmca.haemieee2.xyz/file/1M.zip
	http://nonmca.haemieee2.xyz/file/500k.pdf
	http://nonmca.haemieee2.xyz/file/4.5M.sea
	http://nonmca.haemieee2.xyz/index.php
	* AntiDDos(Enhanced) + MCA with Cache function enabled
	http://mca2.haemieee2.xyz/file/1M.zip
	http://mca2.haemieee2.xyz/file/500k.pdf
	http://mca2.haemieee2.xyz/file/4.5M.sea
	http://mca2.haemieee2.xyz/index.php
	* AntiDDos(Standard) + MCA without Cache 
	http://mca.haemieee2.xyz/file/1M.zip
	http://mca.haemieee2.xyz/file/500k.pdf
	http://mca.haemieee2.xyz/file/4.5M.sea
	http://mca.haemieee2.xyz/index.php
	
* DNS 관리
	* Alibaba Cloud (International) DNS 사용, ICP 적용되지 않은 도메인 사용
* Test 도구 및 환경
	* Zabbix(Open source monitoring tool) 및 manual curl command
	* Zabbix master server 홍콩에 위치, agent 서버는 각각 Beijing과 Shanghai 위치
* 테스트 목표
	* MCA 적용 시 네트워크 성능 개선 여부 확인
	* 중국의 여러 리전(본 테스트에는 BJ, SH로 한정) 별로 MCA 적용 여부에 따른 네트워크 성능 확인
	* 시나리오 별 가장 적합한 인스턴스 조합 확인
	* 네트워크 성능 안전성 확인

## Assumptions

## Test 결과

 * Ping Test (Beijing > Seoul, Shanghai > Seoul)
![](https://github.com/rnlduaeo/alibaba/blob/master/PingTest.png?raw=true)
	 * Beijing > Seoul
    
	| <center>--</center> | <center>last</center> | <center>min</center> | <center>avg</center> | <center>max</center> | 
	|:--------|:--------:|--------:| --------:| --------:|
	| **pingtime (BJ > KR)** | <center>0.0367 </center> |0.0366 |0.0373 |<center>0.1504</center> | <center>cell 2x2 </center> |*cell 2x3* | |**cell 3x1** | <center>cell 3x2 </center> |*cell 3x3* |
	| **pingloss-% (BJ > KR)** | <center>0</center> |<center>0.0236</center>| <center>33.33</center>|<center>0</center> | <center>cell 2x2 </center> |*cell 2x3* | |**cell 3x1** | <center>cell 3x2 </center> |*cell 3x3* |

	*Shanghai > Seoul 
	| <center>--</center> | <center>last</center> | <center>min</center> | <center>avg</center> | <center>max</center> | 
	|:--------|:--------:|--------:| --------:| --------:|
	| **pingtime (SH > KR)** | <center>0.0367 </center> |0.0366 |0.0373 |<center>0.152</center> | <center>cell 2x2 </center> |*cell 2x3* | |**cell 3x1** | <center>cell 3x2 </center> |*cell 3x3* |
	| **pingloss-% (SH > KR)** | <center>0</center> |<center>0.0236</center>| <center>33.33</center>|<center>0</center> | <center>cell 2x2 </center> |*cell 2x3* | |**cell 3x1** | <center>cell 3x2 </center> |*cell 3x3* |


* Static Web Object Load (Beijing > Seoul)
![hello](https://github.com/rnlduaeo/alibaba/blob/master/BJ_KR_WebStatic.png?raw=true)

* Static Web Object Load (Shanghai > Seoul)
![](https://github.com/rnlduaeo/alibaba/blob/master/SH_KR_WebStatic.png?raw=true)

* Dynamic Web Object Load (Beijing > Seoul, Shanghai > Seoul)
![](https://github.com/rnlduaeo/alibaba/blob/master/WebDynamic.png?raw=true)


## Key Finding
1. Ping Test
2. Static Web Object Load (Beijing > Seoul)
	- Direct (MCA 적용 X)
 간헐적으로 튀는 현상이 있기는 하지만 대체적으로 일정한 속도가 유지된다.  
	- AntiDDos(Enhanced) + MCA with Cache function enabled
가장 최적의 네트워크 성능을 보여 준다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 9배, 1M의 경우 약 8배, 4M의 경우 약 2배의 응답 시간 개선 효과를 가져왔다. 응답 시간도 튀는 현상 없이 안정적으로 유지된다. 
	- AntiDDos(Standard) + MCA without Cache
평균 응답 시간을 보았을 때 그 개선효과가 미미하다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 1.3배, 1M의 경우 약 1.7배 개선되었지만 4M의 경우 오히려 0.9배로 미 적용시보다 약간 느려지는 결과를 보였다. 응답시간은 불 안정적으로 변동폭이 큰 편이다. 
3. Static Web Object Load (Shanghai > Seoul)
	- Direct (MCA 적용 X)
 간헐적으로 튀는 현상이 있기는 하지만 대체적으로 일정한 속도가 유지된다.  
	- AntiDDos(Enhanced) + MCA with Cache function enabled
가장 최적의 네트워크 성능을 보여 준다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 7배, 1M의 경우 약 5배, 4M의 경우 약 6배의 응답 시간 개선 효과를 가져왔다. 간헐적으로 튀는 현상이 있으나 대체적으로 응답시간이 안정적으로 유지된다. 
	- AntiDDos(Standard) + MCA without Cache
평균 응답 시간을 보았을 때 그 개선효과가 미미하다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 1.46배, 1M의 경우 약 1.13배, 4M의 경우 1.06배의 응답시간 개선효과가 있었다. 
5. Dynamic Web Object Load (Beijing > Seoul)
6. Dynamic Web Object Load (Shanghai > Seoul)

##  시사점

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2MzU0MzEyMzIsLTE4MDQ3MDcwNDYsMT
kzMzAwMTIxMyw4NDE4NTU4MTYsLTg3NzcwNjM2MywtOTEwODM1
MDY0LDEyNjg1NDA5NDcsLTEyMDA3MDI4NjIsLTExMTI5OTE4Nz
MsLTE1NTQwNzM5MzAsODE5MTgzMzcwLC0xNjcwMDM4NTYyLC0x
ODA3NDM5MzYwLC05NzU1NTM4OTUsMTgxMTAxMTk1NSw1OTAwMj
IxMzEsOTE2MTY2Nzg5LC03MTMyNTgyMDQsMjA4OTM3Njg3Myw0
NjA1MTU4NzJdfQ==
-->