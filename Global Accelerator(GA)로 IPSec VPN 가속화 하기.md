
# Global Accelerator(GA)로 IPSec VPN 가속화 하기

## 1. background
한국과 중국간 인터넷 통신은 매우 불안정합니다. 아래의 베이징(BJ)-서울(KR), 상하이(SH)-서울(KR) 간 ping test 결과를 살펴보면 평균 응답시간이 불규칙하고 ping loss 도 많이 발생하는 것을 알 수 있습니다. 
![](https://github.com/rnlduaeo/alibaba/blob/master/pingtime.png?raw=true)
이는 중국에서 비즈니스를 하는 대다수 고객들에게 많은 불편함을 야기합니다. 가령, 한국 본사와 중국 지사간 IPSec VPN으로 Site-to-Site VPN 통신을 맺고 시스템간 동기화 등의 연동을 맺고 있는 경우, 이 ping loss와 높은 지연시간은 시스템의 장애를 초래할 수 있는 매우 중대한 사안입니다. 
이번 포스팅에서는 알리바바 클라우드의 Global Accelerator(GA)를 통해 한국/중국 간 IPSec VPN 통신에 대한 네트워크의 안정성을 높이고 속도도 가속화하는 방법에 대해 다루어 보겠습니다. 

## 2. Solution Overview
### 2.1 Overview
이번 가이드에서는 중국 Alibaba Cloud의 VPN Gateway와 한국 AWS의 Virtual Private Gateway를 GA와 연동합니다. 이는 테스트를 위한 차선책으로 굳이 알리바바 클라우드의 VPN Gateway를 사용하지 않더라도 'NAT-T(Nat Traversal)'기능을 enable할 수 있는 고객사 VPN 장비라면 GA와 연동하여 가속화할 수 있습니다.
> Note: GA가 양단의 VPN 입장에서는 일종의 NAT 역할을 하는 장비가 되기 때문에, VPN장비 사이에 NAT 장비가 존재하게 되는 셈이고 이로 인해 Pair 메세지의 무결성이 침해되어 IKE Phase 1,2 협상 과정이 실패하게 됩니다. NAT-T 기능을 제공하는 VPN 장비로 이 문제를 해결할 수 있습니다. 

### 2.2 Acceleration Principle
![](https://github.com/rnlduaeo/alibaba/blob/master/GAIpSecVPN1.png?raw=true)
알리바바 클라우드의 [Global Accelerator(GA)](https://www.alibabacloud.com/help/doc-detail/153189.htm?spm=a2c63.l28256.b99.5.82586796Hc8DP7)
는 사용자 시스템의 IP/Domain만 등록하면 전세계의 기 구축된 알리바바 클라우드의 글로벌 백본망을 통해 네트워크 통신을 가속화하는 솔루션입니다. 
## 3. Prerequisites


## 4. Main steps
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.03.13%20PM.png?raw=true)

### 4.1 create a VPC/CEN/CCN
In this step, the basic network architecture on which the entire service depends is built. 

### 4.1.1 create a VPC
In this scenario, we need to create 2 VPC.
|   VPC name       |usage                          |Region     |     Address segment  |
|----------------|-------------------------------|-----------------------------|----|
|Proxy_VPC|Deploy forward proxy services|Shanghai (can be the other region depending on your needs)| 10.0.0.0/8
|PVZ_VPC|The domain name associated with the PrivateZone.|Shanghai|172.19.0.0/16

Which Proxy-VPC can be created in 2 different AZ the vSwitch for easy deployment High available agent cluster. You do not need to deploy any resources in the PVZ-VPC. You can also use any existing domestic VPC without any conflict with the PrivateZone configuration.

### 4.1.2 create a CEN
Create a CEN instance named SF_Accelerate_CEN.

For more information, see:
https://www.alibabacloud.com/help/doc-detail/128625.htm?spm=a2c63.l28256.b99.21.28856ee1KV3iAr

Add the previously created Proxy_VPC and PVZ_VPC to CEN.

For detailed operation steps, see:
https://www.alibabacloud.com/help/doc-detail/128653.htm?spm=a2c63.p38356.b99.22.a6d216b0iUTv2R

### 4.1.3 create a CCN
Create a CCN instance for SAG-APP access and name it SF_Accelerate_CCN.

The steps to create CCN are detailed in:
https://www.alibabacloud.com/help/doc-detail/93669.htm?spm=a2c63.p38356.b99.84.3ca863f2I8DgK7

After the CCN is created, bind the CCN to SF_Accelerate_CEN. For more information, see:
https://www.alibabacloud.com/help/doc-detail/93671.htm?spm=a2c63.p38356.b99.83.6b3e72e6tMfBFd

## 4.2 Create proxy ECS, GA and bind a backend ECS
In this step, we will create a proxy instance in Proxy_VPC in Shanghai as an exit for service access.

### 4.2.1 Create a proxy ECS instance
The following is an example of an ECS instance:
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.08.34%20PM.png?raw=true)
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.09.56%20PM.png?raw=true)
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.08.49%20PM.png?raw=true)
Where:
1.  Configure the Internet bandwidth as needed;
2.  The security group needs to release TCP80 and TCP443 ports;
3.  The instance type can be configured as needed;
4.  According to the HA need, you can create create two different ECS in different zones and use SLB to forward the traffic to backend ECS. Here I only create a single instance.


