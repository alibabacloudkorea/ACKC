# MCA Test 

MCA는 알리바바에서 제공하는 Anti-DDos Premium 제품의 일부 기능이다. Anti-DDos는 DDos 공격으로 의심되는 트래픽을 사전에 차단하고 완화해주는 Security Service이다. 이 Anti-DDos에는 MCA라는 Mainland China Accelerator라는 기능이 있다. 이 기능을 사용하면 비정상(DDos 공격으로 의심되는) 트래픽은 Anti-DDos instance로 라우팅 되어 scrubbing되고, 정상 트래픽은 MCA instance로 라우팅 되어 중국과 그밖의 지역 간 네트워크 전송속도를 향상 시킨다. 

![](http://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/assets/img/79672/154692909135306_en-US.png)

그림을 보면 Security Traffic Manager(STM)이 그 역할을 하는데 정상트래픽은 MCA accelerate line을, 비정상트래픽은 Anti-DDos scrubbing center로 라우팅하는 역할을 한다. Anti-ddos 설정을 하다보면 Security Traffic Manager의 rule을 생성하고 나오는 CNAME을 DNS record에 추가하는 부분이 있는데, 이 설정을 통해 origin server에 라우팅되는 모든 트래픽이 STM을 먼저 거치게 되는 것이다. 

MCA설정은 이 [URL]([https://www.alibabacloud.com/help/doc-detail/92502.htm](https://www.alibabacloud.com/help/doc-detail/92502.htm))을 참고하길 바란다.

> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA4OTM3Njg3Myw0NjA1MTU4NzJdfQ==
-->