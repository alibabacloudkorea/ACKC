
# 한중간 네트워크 가속화 총정리

## 중국 사용자들이 겪는 문제점
중국을 차치하고 생각하면, 일반적인 웹사이트의 성능은 글로벌(중국 외) 평균 2-8초 사이에 페이지가 로딩되는 것으로 확인됩니다. 그러나 중국에서의 글로벌 웹페이지의 페이지 로딩 속도, 또는 인터넷을 통한 서비스 사용 속도는 최대 4-5분이 걸리는 것으로 확인되었고 이는 전자에 비해 10배나 큰 수치입니다. 
중국에서 웹사이트 성능이 현격히 저하되는 이유는 여러가지가 있습니다.

**1) 국경간 불안정한 네트워크**

대부분의 고객들은 중국 밖(한국)에 서버를 두고 중국 내 사용자들에게 서비스하는 경우가 많습니다. 이 경우, 사용자 경험은 중국과 중국밖을 오가는 국경간 인터넷 네트워크의 영향을 크게 받습니다. 사용자와 서버 간 거리 자체가 멀기 때문에 *latency도 크고, 다수 사용자들이 공용으로 사용하는 인터넷의 특성상 인터넷 혼잡도(병목현상)에 의한 packet loss, network jitter 등으로 인해 사용자 경험이 크게 저하됩니다.

**2) 중국 내 불안정한 네트워크**

일부 고객의 경우 중국 내 서버를 두고 정식적으로 ICP filling domain을 발급받아 서비스하는 경우에도, 중국 내 불안정한 네트워크로 인해 속도 이슈를 겪습니다. 중국은 나라 자체도 크고 인구도 많아 지역을 크게 동서남북으로 나누어 다른 통신사업체들(차이나 텔레콤, 차이나 유니콤, 차이나 모바일 등)이 나누어서 관리합니다. 이때 사용자 위치에 따라 여러 통신사업체 망을 걸쳐 네트워크 경로가 형성되는 경우, 라우팅이 최적화되지 않아 속도 이슈를 야기할 수 있습니다.

**3) GFW에 의한 차단되는 컨텐츠**

국경간 네트워크를 오가는 트래픽에 관한 규제입니다. 중국 내에서는 구글, 페이스북을 비롯한 여러 컨텐츠가 아예 차단되어 있고 한국 몇몇 사이트도 사이트 전체 또는 일부가 접속 불가한 경우가 있습니다. 웹사이트에 검열되는 컨텐츠(댓글, 동영상 등)가 포함되어 있다면 해당 object들로 인해 사이트 자체가 느려질 수 있습니다.


*latency: 지연시간, 일반적으로 데이터가 목적지에 도착했다가 다시 돌아 오는 데 걸리는 시간으로 측정하고 거리에 비례하여 증가합니다.
## 중국 비즈니스를 위해 알아야 할 사항들
1) ICP 비안 도메인

	중국 내 온라인(인터넷)을 통한 비즈니스를 운영할 시 필요한 절차입니다. 중국 내에 IT 리소스 (서버, IP, CDN 등)를 사용하여 **도메인**을 통해 인터넷으로 서비스를 한다면 ICP 비안 도메인은 반드시 필요합니다. 
ICP 도메인 발급은 알리바바 클라우드 콘솔을 통해 직접 신청하거나 대행업체 (알리바바 클라우드 파트너사들)을 통해 발급이 가능합니다.

2) GFW(Great Firewall)
	- 대상: Border Network(중국-중국외지역)를 경유하는 모든 public traffic(port)에 대한 규제입니다. 
	- 방법: 알려진 바로는 키워드 필터링, IP 주소 블랙리스트, DNS poisioning, 패킷 검사 등을 통해 컨텐츠를 검열합니다.
	
