# SSH connection acceleration with GA including ACL

As of 2020.07.05, there is no feature that control ACL(Access Control List) in Global Accelerator(GA).(BTW This feature is planned to be published on 2020.10) However, if we think of working on server via ssh, we typically allow only specific fixed IP range to which IT team belongs or use bastion server for security reasons. Here we will discuss how we can use GA to accelerate ssh traffic between China and Korea and setup firewall rule based on client IP address at the same time.

## Test scenario
1. For Korea users to access China server, setup Korea as an accelerated area and Beijing as an endpoint group area.
2. GA instance - Basic bandwidth(enhanced) + Cross-border bandwidth

## Prerequisite
1. Submit a ticket for adding Korea region - this is done based on UID(User ID)
2. Submit a ticket for enable 'Reserve client IP addresses' feature - this is also done based on UID
	> Note: Before purchasing an instance, you should apply above two things in advance, otherwise you should purchase an instance again after application. This inconvenience has been escalated to product development team. It should be fixed as quickly as possible.

## Architecture diagram
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%207.52.50%20PM.png?raw=true)


## Step by step configuration
1. You can check detailed procedure of GA configuration in [Alibaba GA document](https://www.alibabacloud.com/help/doc-detail/153199.htm?spm=a2c63.p38356.b99.13.23f95285c25T51)
2. While configuring endpoint group, you would see the menu 'Reserve Client IP' given that your whitelist has been applied successfully to your account. You should enable this feature.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%206.36.19%20PM.png?raw=true)
3. This is the result of GA configuration. The red boxes in the image are what you should be aware of for further configuration later on.

	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%206.34.31%20PM.png?raw=true)
4. Origin server is hosed in Alibaba Cloud and I added its public IP address. An Endpoint Group IP should be added to cloud security group.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%206.35.16%20PM.png?raw=true)
5. In ecs console, I added four endpoint group IP.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%206.51.52%20PM.png?raw=true)
6. Assuming AWS Seoul public IP is the client's static IP, I ssh to the Alibaba ecs(Beijing) from AWS ec2(Client in Seoul) and at the same time, I captured tcpdump on port 22. In result, as you can see as follows, client real IP has been captured. (62.78.119.192)
	```
	# tcpdump -nn port 22 -w result.pcap
	```
	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%207.04.10%20PM.png?raw=true)
	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%207.04.39%20PM.png?raw=true)

7. Let's whitelist source IP addresses and port in OS firewall rule. (CentOS 7)
	By default, the firewall is disabled in ecs, so we need to enable the firewall rule first.
	```
	# systemctl status firewalld
	# systemctl start firewalld
	# firewall-cmd --list-all
	```
	You'll see your default zone is public and the services enabled are dhcpv6-client and ssh. We don't want any public services available, only the whitelisted IP's are authorized. So let's remove the two public services.
	
	```
	# firewall-cmd --zone=public --remove-service=ssh --permanent
	# firewall-cmd --zone=public --remove-service=dhcpv6-client --permanent
	```
	Now, let's whitelist a specific IP which grants access to 22(SSH) port.
	```
	# firewall-cmd --permanent --zone=public --add-rich-rule='rule family="ipv4" source address="xx.xx.xx.xx" service name="ssh" accept'
	```
	If you're connecting via SSH, be sure to authorize your IP before applying your new rule set. When ready to apply the new rules.
	```
	# firewall-cmd --reload
	```
8. Test if it works. On the left side, connected from 52.78.119.192 and on the right side, connected from my macbook PC. It only allows ssh connection from specific IP. 
	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%207.29.28%20PM.png?raw=true)
	
	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-07-15%20at%207.52.50%20PM.png?raw=true)
9. Opposite way is simpler than this one. You can setup following data flow as below.
China client --> ECS(eg. Beijing, setup forward rule to forward the traffic on 22 port to GA accelerated IP) + Security Group that only allows specific IP range on port 22 --> GA --> Server in Korea 
	


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIxMDI0Njg0NzUsLTEzNTg3NDI0MTJdfQ
==
-->