### 4.2.2 Create a GA instance
If your whitelist (see in the prerequisites section) is successfully applied, you would see the Global Accelerator in VPC console.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.02.08%20PM.png?raw=true)

Select the region 'Asia Pacific NE 2 pop (Seoul)'.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.02.32%20PM.png?raw=true)

Select the 'Dedicated Bandwidth' and the 'create instance' button. 
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.03.35%20PM.png?raw=true)

Select the same as the figure below and complete purchasing.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.04.00%20PM.png?raw=true)


### 4.2.2 Bind the backend instance
Now you can see the GA instance just created. Make sure that you choose the region 'Asia Pacific NE 2 pop (Seoul)', otherwise you can not see anything in the console.
Click the 'Bind instance' button.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.48.11%20PM.png?raw=true)

Choose the ECS instance previously created.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.48.48%20PM.png?raw=true)

Now you can see the backend service instance IP address. Copy this address to keep it.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.49.22%20PM.png?raw=true)

### 4.2.3 Activate the backend service
After the backend service is bound, you need to add a NIC sub interface to the bound ECS instance. The IP address of the sub interface is the backend service address allocated by the system. After the backend service is bound to the Global Acceleration instance, the acceleration link is always active as long as the sub interface in the backend server is correctly configured.

> Note: Activation is required only when the backend service is an ECS instance.

1. Access the proxy ECS. 
2. Run the following command to open the NIC configuration file.
	```
	sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0:1
	```
3. Add the following information in the configuration file. Change the IPADDR to your own copied address from previous section.
	```
	DEVICE=eth0:1
	 IPADDR=10.0.0.124
	 NETMASK=255.255.255.255
	 ONBOOT=yes
	```
4. Run the following command to make the configuration take effect.
	```
	ifup eth0:1
	```
5. Verification
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.25.43%20PM.png?raw=true)
	After the backend service is bound, you can ping the EIP of the Global Acceleration instance to verify if the configuration takes effect. 

## 4.3 configure proxy service
### 4.3.1 configure a forward proxy using nginx
Log in to the proxy ECS and run the following command after root logon:
```
curl https://network-scripts.oss-cn-shanghai.aliyuncs.com/proxy-scripts/install-proxy.sh|bash
```
If you want to see how the forward proxy works through **ngx_stream_ssl_preread_module** in nginx, reach the following blog to understand how this L4 proxy extract the domain name from the upper-layer packets to obtain the target domain name. (in this case, teams related domains)
https://www.alibabacloud.com/blog/how-to-use-nginx-as-an-https-forward-proxy-server_595799#

### 4.3.2 configure SNAT 
1. log in to the proxy ECS server via SSH and enable IP forwarding:
	```
	echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
	sysctl -p
	```

2. Install and configure the iptables SNAT rules. In our scenario, we should change the source IP from eth0 to eth0:1 to access the internet through the GA public IP.
	```
	yum -y install iptables-services
	systemctl start iptables       
	systemctl enable iptables  
	
   #snat rule, dns resolve to eth0, and using eth0:1 as a source to access the internet
	iptables -t nat -A POSTROUTING -s 10.0.0.122 -o eth0 -j SNAT --to-source 10.0.0.124

	iptables-save > /etc/sysconfig/iptables
	systemctl restart iptables
	```
3. Verify configuration using the command `iptables -L -n -t nat`. You should see a SNAT rule is configured:
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.57.04%20PM.png?raw=true)

