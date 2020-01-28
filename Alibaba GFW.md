# 중국의 GFW과 ICP간 관계

## ICP 비안
중국 내 온라인(인터넷)을 통한 비즈니스를 운영할 시 필요한 절차이다. 자세한 사항은 문서 참고. 

## China Great Firewall
ICP와는 별개로 트래픽에 관한 규제이다. 
- **대상: Border Network(중국-중국외지역)를 경유하는 모든 public traffic(port)에 대하여 규제한다.**
- 방법: 알려진 바로는 키워드 필터링, IP 주소 블랙리스트, DNS poisioning, 패킷 검사 등을 통해 컨텐츠를 검열한다. 

위의 대상이 되는 트래픽에 대해 잘 기억하자.
## ICP와 China Great Firewall간의 관계
많은 경우에 한국에 서버를 두고 서비스를 하는데 중국 유저들의 접속이 원활하지 못한 경우가 있다. 단순히 속도가 느린 것은 다른 알리바바 서비스를 통해 쉽게 해결이 가능하지만, 문제는 가령 사이트 접속은 잘되는데 특정 컨텐츠가 안보인다든지, 모바일 앱을 켰는데 갑자기 접속이 안된다든지, 모바일 앱의 특정 기능이 작동 안 한다든지 등 중국의 great firewall에 의해 차단된 것으로 의심되는 경우이다. 이 경우 우리는 다음과 같은 질문을 할 수 있다.

- 현재 안되는 서비스(GFW에 의해 차단된 것으로 의심되는)에서 사용하는 도메인 이름을 ICP 비안을 통해 정식 등록을 하게 되면 서비스가 원활히 진행될까요?

**답은 아니다.**
 ICP와 China Great Firewall(GFW)은 별개이다. ICP비안을 받은 도메인을 사용할지라도 컨텐츠(즉 트래픽)에 따라 GFW에 의해 필터링 되어 서비스가 원활히 실행되지 못할 수 있다. 

## 해결 가능한 알리바바 클라우드 솔루션
위의 경우(문제의 원인이 GFW로 의심될 경우) 우리가 제안할 수 있는 솔루션은 GA2.0이다. 

GA2.0은 내부적으로 CEN(알리바바 전용선)라인을 사용한다. 따라서 GA를 사용하는 트래픽은 위에 언급한 GFW의 대상이 되는 "Border Network(중국-중국외지역)를 경유하는 모든 public traffic(port)"이 아니다. 즉, 검열 대상에서 제외된다는 의미이다. 

따라서 GFW이 의심되는 고객의 경우 GA2.0을 통한 테스트를 제안해 볼 수 있다.

예를 들어 근래 문제가 되었던 아프리카 TV같은 경우를 보자.
아래는 베이징에서 아프리카 티비의 vod를 보기 위해 요청을 보낸 것이다. DNS resolution부터 컨텐츠 전달 까지 잘 작동된다. 
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-28%20at%203.59.29%20PM.png?raw=true)

이번엔 다른 비디오(조금 야한 컨텐츠)의 URL로 요청을 보냈다. DNS resolution은 잘 진행되었지만(222.233.54.41 이라는 IP주소를 잘 받아온다) 요청에 대한 응답은 받지 못하였다. 즉, 트래픽이 client(중국)와 server(한국 위치)간 border network를 경유하므로 GFW의 컨텐츠 검열의 대상이 되었고, 컨텐츠가 부 적합하다고 판단되어 그 패킷은 버려진 것이다. 
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-28%20at%203.59.00%20PM.png?raw=true)

테스트 결과 (100% 확신은 못하지만) 여성이 출연하는 컨텐츠(vlog 포함)는 대부분 차단되었다. 어떤 키워드로 필터링되어 차단되는 지는 모르겠으나 이와 같이 GFW는 ICP 도메인과는 별개로 Border NW를 경유하는 모든 트래픽에 대하여 시행된다는 것을 알 수 있다.

또한 트래픽을 중간에서 가로채서 cleaning하는 것이기 때문에(anti-ddos의 scrubbing center와 유사, anti-ddos도 ddos로 의심되는 트래픽은 anti-ddos scrubbing center로 보내 cleaning한다.) 서비스가 되었다 안되었다 할 수 있다. 

> Note: MCA는 GFW의 대안이 될 수 없다. MCA는 Border Network에 CN라인이라고 하는 MPLS line(중국-홍콩)을 타게 된다. 이를 통해 일반 public 망을 통한 네트워크 보다는 빠르지만 위와 마찬가지로 GFW의 검열 대상이 된다. 

> Note 2: GA2.0을 사용하려면 ICP 도메인을 받아야 한다. 이유는 GA에서 발급하는 IP가 중국내 IP이기 때문이다. 

 ## 고객 상황에 따른 제안 방향
 1. 도메인 이름이 막힌 경우(nslookup 실패): 

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzNDY5OTI5ODQsMTgzNzA3MjI3N119
-->