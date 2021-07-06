
# Alibaba Cloud VPC와 AWS VPC를 VPN으로 연결하기 (IPsec VPN Connection / Site-to-site VPN Connection)


## 1. 배경 설명

많은  기업들은  목적에  따라  다양한  종류의  Public Cloud를  사용하고  있습니다.

이는  사업의  형태  및  목적성에  따라  Alibaba Cloud 혹은  그  외의  Cloud를  혼용하여  사용하기도  하며  Vendor Lock-in 해제의  목적에  따라  같은  국가에  두개  이상의  Cloud 환경을  이용하기도  합니다.

본  시나리오는  고객이  이기종의  Cloud 환경을  안전하게  연결할  수  있는  VPN Connection에  대한  내용을  담았습니다.

특히  Alibaba Cloud의  고객  중  케이스가  많은  **중국의  Alibaba Cloud VPC – 한국의  AWS VPC를  연결하는  시나리오**에  대해서  해당  내용을  참조할  수  있습니다.

## 2. Solution Overview

예시  환경은  중국  Shanghai Region의  Alibaba Cloud VPC 환경과  한국  Central Region의  AWS VPC환경을  VPN (IPsec VPN Connection / Site-to-site VPN Connection) 으로  연결합니다.

<img width="648" alt="Screen Shot 2021-07-05 at 5 30 22 PM" src="https://user-images.githubusercontent.com/34003729/124441562-c2633500-ddb6-11eb-914f-d67b95f679cc.png">


## 3. 사전  준비