4. SNAT Verification
if you can access the internet, `ping 8.8.8.8` then, SNAT is successfully working.

## 4.4 Configure PrivateZone and domain names
In this step, we create a PrivateZone and configure the relevant domain name. Then associate this PrivateZone with PVZ_VPC for SAG-APP acceleration.

### 4.4.1 activate PrivateZone
The procedure for activating PrivateZone is as follows:
https://www.alibabacloud.com/help/doc-detail/64627.htm?spm=a2c63.l28256.b99.13.3b872bdd0Pu1Y9

### 4.4.2 add an accelerate domain name
First add a zone
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.06.48%20PM.png?raw=true)

> Note: If you need to configure generic resolution, do not check the subdomain recursive resolution proxy.

Add the required domain name resolution to the Zone: pointing to proxy ECS eth0 address
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.07.11%20PM.png?raw=true)
You can configure a wildcard resolution to overwrite all subdomains under this domain name to reduce the configuration workload.

Fore more information, see:
https://www.alibabacloud.com/help/doc-detail/64628.htm?spm=a2c63.p38356.b99.14.26287690yMEHob

### 4.4.3 Associate with PVZ_VPC
Click 'bind VPC' and associate the newly created Zone with PVZ_VPC.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.07.45%20PM.png?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.08.13%20PM.png?raw=true)

For more information, see:
https://www.alibabacloud.com/help/doc-detail/64629.htm?spm=a2c63.p38356.b99.15.171a17cfmRaO4L

Do the same procedure for other domains. In my test scenario, I found out 8 domains are engaged to access Microsoft teams. I registered all the domains.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.08.32%20PM.png?raw=true)

### 4.4.4 Configure Private Zone in CEN 
You need to publish the Private Zone to CEN so as to let other CEN networks (PVZ_VPC) communicate with Private Zone.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.09.45%20PM.png?raw=true)

## 4.5 purchase and configure SAG-APP
In this step, we will purchase and configure SAG-APP to enable the terminal to access CCN and access the proxy server cluster in Shanghai through CEN.
You can purchase, configure, and create an account.
### 4.5.1 purchase SAG-APP
For more information about how to setup SAG-APP, see:
https://www.alibabacloud.com/help/doc-detail/173726.htm?spm=a2c63.p38356.b99.139.222231c0FfvHFY

### 4.5.2 configure SAG-APP
After the purchase is successful, you need to configure the SAG-APP. Mainly:
-   Bind CCN: the SF_Accelerate_CCN created before binding;
-   Configure DNS: configure the PrivateZone DNS, namely 100.2.136 and 100.100.2.138;
-   Configure private CIDR block: configure the CIDR block assigned to the SAG-APP client. This CIDR block must be carefully planned and cannot conflict with other CIDR blocks in the network, try to avoid conflicts with the address segment of the customer terminal itself and avoid using the address segment in 168.0.0/16.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.33.45%20PM.png?raw=true)

### 4.5.3 create SAG-APP account
After you download and install the SAG app on your terminal, you need to wait for a while to access Alibaba Cloud Network. If you fail to access to intranet network, please wait for a while and retry.

# 5. Verification
You can compare the upload/download speed while connecting to SAG app and disconnecting to SAG app respectively to compare the latency and packet loss.

# 6. Application to other similar scenarios
-   **Bypass the China Great Firewall**: This scenario only takes an example of microsoft teams, but you can register the any domains(using wildcard domain) in PrivateZone that you want to access from China. (such as google drive, sites that are forbidden to access from China filtered by China Great Firewall, you can use this scenario to bypass GFW, But I do not know whether it is allowed from China regulation perspective)
-   **Accelerate network from Korea to China**: You don't need to use GA in this case, you can simply use the combination of 'SAG+CEN(cross-border bandwidth)+Proxy ECS' with same configuration in above sections. Two things different are that you need to add CEN cross border bandwidth to connect Korea to China through Alibaba Cloud backbone network and, and you can skip SNAT setting on the proxy ECS server. In this case, you can access several China sites (for example [www.qq.com](http://www.qq.com/), baidu.com) over Alibaba backbone network to with accelerated network speed.# SaaS acceleration for Korea: SAG + CEN + GA (for bidirectional, KR to CN and CN to KR)

# 1. background
Many multinational enterprises use SaaS services deployed overseas, such as Office365 and Salesforce. Due to the poor quality of China domestic visits to overseas sites, the customer experience is badly affected.

