# MCA Test 

## MCA Overview
MCA는 알리바바에서 제공하는 Anti-DDos Premium 제품의 일부 기능이다. Anti-DDos는 DDos 공격으로 의심되는 트래픽을 사전에 차단하고 완화해주는 Security Service이다. 이 Anti-DDos에는 MCA라는 Mainland China Accelerator라는 기능이 있다. 이 기능을 사용하면 비정상(DDos 공격으로 의심되는) 트래픽은 Anti-DDos instance로 라우팅 되어 scrubbing되고, 정상 트래픽은 MCA instance로 라우팅 되어 중국과 그밖의 지역 간 네트워크 전송속도를 향상 시킨다. 

![](http://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/assets/img/79672/154692909135306_en-US.png)

그림을 보면 Security Traffic Manager(STM)이 그 역할을 하는데 정상트래픽은 MCA accelerate line을, 비정상트래픽은 Anti-DDos scrubbing center로 라우팅하는 역할을 한다. Anti-ddos 설정을 하다보면 Security Traffic Manager의 rule을 생성하고 나오는 CNAME을 DNS record에 추가하는 부분이 있는데, 이 설정을 통해 origin server에 라우팅되는 모든 트래픽이 STM을 먼저 거치게 되는 것이다. 

MCA설정은 알리바바 공식 메뉴얼([https://www.alibabacloud.com/help/doc-detail/92502.htm](https://www.alibabacloud.com/help/doc-detail/92502.htm))을 참고하길 바란다. 
> **Note** 이 문서에서 사용되는 용어는 모두 알리바바 공식 가이드 문서의 English 버전과 알리바바 클라우드 콘솔의 English 버전을 참고한다. 용어에 혼선 없길 바란다.

## MCA Use Cases

Anti DDos 는 본래 DDoS 공격을 완화시키는 Security 제품이지만, 한국의 경우 다음과 같은 사항에 MCA를 고려해 볼 수 있다.
- 한국에 Origin Server가 위치해 있고 중국의 사용자를 대상으로 서비스 하는 경우
- 도메인 이름이 ICP 공식 승인을 받지 않아 (참고: ICP 승인을 받기 위해서는 중국 사업체가 있어야 한다) 중국 사용자의 속도 개선을 위해 CDN이나 GA2.0을 사용할 수 없는 경우
> **Note: CDN, GA2.0 모두 웹사이트를 서비스 하기 위해 중국 내 IP를 사용한다.** **따라서 ICP 자격 대상 중 하나인 "중국내 IP를 사용하여 웹 사이트를 호스팅 하는 경우"에 부합하여 ICP 승인 대상에 포함된다.**

Anti DDos Premium의 MCA는 홍콩 리전의 IP를 할당받기 때문에 ICP 승인 없이도 웹사이트를 가속화할 수 있으며 라우팅 경로를 중국에서 홍콩을 거쳐 한국으로 들어오도록 변경함으로써 속도를 향상시킨다. 아래는 실제 테스트 계정에서 발급받은 MCA 인스턴스 IP와 해당 IP의 geolocation 정보이다. 
![](https://github.com/rnlduaeo/alibaba/blob/master/hk.png?raw=true)

## MCA 설정 시 주의사항
공식 메뉴얼을 참고하는데 주의사항이 있다. 많은 경우에 설정을 잘못하여 MCA가 제대로 동작하지 않는 것을 보았다. 혹시 메뉴얼을 따라 했는 데도 제대로 동작하지 않는 다면 다음과 같은 경우가 아닌지 의심해 볼 필요가 있다.

- 한국에 origin server가 위치한 경우, Anti-DDos Premium 을 선택해야 한다. Anti-DDos Pro는 origin server가 중국에 위치한 경우(도메인을 사용할 경우 ICP인증을 받아야 한다.)에 사용하는 서비스이다. 

- 인스턴스를 2개 구매하여야 한다. 
	- Insurance(또는 Unlimited): Cache기능을 사용하려면 Enhanced, 그렇지 않다면 Standard를 구매하면 된다. Standard를 구매해도 추후에 Enhanced로 업그레이드 가능하다. 다만, 다운그레이드는 불가하니 참고하자.
	- MCA
- Provisioning 메뉴에서 웹사이트를 추가할 때, 위에서 생성한 2개의 인스턴스를 모두 선택해야 한다. 

- **Provisioning 메뉴에서 웹사이트를 추가하고 나온 CNAME은 무시해야 한다. Sec-Traffic Manager에서 rule을 설정하고 나온 CNAME을 DNS 레코드에 추가하여야 한다. (이 부분에서 가장 실수가 많다. 참고하자.)** 

	> Note: Sec-Traffic Manager를 적용하지 않고 Provisioning 메뉴에서 나온 CNAME을 적용할 경우, 도메인 이름으로 요청을 보낼 때 provisioning시 선택한 인스턴스 IP 중 무작위 방식으로 IP가 선택되어 요청이 라우팅되기 때문에 트래픽 전송 라우팅이 예측 불가능하게 된다. 테스트 결과, Anti DDos와 MCA인스턴스 IP가 번갈아가며 선택되어, Anti DDos쪽이 선택되는 경우 전송 속도가 현저히 느리며, MCA쪽이 선택되는 경우 전송 속도가 빠르다. 따라서 Sec-Traffic Manager 설정을 통해 문제가 있는 비정상 트래픽만 Anti DDos로, 문제가 없는 정상 트래픽은 반드시 MCA로 라우팅 될 수 있도록 설정해야 예측 가능한 성능을 보장할 수 있다. 

- '410 Gone' 에러가 나올 경우, 동일 도메인에 여러 CNAME을 중복 적용했을 경우, 또는 동일 CNAME을 여러 도메인에 중복 적용했을 경우에 주어진 도메인 이름으로 타겟 주소를 찾아가지 못하여 발생하는 에러이다. 내 도메인에 MCA cname을 하나만 적용했는지, 다수 적용했는지, 또는 MCA cname을 여러 도메인에 적용하지는 않았는지 확인해 보자. (여러 도메인에 동일 CNAME을 적용하고자 한다면 CNAME reuse를 사용하자, 뒤에서 설명)

- Cache 기능을 사용할 경우 .css, .js, .txt 파일을 제외한 파일의 캐싱일 경우, static page caching을 Enhanced로 해주어야 캐싱된다. (Mitigation Setting > Web acceleration Policies > static page caching (Enhanced))

## Test Overview
Test는 다음과 같이 진행 되었다.

*  Test 기간
	* 2020-01-05 12:00(AM) ~ 2020-01-07 13:00(PM)

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
	* User Agent
		* Chrome 38.0 (Windows)

* Test Object
	* Static content - 500k, 1M, 4M size
	* Dynamic content - php
* Test Groups
	* Direct(MCA 적용 X)
	* AntiDDos(Enhanced) + MCA with Cache function enabled
	* AntiDDos(Standard) + MCA without Cache 
* Test URLs
	* Direct (MCA 적용 X)
		* http://nonmca.haemieee2.xyz/file/500K.png
		* http://nonmca.haemieee2.xyz/file/1M.pdf
		* http://nonmca.haemieee2.xyz/file/4M.pdf
		* http://nonmca.haemieee2.xyz/index.php
		
	* AntiDDos(Enhanced) + MCA with Cache function enabled
		* http://nonmca.haemieee2.xyz/file/500K.png
		* http://nonmca.haemieee2.xyz/file/1M.pdf
		* http://nonmca.haemieee2.xyz/file/4M.pdf
		* http://mca2.haemieee2.xyz/index.php
	
	* AntiDDos(Standard) + MCA without Cache 
		* http://nonmca.haemieee2.xyz/file/500K.png
		* http://nonmca.haemieee2.xyz/file/1M.pdf
		* http://nonmca.haemieee2.xyz/file/4M.pdf
		* http://mca.haemieee2.xyz/index.php
	
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
- User Agent는 Chrome 3.8(Windows)로 한정했다. 브라우저의 경우 브라우저 자체적으로 캐싱이 default로 설정되어 있다. 해당 캐시에 영향을 받지 않기 위해 요청 간격을 5분으로 설정했다.

## Test 결과

 * Ping Test (Beijing > Seoul 왼쪽, Shanghai > Seoul 오른쪽)
		![](https://github.com/rnlduaeo/alibaba/blob/master/pingtime.png?raw=true)
		

아래는 웹 페이지 로딩 속도를 측정한 그래프이다. y축은 요청에 대한 응답시간을 나타내고 x축은 색깔 별로 각각 MCA Cache(연두), MCA NoCache(주황), Public(파랑)망을 나타낸다. 속도는 베이징, 상해에서 서울로 500k, 1M, 4M 페이지에 대한 페이지 로딩 속도를 측정했다. 응답시간이 낮을 수록 로딩 속도가 빠르다는 것을 나타낸다.

* Static Web Object Load (Beijing > Seoul) - 응답시간 추이
![hello](https://github.com/rnlduaeo/alibaba/blob/master/BJ_KR.png?raw=true)

* Static Web Object Load (Shanghai > Seoul) - 응답시간 추이
![](https://github.com/rnlduaeo/alibaba/blob/master/SH_KR.png?raw=true)

* Dynamic Web Object Load (Beijing > Seoul, Shanghai > Seoul) - 응답시간 추이
![](https://github.com/rnlduaeo/alibaba/blob/master/Dynamic.png?raw=true)


## Key Finding
1. Ping Test
![]()
	>Note: Ping Test는 2019-01-06 16:30 ~ 2019-01-07 00:00 까지 약 0시간 진행하였다.
3. Static Web Object Load (Beijing > Seoul)
	- Direct (MCA 적용 X)
 간헐적으로 튀는 현상이 있기는 하지만 대체적으로 일정한 속도가 유지된다.  
	- AntiDDos(Enhanced) + MCA with Cache function enabled
가장 최적의 네트워크 성능을 보여 준다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 9배, 1M의 경우 약 8배, 4M의 경우 약 2배의 응답 시간 개선 효과를 가져왔다. 간헐적으로 튀는 현상이 있지만 대체적으로 Direct 보다 훨씬 큰 폭의 대역폭을 유지한다. 
	- AntiDDos(Standard) + MCA without Cache
평균 응답 시간을 보았을 때 그 개선효과가 Cache 적용보다는 미미하다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 1.7배, 1M의 경우 약 2.68배 개선되었지만 4M의 경우 1.12배 개선되었다. 
4. Static Web Object Load (Shanghai > Seoul)
	- Direct (MCA 적용 X)
 간헐적으로 튀는 현상이 있기는 하지만 대체적으로 일정한 속도가 유지된다.  
	- AntiDDos(Enhanced) + MCA with Cache function enabled
가장 최적의 네트워크 성능을 보여 준다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 7배, 1M의 경우 약 5배, 4M의 경우 약 6배의 응답 시간 개선 효과를 가져왔다. 간헐적으로 튀는 현상이 있지만 대체적으로 Direct 보다 훨씬 큰 폭의 대역폭을 유지한다. 
	- AntiDDos(Standard) + MCA without Cache
평균 응답 시간을 보았을 때 그 개선효과가 미미하다. Direct와 비교했을 때 500k의 오브젝트의 경우 약 1.46배, 1M의 경우 약 1.13배, 4M의 경우 1.06배의 응답시간 개선효과가 있었다. 응답시간은 불 안정적으로 변동폭이 큰 편이다.

5. Dynamic Web Object Load (Beijing > Seoul, Shanghai > Seoul)
리전에 따라 상이한 결과를 보인다. 베이징의 경우 1.8배의 개선 효과가 있었지만, 상하이의 경우 비슷한 속도를 보였다. 

##  시사점

* Anti DDos(Enhanced - Cache function enabled)와 MCA의 조합이 static content에 한하여 가장 최적의 결과를 가져왔다. cache 설정은 아래처럼 각 페이지 URL 별로 설정 가능하다. 

	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-06%20at%208.44.29%20PM.png?raw=true)

	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-06%20at%208.39.08%20PM.png?raw=true)

* MCA 설정은 매우 간단하다. 인스턴스 프로비저닝 및 웹 사이트 설정은 수 분 안에 모두 끝낼 수 있다. 

* CDN을 대체할 만큼 다양한 기능을 보유하고 있지 않다. 가령 http header 설정, rewrite(http->https etc.) 설정 등은 모두 불가하다.

* Dynamic content의 경우 리전에 따라 상이한 결과를 보인다. SH(상하이) 리전에서는 약 2배 정도의 속도 개선 효과가 있었지만 BJ(베이징) 리전에서는 효과가 없었다.  이 부분은 실제 구현된 웹사이트를 바탕으로 중국 전역에서 접속하는 client에 대해 속도를 측정하여야 정확한 결과를 알 수 있을 것 같다.

* Website(http, https) 이외에도 NonWebsite TCP, UDP에 대해서도 MCA 설정이 가능하다. 

* 동일한 서버에서 호스팅되는 여러 도메인을 Anti-DDoS Premium 인스턴스에 추가하려면 CNAME reuse를 신청해야 한다. 이 기능을 사용하면 Anti-DDoS Premium을 한 번만 구성하고 동일한 서버에서 호스팅하는 모든 도메인의 DNS resolution에 동일한 CNAME을 사용할 수 있다.
	> Note: CNAME reuse는 ticket을 생성하여 요청해야 한다.

## MCA 제안 시 주의사항
MCA와 관련된 ICP 관련된 이점 외에도, 게임 패키지, 리소스 패치와 같은 큰 컨텐츠를 중국 유저를 대상으로 제공하는데 큰 역할을 할 수 있다. 그러나 다음과 같은 경우에는  MCA 고려 대상이 아니니 주의하자. 

* 3XX로 리디렉션되는 URL
* 스트리밍 (HLS 없음)
* 복잡한 캐시 설정이 필요한 웹사이트

> Note: Dynamic Contents 의 경우 리전에 따라 상이한 결과를 보이기 때문에 고객의 실제 Website를 바탕으로 한 PoC 결과를 참고하는 것이 좋겠다.




<!--stackedit_data:
eyJoaXN0b3J5IjpbODQwOTQ4MDc4LC0xMDgyNTA0ODUwLC03Mj
A3NzEwMDQsMjM0ODE5ODg2LC04NTU2MDc1MTIsLTEwNTg3OTA1
MTYsLTE1NDY4MTUyMTQsLTE5OTYxNzgyNjgsMjA4MjI0MzMwNy
wtNDExNzM2ODMwLDE1NDgzMzE2MzIsLTE5NzQyNzk4MzYsLTIx
MjQ5Mjg4ODgsLTY5NzkyNzc5MSwtMTE4OTE5MTAzNywtMTc2OT
g1MzkzLC0xMTYzNDU3ODc5LDgyODY3MzAzNSwxMDAyOTY4NjU1
LC01MzAwMzkwXX0=
-->