- [Alibaba Cloud VPN Gateway](https://www.alibabacloud.com/help/doc-detail/64960.htm?spm=a2c63.l28256.b99.5.5d6ae889hLNiHt)

- [AWS Virtual Private Gateway](https://docs.aws.amazon.com/ko_kr/vpn/latest/s2svpn/how_it_works.html)


## 4. Main Steps

**[Alibaba Cloud Side]**
### 4.1 VPC 생성
VPC를  생성합니다. 사용할  이름과  IPv4 CIDR Block을  설정합니다.
> VPC는  퍼블릭  클라우드에서  사용할  전용  가상  네트워크입니다. 설정된  IPv4 CIDR Block은  Private Network으로  사용할  구간으로  이해할  수  있습니다.

<img width="691" alt="Screen Shot 2021-07-05 at 5 39 07 PM" src="https://user-images.githubusercontent.com/34003729/124442672-effcae00-ddb7-11eb-9e63-88d6a38313d9.png">

### 4.2 VPN 생성
[VPN Gateway를  구매 및 생성](https://www.alibabacloud.com/help/doc-detail/65290.htm?spm=a2c63.l28256.b99.23.d9a5e889eDXe0e)합니다. 본  시나리오에서는  Shanghai Region에  생성했습니다.
> VPN은  Site to Site환경에서  통신  내용을  바깥  사람에게  드러내지  않고  통신할  목적으로  쓰이는  사설  통신망입니다. 이  환경에서  VPN Gateway는  Alibaba Cloud VPC 환경에  들어올  문으로  이해할  수  있습니다.

<img width="862" alt="Screen Shot 2021-07-05 at 5 41 08 PM" src="https://user-images.githubusercontent.com/34003729/124442991-3fdb7500-ddb8-11eb-95e7-383d346d9add.png">

### 4.3 VPN Gateway 설정
생성된  VPN Gateway의  Name을  설정합니다. 또한  VPN Gateway의  IP Address를  메모합니다.
> 이  IP Address는  VPN으로  연결될  AWS의  Customer Gateway에  설정됩니다.

<img width="882" alt="Screen Shot 2021-07-05 at 5 43 36 PM" src="https://user-images.githubusercontent.com/34003729/124443329-8cbf4b80-ddb8-11eb-8f91-4d20672c00b7.png">

**[AWS Side]**
*Alibaba Cloud에  Customer Gateway를  생성하기  전, Alibaba의  VPC에  연결될  환경인  AWS에  Virtual Private Gateway(Alibaba Cloud의  VPN Gateway와  같은  개념)를  생성해야  합니다.*

### 4.4 VPC 생성
Alibaba Cloud와  VPN으로  연결될  환경인  AWS에  VPC를  생성합니다. 생성된  VPC 정보에서  CIDR 정보를  메모합니다.
> 메모된  CIDR은  각  VPN Connection 설정  시  사용됩니다.

<img width="874" alt="Screen Shot 2021-07-05 at 5 46 29 PM" src="https://user-images.githubusercontent.com/34003729/124443809-f50e2d00-ddb8-11eb-8948-e7b990cdc6e5.png">

### 4.5 Virtual Private Gateway 생성
Virtual Private Gateway를  생성합니다. 해당  시나리오에서는  AWS에서  기본으로  설정될  ASN을  사용하기  때문에  별도  ASN을  설정할  필요는  없습니다.
> AWS의  Virtual Private Gateway는  AWS의  VPC환경에 VPN으로  접속될  Gate 의  역할을  합니다. ASN은  각기  다른  오퍼레이터가  관리하는  IP 서브넷을  식별하기  위해  고유하게  부여된  번호입니다.

<img width="871" alt="Screen Shot 2021-07-05 at 5 48 14 PM" src="https://user-images.githubusercontent.com/34003729/124444077-3272ba80-ddb9-11eb-90b4-4253d409698f.png">

### 4.6 Virtual Private Gateway 확인
생성된  Virtual Private Gateway의  ASN을  메모합니다.
> 해당  ASN은  Alibaba Cloud의  Customer Gateway에  입력됩니다.

<img width="736" alt="Screen Shot 2021-07-05 at 5 49 46 PM" src="https://user-images.githubusercontent.com/34003729/124444300-6948d080-ddb9-11eb-8237-73738a98ae12.png">

### 4.7 Customer Gateway 생성
AWS 환경에  Alibaba Cloud로  연결될  Customer Gateway를  생성합니다. 
- Routing : BGP를  사용할  것이므로  Routing은  Dynamic을  설정합니다. 
- BGP ASN : Alibaba Cloud BGP ASN의  기본  값인  45104으로  설정합니다. 추후  Alibaba Cloud VPN에서  IPsec Peering 설정  시  나오는  값으로  수정할  수  있습니다.
- IP Address : 4.3단계에서  메모한  Alibaba Cloud의  VPN Gateway IP를  입력합니다.

<img width="816" alt="Screen Shot 2021-07-05 at 5 54 16 PM" src="https://user-images.githubusercontent.com/34003729/124444934-0dcb1280-ddba-11eb-8117-740707240d04.png">

### 4.8 Site-to-Site VPN 설정
가장  중요한  단계인  AWS의  Site-to-Site VPN Connection(Alibaba Cloud의  IPsec Connection과  같은  의미) 설정입니다. 본  단계에서  아래와  같은  내용으로  입력합니다.
<![endif]-->

- Name tag : 사용할  VPN Connection 이름  입력
- Virtual Private Gateway : 4.5단계에서  생성한  VPG 선택
- Customer Gateway : 4.7 단계에서  생성한  Customer Gateway 선택
- Routing Options : Dynamic (requires BGP)
- Tunnel Inside Ip Version : IPv4
- Local IPv4 Network Cidr(중요) : 4.1 단계에서  생성한  Alibaba Cloud의  VPC 환경  Cidr 입력
- Remote IPv4 Network Cidr(중요) : 4.4 단계에서  생성된  AWS의  VPC환경  Cidr 입력
- Tunnel Option : 기본  값  사용
> AWS 환경에서  의미하는 Local은  Local Data Center를  의미하며  Remote는  원격지  Data Center를  의미합니다. 즉, 현재  환경에서  AWS Site에서의  Local은  Alibaba Cloud를  의미하여  Remote는  AWS를  의미합니다.

![Screen Shot 2021-07-05 at 5 57 03 PM](https://user-images.githubusercontent.com/34003729/124445366-73b79a00-ddba-11eb-9543-2257f3d039ee.png)

### 4.9 VPN Connection 확인
생성된  VPN Connection의  Tunnel Details 정보를  확인합니다. 생성된  Tunnel 1, 2의  Outside IP Address를  메모합니다.
> AWS의  Site to Site VPN Connection은  기본적으로  HA를  위한  옵션으로  터널을  두개  생성합니다. 우리는  본  환경에서  두개의  Tunnel을  연결하기  위해  Alibaba Cloud 환경에  Customer Gateway를  두개  생성해야  합니다.

<img width="872" alt="Screen Shot 2021-07-05 at 5 59 33 PM" src="https://user-images.githubusercontent.com/34003729/124445738-c5602480-ddba-11eb-8811-1ab3b9d73e94.png">

### 4.10 VPN Connection Configuration 다운로드
VPN Connection 화면에서  Download Configuration을  선택합니다. 나오는  팝업창에서는  구분이  쉬운  CISCO Configuration를  다운로드합니다.
> AWS에서는  VPN Connection 정보  확인을  위한  Configuration을  제공합니다. 본  시나리오에서는  해당  정보를  이용해  Alibaba Cloud IPsec Connection 설정을  쉽게  찾을  수  있습니다.

<img width="875" alt="Screen Shot 2021-07-05 at 6 00 54 PM" src="https://user-images.githubusercontent.com/34003729/124445959-f6d8f000-ddba-11eb-88dc-39a5fe0e5939.png">

### 4.11 Route Propagation 설정
Alibaba Cloud설정으로  넘어가기  전, AWS에  내부  네트워크에  자동  라우팅을  위한  경로  전파  활성화가  필요합니다. [VPC > Route tables > route table 선택 > Route propagation > Edit route propagation > 활성화] 작업을  수행합니다.

<img width="872" alt="Screen Shot 2021-07-05 at 6 02 54 PM" src="https://user-images.githubusercontent.com/34003729/124446275-3e5f7c00-ddbb-11eb-8567-3101ed654928.png">


**[Alibaba Cloud Side]**
*본  단계에서부터  Alibaba Cloud의  IPsec Connection을  설정합니다.*

### 4.12 Customer Gateway *2개* 생성
AWS VPN에  연결을  위한  Customer Gateway를  **2개**  생성합니다. 내용은  아래  내용을  참조할  수  있습니다.
- Name : AWS VPN Connection의  각  Tunnel 1 / 2와  연결할  이름  입력
- IP Address : 4.9에서  메모한  각  Tunnel 1 / 2의  Outside IP Address 입력
- ASN : 4.6에서  메모한  AWS 환경의  ASN 입력

![Screen Shot 2021-07-05 at 6 05 03 PM](https://user-images.githubusercontent.com/34003729/124446625-8ed6d980-ddbb-11eb-8b76-dcd86224225b.png)

### 4.13 IPsec VPN Connection *2개* 생성
Alibaba Cloud의  가장  중요한  단계인  IPsec Connection을  **두개**  생성합니다. 본  단계에서  필요한  내용들은  4.10에서  다운로드  받은  Configuration File에서  쉽게  참조할  수  있습니다.
> 전  단계에서  언급했듯이, AWS는  Site to Site VPN Connection을  생성하면  2개의  터널이  생성되는  메카니즘을  지니고  있습니다. 하지만  Alibaba Cloud는  기본적으로  한개의  터널로  VPN Connection을  생성하여  AWS와  연결을  위해서는  두개의  IPsec VPN Connection을  생성해야  합니다.

> 본  내용에서  Local Network/Remote Network은  AWS와  반대의  개념을  지니고  있습니다. Local Network은  Alibaba Cloud의  VPC를  의미하며  Remote Network은  Alibaba Cloud VPC와  연결될  원격지  즉, AWS의  VPC를  의미합니다.

- Name : 각Tunnel 1 / 2 연결을  위한  IPsec Connection 이름  입력
- VPN Gateway : 4.3에서  설정한  VPN Gateway 선택
- Customer Gateway : 4.12에서  생성한  각  Tunnel 1 / 2 연결을  위한  Customer Gateway 선택
- Routing Mode : Protected Data Flow 선택
- Local Network(중요) : 4.1에서  생성한  Alibaba Cloud VPC CIDR 입력
- Remote Network(중요) : 4.4에서  메모한  AWS VPC CIDR 입력
- Effective Immediately : YES
- Pre-shared Key : 4.10에서  다운받은  Configuration File에서  Pre-shared Key 검색하여  입력
- IKE / IPsec Configuration : 4.10에서  다운받은  Configuration 참조하여  각  항목  입력
- DPD, NAT Traversal : 활성화
- BGP Configuration : 활성화
- Tunnel CIDR Block : AWS VPN에  설정된  Tunnel 1 / 2의  Local CIDR 입력
- Local BGP IP Address : 위의  Block으로  입력된  xxx.xxx.xxx.xxx의  마지막  주소에  +1하여  입력  (스크린샷  예시  참조)
- Local ASN : 기본  값  사용  (해당  값으로  4.7 단계의  ASN과  싱크)

![Screen Shot 2021-07-05 at 6 08 23 PM](https://user-images.githubusercontent.com/34003729/124447132-0b69b800-ddbc-11eb-8476-87267fbcd9a6.png)
![Screen Shot 2021-07-05 at 6 08 39 PM](https://user-images.githubusercontent.com/34003729/124447181-16244d00-ddbc-11eb-82b8-5b902e3397a2.png)

### 4.14 연결 확인
연결을  기다린  후, Alibaba Cloud와  AWS 양쪽에서  정상적으로  연결이  된  것을  확인합니다.

*[Alibaba Cloud Side] – 2개의  Connection에  대한  Phase 2 of IKE Tunnel Negotiation Succeeded 확인*
<img width="853" alt="Screen Shot 2021-07-05 at 6 10 35 PM" src="https://user-images.githubusercontent.com/34003729/124447420-4f5cbd00-ddbc-11eb-94c5-b20690f4c089.png">


*[AWS Side] – Site-to-Site VPN Connection > VPN 선택  > Tunnel Details에서  두개의  터널  모두  UP으로  활성화  확인*
<img width="737" alt="Screen Shot 2021-07-05 at 6 11 13 PM" src="https://user-images.githubusercontent.com/34003729/124447505-656a7d80-ddbc-11eb-902a-901da0726632.png">


## 5. 결과

### 5.1 트러블 슈팅
연결을  시도했을  시  아래와  같이  Phase 1,2 of connection Fail 혹은  BGP : error 등의  붉은색  문구가  나오면  설정  문제로  연결이  실패했다는  뜻입니다. 우리는  해당  문제를Alibaba Cloud 사이트의  [FAQ](https://www.alibabacloud.com/help/doc-detail/65802.htm)를  통해  해결할  수  있습니다.

<img width="723" alt="Screen Shot 2021-07-05 at 6 12 47 PM" src="https://user-images.githubusercontent.com/34003729/124447729-9ea2ed80-ddbc-11eb-8d39-1ed02a168595.png">

만약  connection process에  대해  자세한  로그를  보고  싶으면  위  화면의  Actions > … > Logs 를  선택하여  아래  로그를  확인할  수  있습니다.

<img width="830" alt="Screen Shot 2021-07-05 at 6 13 33 PM" src="https://user-images.githubusercontent.com/34003729/124447831-baa68f00-ddbc-11eb-9751-d6d302deec1f.png">

## 5.2 연결 테스트
정상적으로  연결된  Alibaba Cloud VPC, AWS VPC 환경에  각각  ECS / EC2를  생성하고  Security Group에서  ICMP를  Allow한  후  Private IP로  Ping 테스트를  진행합니다.

<img width="870" alt="Screen Shot 2021-07-05 at 6 14 33 PM" src="https://user-images.githubusercontent.com/34003729/124447949-dd38a800-ddbc-11eb-99c7-59bc52dc650f.png">

양방향  모두  정상적으로  Private 통신이  가능함을  확인할  수  있습니다. 하지만  해당  시나리오는  한-중간  통신이라는  조건으로  많은  Packet Loss와  Delay가  발생됨을  확인할  수  있습니다.

# 마치며..

다음  시나리오에서는  본  시나리오에서  문제가  된  Site 간  VPN 연결에서의  Packet Loss 및  연결  지연  문제를  해결할  수  있는  가속화  솔루션([Alibaba Cloud Global Accelerator](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.l28256.b99.5.82586796Hc8DP7))를  연동한  내용을  확인하실  수  있습니다.
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTY5MTQ0NTMyLC0xNjg1NTMyNzYyLC04ND
Y0NTMwNDYsLTE1OTc0NDYxMDQsLTI1ODI5MjcxNSwtMzA5MDI3
MTM5LC04NTg1OTQ3NjQsLTIwMzExMjI2NzksMTQxMTI0ODU1NS
wtMzA5MDI3MTM5LDE0MTEyNDg1NTVdfQ==
-->