This solution uses smart Access Gateway SAG, CEN and GA1.0 to build an application acceleration service, which can help domestic users in China accelerate access to application systems deployed overseas.

Before the start, you need to check the location of your SaaS service so that you can determine the proxy ECS instance region. If it's not located in Korea, please reach out to Alibaba Cloud Korea sales rep.

# 2. Solution Overview
## 2.1 Overview
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2011.04.06%20AM.png?raw=true)

To accelerate the Korea MS teams service as an example, we have 5 main parts:
1. Client: SAG-APP is Alibaba Cloud SD-WAN client software that can be installed on Android, iOS, Windows, MacOS and other systems. SAG-APP can be connected to the nearest access point(PoP) of the CCN network.
2. CCN: CCN is Alibaba Cloud SD-WAN access network, which consists of access points all over the country. It can quickly connect SAG terminals to Alibaba Cloud backbone networks.
3. CEN: CEN is a global virtual enterprise network. Relying on Alibaba Cloud global backbone network, it provides high-quality global networking services for enterprise customers.
4. Proxy server: As a forward proxy and SNAT, it has two different functions to forward the traffic. It acts as a L4 proxy  helped from the upper layer to extract the domain name and acts as a SNAT to access public internet through GAIP.
5. GA1.0: Backed by the Alibaba Cloud backbone network, GA provides a high-speed network experience and ultra-low transmission latency between China and Korea.

## 2.2 Acceleration Principle

This solution can accelerate HTTP/HTTPs based on the domain name.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2011.26.37%20AM.png?raw=true)
1. The client configures the DNS address of the Private Zone. The custom DNS function of the SAG-APP allows you to configure the DNS of the terminal to Private Zone DNS. 

Private Zone DNS addresses are 100.100.2.136 and 100.100.2.138

2. Use the Private Zone to resolve the domain name to be accelerated into the internal IP address of the proxy server. If the domain does not exist in Private Zone, the SAG client then lookup public DNS to reach the target server. In this way, we only accelerate teams related domains.
3. The traffic to be accelerated is forwarded to the proxy server via CCN and CEN. The proxy server then send the request to the MS teams service through the local Korea internet.
4. Traffic that does not need to be accelerated is not pulled to CCN, and is directly accessed from the local internet of the client, without occupying SAG-APP acceleration bandwidth.

# 3. Prerequisites
As of now(2021.02.16), Alibaba Cloud do not have a Korea region. For having every component be in Alibaba Cloud, we use an old version of GA(Global Accelerator). We can use a current version of GA, but then we need to deploy a proxy in somewhere in Korea by using other cloud vendors or IDC etc, which leads to become cumbersome to manage entire components. To be able to use old version of GA(GA1.0), you need to submit the ticket and apply a whitelist. Make sure that you apply all of them below.
	1) GA1.0
	2) Korea(Seoul) Network PoP for an accelerated area
	3) A VPC whitelist for Korea Network PoP

# 4. Main steps
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.03.13%20PM.png?raw=true)

## 4.1 create a VPC/CEN/CCN
In this step, the basic network architecture on which the entire service depends is built. 

### 4.1.1 create a VPC
In this scenario, we need to create 2 VPC.
|   VPC name       |usage                          |Region     |     Address segment  |
|----------------|-------------------------------|-----------------------------|----|
|Proxy_VPC|Deploy forward proxy services|Shanghai (can be the other region depending on your needs)| 10.0.0.0/8
|PVZ_VPC|The domain name associated with the PrivateZone.|Shanghai|172.19.0.0/16

Which Proxy-VPC can be created in 2 different AZ the vSwitch for easy deployment High available agent cluster. You do not need to deploy any resources in the PVZ-VPC. You can also use any existing domestic VPC without any conflict with the PrivateZone configuration.

### 4.1.2 create a CEN
Create a CEN instance named SF_Accelerate_CEN.

For more information, see:
https://www.alibabacloud.com/help/doc-detail/128625.htm?spm=a2c63.l28256.b99.21.28856ee1KV3iAr

Add the previously created Proxy_VPC and PVZ_VPC to CEN.

For detailed operation steps, see:
https://www.alibabacloud.com/help/doc-detail/128653.htm?spm=a2c63.p38356.b99.22.a6d216b0iUTv2R

### 4.1.3 create a CCN
Create a CCN instance for SAG-APP access and name it SF_Accelerate_CCN.

