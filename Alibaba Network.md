# Go-China NW 솔루션 비교

## 각 솔루션 소개
1. MCA
MCA는 알리바바 클라우드 DDoS Protection 중 Anti-DDoS Premium 서비스에 에 포함된 서비스이다. Anti-DDos Premium은 중국 밖에 위치한 서버를 위한 디도스 공격 완화 서비스이다. 만약 중국내 유저가 있고 서버가 중국 밖에 있다면 MCA를 함께 구매할 필요가 있다. 이렇게 MCA와 Anti-DDoS를 함께 사용하게 되면, STM(Security Traffic Manager)이 User Request를 받아 DDoS공격이 의심되는 트래픽은 중국 밖에 위치한 Anti-DDoS Scrubbing Center로 라우팅하여 공격을 완화시키고, 정상 트래픽은 MCA를 통해 가속화하여 Origin Server 에 트래픽을 빠르게 전달하게 된다. 다만, 주의할 점은 Anti-DDoS와 MCA 두개의 인스턴스를 함께 구매해야 하고, 중국 <-> 중국밖을 연결하는 MCA 구간은 bandwidth가 제한되어 있다. 10Mbps ~ 100Mbps까지 구매가능하다. (아래 그림 참고 - 아래 그림은 MCA bandwidth 10Mbps, AntiDDoS bandiwdth 100Mbps 구매 시 적용되는 그림이다.) 

![](https://github.com/rnlduaeo/alibaba/blob/master/MCA.png?raw=true)

> Note: Anti-DDoS Premium과 MCA는 모두 중국 밖의 리소스를 사용하기 때문에 ICP 비안을 받지 않은 도메인 설정이 가능하다. 따라서 가속화할 도메인 별로 http, https, websocket 도메인을 설정할 수 있다. https 도메인의 경우 ssl certificate 을 업로드 하여 적용 가능하다. Static contents에 한하여 Cache가 가능하지만 마찬가지로 중국밖 캐시노드에 매핑되고 client에서 다운받는 last mile도 MCA bandwidth안에 포함된다. 중국내 사용자 트래픽이 MCA bandwidth안에서 소화가능할 때 사용 가능한 솔루션이다. 

2. GA2.0
한 중간 전용선 연결 서비스이다. 타입은 여러가지가 있고 타입에 따라 알리바바 backbone 망(CEN)을 통한 
3. CDN

4. CEN

5. VPN

## 상황 별 Right Solution 정리


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4NzI0NTczNTYsLTE4ODM4ODI2OCw5ND
Y4NjYyMjQsLTE4MjAyMzA2OTUsLTE2MjUyNDczODldfQ==
-->