3) CSL 2.0(China Security Law) 또는 MLPS2.0(China’s Multi-Level Protection Scheme)

	중국에서 비즈니스를 하려면 반드시 지켜야 하는 중국 네트워크 보안법으로 중국 내 발생한 데이터에 대한 해외반출 절차, 개인정보 보호, 중요한 데이터에 대한 유출 방지 등에 대한 상세한 보안규제 요구사항을 담고 있습니다. 

4) 그외 산업별 규제

	게임 서비스에 필요한 판호(게임·서적 등 출판물이 중국 내에서 서비스할 수 있도록 허가해주는 일종의 고유번호) 등 산업별 규제 사항은 따로 확인해주셔야 합니다. 

## 시나리오에 따른 가속화 방안
그럼 본격적으로 시나리오에 따른 가속화 방안을 알아보겠습니다. 웹사이트도 사내용인지(특정 다수 대상), 불특정 다수를 대상으로 하는 웹사이트인지, 자체 운영지 아닌지 등 다양한 조건에 따라 가속화 방안이 달라집니다. 자세한 사항은 아래 다이어그램을 참고하여 현재 조건에 맞는 가속화 방안을 참고해 주시기 바랍니다. 

![](https://github.com/rnlduaeo/alibaba/blob/master/networkdiagram.png?raw=true)

### 불특정 다수를 대상으로 하는 서비스를 자체운영하면서 ICP 도메인을 가지고 정식으로 운영하는 사이트인 경우 (1~4번)

**1. [GA(Global Accelerator)](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.p38356.b99.5.1d21c2426A4UJm)** 
- 소개: 
GA는 사용자와 가장 가까운 access point로부터 origin 서버까지 알리바바 클라우드의 글로벌 백본망으로 연결하여 기존 인터넷 망에 비해 안정적이고 빠른 성능을 가져다 주는 네트워크 가속화 솔루션입니다. 사용자는 origin 서버의 IP나 도메인, 포트, 프로토콜(tcp, udp, http, https)를 등록하여 통신을 가속화할 수 있습니다. pay by traffic, pay by bandwidth 두 가지 형태로 과금됩니다.
- [사용 시나리오](https://www.alibabacloud.com/help/doc-detail/153191.htm?spm=a2c63.l28256.b99.7.16d26796BlZ3CV):
API요청/결과값 반환 처럼 작은 패킷이 오고 가는 통신을 가속화하는데에는 적합합니다. 가령, FPS, 실시간 대전류처럼 지연시간에 민감한 게임 서비스에 GA를 적용할 수 있습니다. 
- 고려 사항: 
GA(2021.06기준)는 한 사용자가 사용할 수 있는 대역폭이 정해져 있습니다. 따라서, 동시접속자들이 많고 트래픽이 폭팔적으로 증가하여 큰 대역폭이 확보되어야 하는 인터넷 서비스의 경우 부적합합니다. 

	GA에 대한 자세한 사항은 [GA 공식 페이지](https://www.alibabacloud.com/help/product/55629.htm?spm=a2c63.m28257.a1.89.65375922PzfQDh)를 확인해 주세요.


**2. (D)CDN:**
- 소개: 
CDN은 중국을 포함한 전 세계에 위치해 있는 알리바바의 CDN edge node들을 통해 사용자 가장 가까이 위치한 edge node에 static contents를 캐싱함으로써 웹 사이트 컨텐츠를 빠르게 전송할 수 있는 서비스입니다. 
ICP 비안이 등록된 도메인의 경우에 한하여, CDN의 mainland China(중국 내 edge) 노드를 사용하여 컨텐츠를 가속화할 수 있습니다.
API 통신, websocket 통신 처럼 캐싱할 수 없는 컨텐츠의 경우에는 DCDN(Dynamic CDN)이라고 하는 별도의 서비스를 사용하여 클라이언트-서버 간 통신 속도를 개선할 수 있습니다.
- 고려사항:
중국 내 CDN의 edge 노드를 사용하려면 반드시 ICP 비안을 발급받은 도메인이 있어야 합니다. 

	(D)CDN에 대한 자세한 사항은 [CDN 공식페이지](https://www.alibabacloud.com/help/product/27099.htm?spm=a2c63.m28257.a1.92.65375922agGuYa) 와 [DCDN 공식페이지](https://www.alibabacloud.com/help/product/64812.htm?spm=a2c63.m28257.a1.93.65375922hLueF1)를 확인해 주세요.

**3. GA + CDN**
- 소개: 위의 두가지 서비스를 합쳐 각 서비스의 한계를 상호보완할 수 있습니다. 
중국 내 CDN edge node를 사용하여 컨텐츠를 캐싱하더라도 오리진 서버는 중국 외 지역에 위치하기 때문에 국경 간 네트워크를 필터링하는 GFW 에 의해 오리진으로 부터 컨텐츠를 받아오지 못할 수 있습니다. (CDN에서 504 error 발생) 이때, CDN와 오리진 서버간 GA를 설정하여 알리바바 백본망을 타게 함으로써 이 문제를 해결할 수 있습니다.
또는, 중국 내 CDN edge 노드를 사용하더라도 CDN L2 node(서버와 가까이 위치한 CDN노드)와 오리진 서버간 인터넷 네트워크의 불안정성으로 인해 속도 저하가 있을 수 있습니다. 이 경우에도 CDN과 GA를 함께 사용하여 문제를 해결할 수 있습니다. 
- 다이어그램:
![](https://github.com/rnlduaeo/alibaba/blob/master/CDNGA.png?raw=true)


	[CDN+GA의 자세한 설정 절차](https://www.alibabacloud.com/help/doc-detail/176807.htm?spm=a2c63.p38356.b99.79.163d77006NSBRv)를 클릭하여 자세한 내용을 확인하시기 바랍니다.
	
- 고려사항: 
CDN과 GA 두 개의 서비스가 들어가기 때문에 비용이 증가합니다.
또한, CDN과 오리진 서버 간 트래픽이 증가함에 따라 GA가 병목구간이 될 수 있습니다. pay by traffic을 통한 과금을 선택하더라도 내부적으로 대역폭 할당에 제한을 걸어 놓기 때문에, 미리 그 제한을 풀어 병목현상의 위험을 줄여야 합니다.  

**4. Chinafy**
- 소개: 
Chinafy는 알리바바 클라우드의 파트너 솔루션으로 동일한 웹사이트의 중국 버전을 생성하여 중국 사용자로 하여금 속도 개선 효과를 가져다 주는 솔루션입니다. 
웹사이트의 url만 Chinafy 팀에게 전달해주면 Chinafy팀은 기존 사이트를 기반으로 웹 사이트와 웹 애플리케이션을 중국에 맞게 재 설계합니다. 고객이 해당 솔루션을 채택할 경우, DNS 레코드 변경(Chinafy 에서 제공해주는 cname으로 dns record 변경, 또는 고객이 사용하는 DNS의 지역기반 라우팅 기능을 사용해도 됨)을 통해 기존 사이트와 통합합니다. 
Chinafy는 웹사이트에 포함된 다양한 3rd party component(비콘, 구글맵, 동영상 등)을 중국 내에서 성능저하 없이 수용할 수 있는 형태로 변경하는 등 중국에 맞는 최적화 작업을 수행합니다.

- 고려사항: 
Chinafy는 대부분 static contents에 한하여 가속화합니다. 따라서 동적 요청의 경우 [GA](https://www.alibabacloud.com/help/product/55629.htm?spm=a2c63.m28257.a1.89.65375922PzfQDh)나 [DCDN](https://www.alibabacloud.com/help/product/64812.htm?spm=a2c63.m28257.a1.93.65375922hLueF1)을 통해 보완해야 합니다. 

	자세한 사항은 [알리바바 클라우드 마켓플레이스의 Chinafy](https://marketplace.alibabacloud.com/products?keywords=chinafy&pageIndex=1)페이지를 확인하시기 바랍니다.

### 불특정 다수를 대상으로 하는 서비스 중 자체운영하면서 ICP 비안 도메인을 가지고 있지 않은 경우, 또는 비안 발급이 빠른 시일 내에 예정되어 있지 않은 경우 (6~7번)

**6. GA**
- 소개

	[GA](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.p38356.b99.5.1d21c2427iMI9g)에 대한 자세한 사항은 위의 1번 설명을 참고하시기 바랍니다. 6번의 경우 ICP 비안을 받은 도메인이 없기 때문에 중국내 가속화 IP를 사용할 수 없습니다. 대신, 홍콩의 가속화 IP를 경유하여 네트워크 속도 및 품질을 개선할 수 있습니다. 

	자세한 사항은 [GA 설정 가이드](https://www.alibabacloud.com/help/doc-detail/155066.htm?spm=a2c63.p38356.b99.17.166c2e243Uwsg1)를 참조해 주시기 바랍니다.

- 고려사항

	국경간 인터넷 네트워크를 거치기 때문에 GFW로 인해 컨텐츠가 차단될 수 있습니다. 이를 해결하려면 정식적인 절차, 즉  ICP비안 발급을 고려해 주셔야 합니다.

**7. Chinafy**
- 소개


	[Chinafy](https://marketplace.alibabacloud.com/products?keywords=chinafy&pageIndex=1)는 ICP 발급받지 않은 도메인도 가속화할 수 있습니다. 자세한 사항은 4번 설명을 참조해 주시기 바랍니다.

- 고려사항


	7번 또한 국경간 인터넷 네트워크를 거치기 때문에 GFW로 인해 컨텐츠가 차단될 수 있습니다. 이를 해결하려면 정식적으로 ICP비안 도메인을 발급받아야 합니다.

### 특정 다수를 대상으로 하는 서비스 중 자체 운영하는 웹사이트를 사내망을 통해 접속해야 하는 경우 (9~10번)
**9. VPN + GA**
기존에 사용하던 VPN 장비가 있으면 GA와 연동하여 가속화할 수 있습니다. 
1) VPN 장비 설정에서 NAT-T(Nat Traversal)기능을 enable
2) GA 설정에서 나온 accelerated IP와 endpoint ip를 각 장비의 remote gateway IP로 설정 (endpoint group ip가 4개가 나오기 때문에 하나의 IP로 합치는 작업 필요, 알리바바 클라우드 백앤드 작업 필요)
3) IPSec connection 설정 시 passive mode로 터널링

	![](https://github.com/rnlduaeo/alibaba/blob/master/GAIpSecVPN1.png?raw=true)

**10. SAG + CEN**

SAG는 알리바바 클라우드의 SDWAN 솔루션으로 알리바바의 글로벌 백본망을 기반으로 암호화된 레이어(VPN)를 구성하여 안정적이고 빠른 사내망 구축을 돕는 서비스입니다. 일반 VPN이 인터넷 공용망을 기반으로 하여 많은 성능 이슈를 겪는 반면, SAG는 한중간 VPN을 구성하더라도 속도나 끊김 문제 없이 안정적인 성능을 제공합니다. 
중국 내 사무실 또는 지점에 [SAG device(하드웨어)](https://www.alibabacloud.com/help/doc-detail/69232.htm?spm=a2c63.p38356.b99.123.41dd3527CdLSL3)나  [vCPE(서버 설치용 소프트웨어)](https://www.alibabacloud.com/help/doc-detail/182147.htm?spm=a2c63.p38356.b99.134.ee94513afzkjLn)를 설치하여 운영하거나, 사용자 단말기(모바일, PC)에 [SAG app](https://www.alibabacloud.com/help/doc-detail/108541.htm?spm=a2c63.p38356.b99.139.a2365d49pVQD5E)을 설치하여 가속화할 수 있습니다.
![](https://github.com/rnlduaeo/alibaba/blob/master/sagDiagram.png?raw=true)

> 선택 시 고려사항: 
9번(GA+VPN)은 기본 장비를 그대로 활용할 수 있는 반면, 문제 발생 시 GA와 VPN의 통합 모니터링이 불가하여 원인 분석을 위한 모니터링/로그를 각각 봐야합니다.
10번(SAG+CEN)은 하드웨어나, 서버 설치용 SW를 새로 구성해야하지만 , SAG 단일 콘솔에서 장비/트래픽에 대한 통합 모니터링 및 알람 설정이 가능하고 QoS(애플리케이션에 따른 대역폭 throttling 설정), 장비 및 link 단의 HA 구성 등 SAG의 장점을 누릴 수 있습니다.

### 특정 다수를 대상으로 하는 서비스를 자체운영하면서 사내망을 사용하지 않는 경우 (12~13번)
이 경우는 ICP비안을 발급받은 도메인이 없다는 가정을 전제로 합니다. 
> Note: 만약 ICP비안 도메인을 가지고 있다면(또는 발급 받는다면) GA에서 중국을 가속화 지역으로 설정하고 나온 중국지역의 가속화 IP를 DNS에 연결하여 바로 연결을 가속화할 수 있습니다. 

12. GA(중국 가속화 IP사용) + pac
소개:
	
	사용자 PC나 모바일 단말기의 OS나 브라우저에 pac을 설정하여 웹사이트 도메인에 대한 라우팅 경로를 임의로 바꿔주는 설정입니다. 웹사이트의 도메인이 ICP 비안을 발급받지 않았기 때문에 중국내 가속화 IP와 도메인을 DNS서버에 연결할 수 없습니다. 대신, client단에서 pac file이 위치한 OSS url만 설정해 주면 웹서버로 가는 경로가 중국과 한국을 다이렉트로 연결하는 알리바바 글로벌 네트워크로 변경되면서 속도가 가속화됩니다. 

	다이어그램:
		
	![](https://github.com/rnlduaeo/alibaba/blob/master/GApac.png?raw=true)

13. GA(홍콩 가속화 IP사용)
소개: 

	12번처럼 client 에 무언가를 설정하는게 번거롭다면 GA 설정에서 홍콩을 가속화 지역으로 설정하고 나온 홍콩 가속화 IP를 DNS에 연결하여 사용자단의 변경 없이 연결을 가속화할 수 있습니다. 다만, 중국과 한국을 다이렉트로 연결하는 구성이 아니기 때문에 가속 효과는 12번보다 떨어집니다. 
	
	다이어그램: 

	![](https://github.com/rnlduaeo/alibaba/blob/master/GAHK.png?raw=true)

### 특정 다수를 대상으로 하는 서비스를 자체운영하지 않고 SaaS와 같은 3rd party platform을 사용하는 경우 (14번)
MS office 365, MS teams, Salesforce, Google drive, Dropbox 처럼 사내 직원들 간 협업과 업무를 위해 사용되는 SaaS 애플리케이션을 가속화는 경우입니다. 
고객이 인프라를 직접 관리하는 것이 아니기 때문에 반드시 VPN이나 SDWAN, pac등 client 단의 설정이 추가되어 전체 네트워크 경로를 변경하여야 합니다. 
#### <한국 고객을 위한 SaaS 서버가 "한국"에 위치해 있는 경우>
MS teams 처럼 한국에 서버를 두고 운영하는 SaaS의 경우 아래의 다이어그램과 [구성을 위한 가이드 문서](https://github.com/rnlduaeo/alibaba/blob/master/SaaS%20acceleration%20for%20Korea.md)를 참고하시기 바랍니다.

데이터 플로우:
![](https://github.com/rnlduaeo/alibaba/raw/master/Screen%20Shot%202021-02-16%20at%2011.04.06%20AM.png?raw=true)


#### <한국 고객을 위한 SaaS 서버가 "일본"에 위치해 있는 경우>
Salesforce의 경우 한국 고객들은 일본 서버를 사용하기 때문에 알리바바 클라우드 일본리전을 끝지점으로 사용하여 가속화할 수 있습니다. 
고객의 편의 및 기호에 따라 아래 여러가지 옵션 중 선택하여 적용할 수 있습니다.

1) 접속 지점:
	- pac only : 
	사용자 PC 및 모바일 단말기 OS나 브라우저에 pac file이 위치한 url만 넣어주면 됩니다. 간단한 설정입니다.
	- fortigate ssl vpn client + pac : 
	Fortigate proxy를 사용할 경우 fortigate에서 제공하는 ssl vpn client을 다운받아 설치할 수 있습니다. 이 경우, client부터 프록시 서버까지 암호화되기 때문에 보안이 강화됩니다. 
	- [SAG(Smart Access Gateway)](https://www.alibabacloud.com/help/doc-detail/69227.htm?spm=a2c63.l28256.b99.7.399c149c9DABNd) :
	알리바바 클라우드의 SDWAN 솔루션으로 속도와 안정성을 보장하는 VPN망을 제공합니다. 
		- [SAG 하드웨어 디바이스](https://www.alibabacloud.com/help/doc-detail/69232.htm?spm=a2c63.l28256.b99.123.8f78149cxlN6Ak): 사무실이나 지점에 wifi device처럼 설치하는 SDWAN 디바이스입니다. 사용자 단말기의 변경을 원하지 않는 경우, 하드웨어 디바이스를 선택하면 됩니다. 
		- [SAG 서버 설치용 소프트웨어](https://www.alibabacloud.com/help/doc-detail/182147.htm?spm=a2c63.p38356.b99.134.4493513anwLHw1): SAG 하드웨어 디바이스와 동일한 기능을 제공하는 서버 설치용 소프트웨어입니다. 사무실이나 지점에 남는 서버가 있으면 해당 라이센스 비용을 지불하고 설치해서 사용할 수 있습니다. 
		- [SAG 애플리케이션 - PC, mobile 설치용](https://www.alibabacloud.com/help/doc-detail/108541.htm?spm=a2c63.p38356.b99.139.30ad5d49EA0ydL): 사용자 단말기에 설치할 수 있는 client 소프트웨어입니다. 


2) 프록시 서버:
	- [Fortigate proxy server](https://marketplace.alibabacloud.com/products/56700005/Fortinet_em_FortiGate_em_PAYG_Next_Generation_Firewall_2_vCPUs_-sgcmjj00024896.html?spm=a3c0i.730005.0.0.5a6a2faaEIhW61&innerSource=search_fortigate): 상용 프록시 서버로 fortigate의 기술 지원을 받을 수 있습니다. 또한 office365, salesforce, google, dropbox 등 여럿 SaaS 애플리케이션에 대해 지역에 따라 SaaS 도메인에 해당하는 서버 IP를 자동으로 식별하고 업데이트 할 수 있습니다. 
	- [nginx forward proxy](https://www.alibabacloud.com/blog/how-to-use-nginx-as-an-https-forward-proxy-server_595799#): nginx는 보통 reverse proxy로 많이 사용 되지만, forward proxy로도 사용 가능합니다. 
	- squid proxy: nginx와 마찬가지로 오픈소스 forward proxy입니다. fortigate처럼 프록시 자체에 대한 기술지원은 받을 수 없지만 간단하게 설치 및 사용이 가능한 솔루션입니다. 

솔루션은 총 3가지로 정리됩니다. 

1) GA + fortinet proxy
	- 데이터 플로우: 
	![](https://github.com/rnlduaeo/alibaba/blob/master/fortigate.png?raw=true)
	- 견적: 
		- [GA(basic + crossborder, instance)](https://www.alibabacloud.com/help/doc-detail/153194.htm?spm=a2c63.l28256.b99.10.293867965t46Ra)
		- fortinet marketplace image: [구식(obsolete)](https://marketplace.alibabacloud.com/products/56700005/Fortinet_FortiGate_PAYG_NGFW_HA_Supported_-sgcmjj024463.html)은 444.8 usd/month
	[신식(new generation)](https://marketplace.alibabacloud.com/products/56700005/Fortinet_em_FortiGate_em_PAYG_Next_Generation_Firewall_2_vCPUs_-sgcmjj00024896.html?spm=a3c0i.730005.0.0.5a6a2faahXG6LY&innerSource=search_fortigate#support)은 532.9 usd/month
		- EIP
	- 장점: fortigate의 기술 서포트를 받을 수 있고 프록시의 단일장애 지점 위험을 줄이기 위하여 HA 구성이 가능(ha 구성시 비용 증가)합니다. 자세한 사항은 위의 프록시서버 설명을 참고해 주시기 바랍니다.
	- 단점: 상용 프록시 서버이기 때문에 별도의 라이센스 비용을 지불하셔야 합니다.

2) SAG + CEN + privatezone + nginx proxy
	- 데이터 플로우:
	- 
		![](https://github.com/rnlduaeo/alibaba/blob/master/sagPrivateZoneProxy.png?raw=true)
	
	slb+ecs2개 를 [ECI](https://www.alibabacloud.com/help/doc-detail/89129.htm?spm=a2c63.l28256.b99.2.29a03b03fJ3is8)로 바꾸어도 무방합니다. ECI는 serverless container로 사용자는 밑단의 인프라 장애 및 HA, 유지보수에 신경쓸 필요가 없습니다. 
	- 견적: sag app + cen + ecs + slb + privatezone
	- 장점: HA 구성이 가능하고  SAG관련 알리바바의 기술 지원을 받을 수 있습니다. 
	- 단점: 구성이 다소 복잡합니다. 직접 구축하기 어려운 경우 알리바바 파트너 사에게 구축을 맡길 수 있습니다. 파트너사와의 연결은 알리바바 클라우드 코리아 채널담당 고명훈 부장(myeonghoon.ko@alibaba-inc.com)에게 연락해주시기 바랍니다.
	- [위 구성에 대한 자세한 설정 가이드](https://github.com/rnlduaeo/alibaba/blob/master/SaaS%20acceleration%20for%20Korea.md)는 클릭하여 확인해주세요. 

3) pac + GA + squid proxy 
	- 데이터 플로우: 
![](https://github.com/rnlduaeo/alibaba/blob/master/squid.png?raw=true)
	- 견적: GA(basic, crossborder, instance) + ecs + eip
	- 장점: 간편한 구성, client 증가에 따른 추가 요금 없음
	- 단점: squid 관리 포인트, pac관리 포인트(포인트)
	- [위 구성에 대한 자세한 설정 가이드](https://www.alibabacloud.com/blog/cross-border-acceleration-with-alibaba-cloud---global-accelerator-and-squid-caching-proxy_597106)는 클릭하여 확인해주세요. 

위 가이드에 대해 문의사항이 있으시면 알리바바 코리아 SA팀에게 문의하시기 바랍니다.
- 김해미 Solution Architect: haemi.kim@alibaba-inc.com
- 임종진 Solution Architect: j.lim@alibaba-inc.com



<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzNDc1MDY3MDAsLTEyNTEwODM0MzEsMT
k0MDc5MTY3OCwtNzMxNDUzMTE0LDEyNDc3OTM5MjQsLTE2ODIz
MTE5MzUsMzU5NzMwNTcsLTE2ODIzMTE5MzUsMTI3NjQ1MTc2MC
wtMTM5MTA1NTg5NiwxMTExODg1ODEzLDcxMjQ5OTQ0OSwtMTU3
Mjc0MzYyMSwyMTk5NDIzOTksMjEzMzk2NjM0MSw2MjM2NDMwOD
csLTEzNzQ4MzEzMTcsOTc3ODU3NDQ0LDYwNDU3MDYyMCwxNDQ0
NTk1ODI3XX0=
-->