The steps to create CCN are detailed in:
https://www.alibabacloud.com/help/doc-detail/93669.htm?spm=a2c63.p38356.b99.84.3ca863f2I8DgK7

After the CCN is created, bind the CCN to SF_Accelerate_CEN. For more information, see:
https://www.alibabacloud.com/help/doc-detail/93671.htm?spm=a2c63.p38356.b99.83.6b3e72e6tMfBFd

## 4.2 Create proxy ECS, GA and bind a backend ECS
In this step, we will create a proxy instance in Proxy_VPC in Shanghai as an exit for service access.

### 4.2.1 Create a proxy ECS instance
The following is an example of an ECS instance:
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.08.34%20PM.png?raw=true)
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.09.56%20PM.png?raw=true)
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.08.49%20PM.png?raw=true)
Where:
1.  Configure the Internet bandwidth as needed;
2.  The security group needs to release TCP80 and TCP443 ports;
3.  The instance type can be configured as needed;
4.  According to the HA need, you can create create two different ECS in different zones and use SLB to forward the traffic to backend ECS. Here I only create a single instance.


### 4.2.2 Create a GA instance
If your whitelist (see in the prerequisites section) is successfully applied, you would see the Global Accelerator in VPC console.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.02.08%20PM.png?raw=true)

Select the region 'Asia Pacific NE 2 pop (Seoul)'.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.02.32%20PM.png?raw=true)

Select the 'Dedicated Bandwidth' and the 'create instance' button. 
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.03.35%20PM.png?raw=true)

Select the same as the figure below and complete purchasing.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.04.00%20PM.png?raw=true)


### 4.2.2 Bind the backend instance
Now you can see the GA instance just created. Make sure that you choose the region 'Asia Pacific NE 2 pop (Seoul)', otherwise you can not see anything in the console.
Click the 'Bind instance' button.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.48.11%20PM.png?raw=true)

Choose the ECS instance previously created.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.48.48%20PM.png?raw=true)

Now you can see the backend service instance IP address. Copy this address to keep it.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%2012.49.22%20PM.png?raw=true)

### 4.2.3 Activate the backend service
After the backend service is bound, you need to add a NIC sub interface to the bound ECS instance. The IP address of the sub interface is the backend service address allocated by the system. After the backend service is bound to the Global Acceleration instance, the acceleration link is always active as long as the sub interface in the backend server is correctly configured.

> Note: Activation is required only when the backend service is an ECS instance.

1. Access the proxy ECS. 
2. Run the following command to open the NIC configuration file.
	```
	sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0:1
	```
3. Add the following information in the configuration file. Change the IPADDR to your own copied address from previous section.
	```
	DEVICE=eth0:1
	 IPADDR=10.0.0.124
	 NETMASK=255.255.255.255
	 ONBOOT=yes
	```
4. Run the following command to make the configuration take effect.
	```
	ifup eth0:1
	```
5. Verification
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.25.43%20PM.png?raw=true)
	After the backend service is bound, you can ping the EIP of the Global Acceleration instance to verify if the configuration takes effect. 

## 4.3 configure proxy service
### 4.3.1 configure a forward proxy using nginx
Log in to the proxy ECS and run the following command after root logon:
```
curl https://network-scripts.oss-cn-shanghai.aliyuncs.com/proxy-scripts/install-proxy.sh|bash
```
If you want to see how the forward proxy works through **ngx_stream_ssl_preread_module** in nginx, reach the following blog to understand how this L4 proxy extract the domain name from the upper-layer packets to obtain the target domain name. (in this case, teams related domains)
https://www.alibabacloud.com/blog/how-to-use-nginx-as-an-https-forward-proxy-server_595799#

### 4.3.2 configure SNAT 
1. log in to the proxy ECS server via SSH and enable IP forwarding:
	```
	echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
	sysctl -p
	```

2. Install and configure the iptables SNAT rules. In our scenario, we should change the source IP from eth0 to eth0:1 to access the internet through the GA public IP.
	```
	yum -y install iptables-services
	systemctl start iptables       
	systemctl enable iptables  
	
   #snat rule, dns resolve to eth0, and using eth0:1 as a source to access the internet
	iptables -t nat -A POSTROUTING -s 10.0.0.122 -o eth0 -j SNAT --to-source 10.0.0.124

	iptables-save > /etc/sysconfig/iptables
	systemctl restart iptables
	```
