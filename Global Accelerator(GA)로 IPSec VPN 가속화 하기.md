
# Global Accelerator(GA)로 IPSec VPN 가속화 하기

## 1. 배경  설명 
한국과 중국간 인터넷 통신은 매우 불안정합니다. 아래의 베이징(BJ)-서울(KR), 상하이(SH)-서울(KR) 간 ping test 결과를 살펴보면 평균 응답시간이 불규칙하고 ping loss 도 많이 발생하는 것을 알 수 있습니다. 

![](https://github.com/rnlduaeo/alibaba/blob/master/pingtime.png?raw=true)

이는 중국에서 비즈니스를 하는 대다수 고객들에게 많은 불편함을 야기합니다. 가령, 한국 본사와 중국 지사간 IPSec VPN으로 Site-to-Site VPN 통신을 맺고 시스템간 동기화 등의 연동을 맺고 있는 경우, 이 ping loss와 높은 지연시간은 시스템의 장애를 초래할 수 있는 매우 중대한 사안입니다. 
이번 포스팅에서는 알리바바 클라우드의 Global Accelerator(GA)를 통해 한국/중국 간 IPSec VPN 통신에 대한 네트워크의 안정성을 높이고 속도도 가속화하는 방법에 대해 다루어 보겠습니다. 

## 2. Solution Overview
### 2.1 Overview
이번 가이드에서는 중국 Alibaba Cloud의 VPN Gateway와 한국 AWS의 Virtual Private Gateway를 GA와 연동합니다. 이는 테스트를 위한 차선책으로 굳이 알리바바 클라우드의 VPN Gateway를 사용하지 않더라도 'NAT-T(Nat Traversal)'기능을 enable할 수 있는 고객사 VPN 장비라면 GA와 연동하여 가속화할 수 있습니다.
> Note: GA가 양단의 VPN 입장에서는 일종의 NAT 역할을 하는 장비가 되기 때문에, VPN장비 사이에 NAT 장비가 존재하게 되는 셈이고 이로 인해 Pair 메세지의 무결성이 침해되어 IKE Phase 1,2 협상 과정이 실패하게 됩니다. NAT-T 기능을 제공하는 VPN 장비로 이 문제를 해결할 수 있습니다. 

### 2.2 가속화 원리 
![](https://github.com/rnlduaeo/alibaba/blob/master/GAIpSecVPN1.png?raw=true)

알리바바 클라우드의 [Global Accelerator(GA)](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.l28256.b99.5.82586796Hc8DP7)
는 사용자 시스템의 IP/Domain만 등록하여 네트워크 통신을 가속화하는 솔루션입니다. 이번 가이드에서는 중국 상해에 고객사의 중국지사 VPN장비가 있고(Alibaba Cloud VPN Gateway로 대체) 한국에 본사 VPN 장비가 있다고(AWS Virtual Private Gateway로 대체) 가정하고 테스트를 수행합니다. 

## 3. 사전  조건 
1. [Alibaba Cloud VPN Gateway](https://www.alibabacloud.com/help/doc-detail/64960.htm?spm=a2c63.l28256.b99.5.5d6ae889hLNiHt) - 고객사 VPN 장비(NAT-T enabled)로 대체 가능
2. [AWS Virtual Private Gateway](https://docs.aws.amazon.com/ko_kr/vpn/latest/s2svpn/how_it_works.html) - 고객사 VPN 장비(NAT-T enabled)로 대체 가능
3. [Alibaba Cloud Global Accelerator](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.l28256.b99.5.82586796Hc8DP7) 
	 
	* GA 인스턴스를 만든 후 티켓을 통해 GA Instance ID로 'Source-Consistent' 기능 enable할 것을 요청합니다. 	
	* Listener 설정이 끝난 후 티켓을 통해 GA OFF IP를 획득합니다.(이 EIP는 한국 VPN 장비의 Peer IP로 사용됨) - GA 내부적으로 로드발란서의 가중치(weight)를 0으로 수정 (1 개의 ECS 만 포워딩 용으로 예약)하고 나머지 ECS의 EIP를 획득하는 과정입니다. 
	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-07-02%20at%2011.20.04%20AM.png?raw=true)


## 4. Main steps
![](https://github.com/rnlduaeo/alibaba/blob/master/Picture1.png?raw=true)
### 4.1 GA 인스턴스 생성과 Source Consistent 요청(Ticket)
#### 4.1.1 GA 인스턴스 및 밴드위스 생성
GA는 가속화 요건에 따라 다양한 조합의 구매가 가능합니다. 이번 시나리오는 중국과 한국간 네트워크를 가속화 하고, 양 종단이 Alibaba Cloud 외 리소스이기 때문에 아래의 조합으로 구매해 주시면 됩니다. 
> Note: [GA 인스턴스 및 밴드위스 구매 조건](https://www.alibabacloud.com/help/doc-detail/153194.htm?spm=a2c63.p38356.b99.10.571c2e24WeD1J9)에 대한 자세한 사항은 클릭하여 확인해 주시기 바랍니다. 

|GA Instance Type|Basic Bandwidth Type|Cross Border Acceleration |
|---|---|---|
|Small I(필요한 최대 밴드위스에 따라 구매)|Enhanced Bandwidth|구매|
[GA 인스턴스를 구매](https://www.alibabacloud.com/help/doc-detail/153200.htm?spm=a2c63.p38356.b99.22.3e8d3ec5YMYcrz) 하고 [Basic Bandwidth를 구매](https://www.alibabacloud.com/help/doc-detail/153205.htm?spm=a2c63.p38356.b99.27.111077493Kolwl)하고 [Cross Border Acceleration을 구매](https://www.alibabacloud.com/help/doc-detail/155107.htm?spm=a2c63.p38356.b99.35.4f37763eng34lg)합니다. 
그리고 구매한 Basic Bandwidth와 Cross Bandwidth를 GA 인스턴스에 bind합니다. 바인딩에 대한 자세한 사항은 [bind basic bandwidth 문서](https://www.alibabacloud.com/help/doc-detail/153206.htm?spm=a2c63.p38356.b99.28.34528816XU1IGd)와 bind cross border acceleration



### 4.2 GA 리스너 설정

### 4.3 GA OFF IP 획득

### 4.4 종단간 IPSec Connection 설정

### 4.5 연결 확인 및 속도/성능 확인

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA3ODYzNzI1NSwyMDI5Mzg1NjQ5LC0xMj
YzNjE3NDc5LC0xNzQ3NzEzNTYxLDEyMzYzNDAyMTEsLTYwODc1
MTcxMiw0OTMyNDM4MDQsLTE1MjE0MDY0MDcsMjQxMDU3NzUxLD
Y5MjIxNjc0NCwtMjEwODY1NTM3OF19
-->