3. Verify configuration using the command `iptables -L -n -t nat`. You should see a SNAT rule is configured:
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%201.57.04%20PM.png?raw=true)

4. SNAT Verification
if you can access the internet, `ping 8.8.8.8` then, SNAT is successfully working.

## 4.4 Configure PrivateZone and domain names
In this step, we create a PrivateZone and configure the relevant domain name. Then associate this PrivateZone with PVZ_VPC for SAG-APP acceleration.

### 4.4.1 activate PrivateZone
The procedure for activating PrivateZone is as follows:
https://www.alibabacloud.com/help/doc-detail/64627.htm?spm=a2c63.l28256.b99.13.3b872bdd0Pu1Y9

### 4.4.2 add an accelerate domain name
First add a zone
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.06.48%20PM.png?raw=true)

> Note: If you need to configure generic resolution, do not check the subdomain recursive resolution proxy.

Add the required domain name resolution to the Zone: pointing to proxy ECS eth0 address
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.07.11%20PM.png?raw=true)
You can configure a wildcard resolution to overwrite all subdomains under this domain name to reduce the configuration workload.

Fore more information, see:
https://www.alibabacloud.com/help/doc-detail/64628.htm?spm=a2c63.p38356.b99.14.26287690yMEHob

### 4.4.3 Associate with PVZ_VPC
Click 'bind VPC' and associate the newly created Zone with PVZ_VPC.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.07.45%20PM.png?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.08.13%20PM.png?raw=true)

For more information, see:
https://www.alibabacloud.com/help/doc-detail/64629.htm?spm=a2c63.p38356.b99.15.171a17cfmRaO4L

Do the same procedure for other domains. In my test scenario, I found out 8 domains are engaged to access Microsoft teams. I registered all the domains.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.08.32%20PM.png?raw=true)

### 4.4.4 Configure Private Zone in CEN 
You need to publish the Private Zone to CEN so as to let other CEN networks (PVZ_VPC) communicate with Private Zone.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.09.45%20PM.png?raw=true)

## 4.5 purchase and configure SAG-APP
In this step, we will purchase and configure SAG-APP to enable the terminal to access CCN and access the proxy server cluster in Shanghai through CEN.
You can purchase, configure, and create an account.
### 4.5.1 purchase SAG-APP
For more information about how to setup SAG-APP, see:
https://www.alibabacloud.com/help/doc-detail/173726.htm?spm=a2c63.p38356.b99.139.222231c0FfvHFY

### 4.5.2 configure SAG-APP
After the purchase is successful, you need to configure the SAG-APP. Mainly:
-   Bind CCN: the SF_Accelerate_CCN created before binding;
-   Configure DNS: configure the PrivateZone DNS, namely 100.2.136 and 100.100.2.138;
-   Configure private CIDR block: configure the CIDR block assigned to the SAG-APP client. This CIDR block must be carefully planned and cannot conflict with other CIDR blocks in the network, try to avoid conflicts with the address segment of the customer terminal itself and avoid using the address segment in 168.0.0/16.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202021-02-16%20at%202.33.45%20PM.png?raw=true)

### 4.5.3 create SAG-APP account
After you download and install the SAG app on your terminal, you need to wait for a while to access Alibaba Cloud Network. If you fail to access to intranet network, please wait for a while and retry.

# 5. Verification
You can compare the upload/download speed while connecting to SAG app and disconnecting to SAG app respectively to compare the latency and packet loss.

# 6. Application to other similar scenarios
-   **Bypass the China Great Firewall**: This scenario only takes an example of microsoft teams, but you can register the any domains(using wildcard domain) in PrivateZone that you want to access from China. (such as google drive, sites that are forbidden to access from China filtered by China Great Firewall, you can use this scenario to bypass GFW, But I do not know whether it is allowed from China regulation perspective)
-   **Accelerate network from Korea to China**: You don't need to use GA in this case, you can simply use the combination of 'SAG+CEN(cross-border bandwidth)+Proxy ECS' with same configuration in above sections. Two things different are that you need to add CEN cross border bandwidth to connect Korea to China through Alibaba Cloud backbone network and, and you can skip SNAT setting on the proxy ECS server. In this case, you can access several China sites (for example [www.qq.com](http://www.qq.com/), baidu.com) over Alibaba backbone network to with accelerated network speed.
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTk0ODU3Mzc0LC0yMTA4NjU1Mzc4XX0=
-->