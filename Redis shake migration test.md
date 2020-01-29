# Redis shake migration test

Redis shake는 알리바바에서 개발하는 오픈소스 마이그레이션 툴이다. 본 테스트는 redis 마이그레이션을 위해 수행했지만 redis 뿐만 아니라 mongodb도 지원한다. 

# 테스트 목적
테스트를 진행한 이유는 고객이 알리바바 클라우드 China console에서 International console로 마이그레이션을 하는데 최소한의 다운타임을 가져가는 것을 원해서라고 할 수 있다. 레디스를 온라인 상 마이그레이션하는 방법은 다음과 같다.

- DTS(Data Transmission Service): Source/Target 모두 Redis Cluster Edition을 지원하지만 어카운트 간 마이그레이션은 지원하지 않는다. 

	테스트 차 Target instance type을 User-Created Database Connected Over Express Connect ---" 로 해보았으나 연결은 되지 않았다. 수 차례 테스트 결과 단순히 두 VPC간 마이그레이션과는 다르게 RAM 계정에서의  적절한 권한을 주고 target instance에서 DTS private IP list를 whitelist에 넣어주는 등의 작업이 필요하다. 그 작업을 다 해도 결국 연결은 되지 않았다. 

	결론은.. DTS가 account간 마이그레이션을 지원할 때까지 기다려야 한다. 당장은 지원 예정에 없다. 
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-29%20at%205.15.58%20PM.png?raw=true)

	![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-29%20at%205.18.59%20PM.png?raw=true)


- Redis Shake를 통한 마이그레이션 
sync mode와 rump모드가 있고 sync mode로 이관 시 온라인 마이그레이션이 가능하다. 하지만 현재 sync mode에서 Apsara redis cluster edition DB를 지원하지 않는다.

따라서 본 테스트는 redis cluster이 얼마만큼 간단하고 빠르게 수행되는지, online migration을 위한 incremental migration이 진행되는지를 확인하는 것이 목적이다. 

# 테스트 환경
- Source DB: 
	- Region: China (Hong Kong)
	- Zone: Hong Kong MZone1 B+C
	- Redis version: 4.0
	- Architecture Type: Cluster
	- Instance Class: 1G (2 shards with 2 replicas)
	- Package Type: Standard Package
	- Account: Aliyun (China Cloud Account)
- Target DB
	- Region: China (Hong Kong)
	- Zone: Hong Kong MZone1 B+C
	- Redis version: 4.0
	- Architecture Type: Cluster
	- Instance Class: 1G (2 shards with 2 replicas)
	- Package Type: Standard Package
	- Account: International account
- NW configuration
	- CEN을 통한 vpc peering이 된 상태다. 즉, 네트워크는 알리바바 private 망으로 구성되었다 할 수 있다.
# 테스트 시나리오
1. Redis Shake with "sync" mode 
	- Online 상 마이그레이션 가능
	- 현재 Redis Cluster Edition은 소스로 지원하지 않는다. 하지만 테스트 차 돌려보았다.
2. Redis Shake with "rump" mode
	- Data consistency를 위해 DB 중단 후 사용하는 것이 좋음. 즉 오프라인 마이그레이션 용
	- 럼프 모드에서 redis-shake는 SCAN 모드의 소스 Redis에서 전체 데이터 양을 가져 와서 대상에 쓰고 데이터 마이그레이션을 구현함. 이 마이그레이션 방법은 SYNC 또는 PSYNC를 사용하지 않으며 Redis 서비스 성능에 거의 영향을 미치지 않는다. Redis 클러스터를 지원하는데 이는 클라우드 DB든, 자체 구축 DB든 모두 지원한다. 
	- 럼프 모드는 버전 2.8 인스턴스를 버전 4.0 인스턴스로 마이그레이션하는 것과 같이 버전 간 마이그레이션을 지원함.
	- redis-shake에 대한 자세한 내용은 [redis-shake Github 홈페이지](https://github.com/aliyun/redis-shake?spm=a2c4g.11186623.2.10.10776f10RwLL6e) 또는 [FAQ](https://github.com/alibaba/RedisShake/wiki/%E7%AC%AC%E4%B8%80%E6%AC%A1%E4%BD%BF%E7%94%A8%EF%BC%8C%E5%A6%82%E4%BD%95%E8%BF%9B%E8%A1%8C%E9%85%8D%E7%BD%AE%EF%BC%9F?spm=a2c4g.11186623.2.11.10776f10RwLL6e)를 참조하십시오.

> Note: 어차피 redis shake의 sync모드가 redis DB 엔진의 sync와 psync command를 바탕으로 하기 때문에 내부적으로 해당 코멘드가 실행 가능한지 ticket을 통해 물어보았다. 답변은 아직 진행 중이다.

# 테스트 내용
1. Redis Shake with "sync" mode
souce.type 에 proxy를 지정해야 하는데(Apsara Redis가 proxy 구성이기 때문) proxy는 현재 rump mode에서만 지원가능하다는 에러가 나옴. 따라서 해당 기능이 제공되는 새로운 버전이 나올 때 까지 기다려야 함. 
2. Redis Shake with "rump" mode
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-29%20at%204.51.16%20PM.png?raw=true)
데이터가 적어서 그런지 금방 수행되었다.

	설정 방법은 [aliyun documentation]([https://help.aliyun.com/document_detail/117311.html?spm=a2c4g.11186623.6.699.33f57892h0NAy9](https://help.aliyun.com/document_detail/117311.html?spm=a2c4g.11186623.6.699.33f57892h0NAy9))과 [github - how to setup]([https://github.com/alibaba/RedisShake/wiki/tutorial-about-how-to-set-up#32-example-cluster-to-cluster-sync](https://github.com/alibaba/RedisShake/wiki/tutorial-about-how-to-set-up#32-example-cluster-to-cluster-sync))을 참고했다.

# 테스트 결과

아래는 aliyun account의 source DB다. learderboard key에 1000개의 레코드가 있다.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-29%20at%202.22.47%20PM.png?raw=true)

아래는 international account의 target DB이다. 하나의 키와 1000개의 레코드가 잘 마이그레이션 된 것을 확인할 수 있다.
![](https://github.com/rnlduaeo/alibaba/blob/master/Screen%20Shot%202020-01-29%20at%204.50.44%20PM.png?raw=true)






<!--stackedit_data:
eyJoaXN0b3J5IjpbMTI1NjYwMTgxNyw4MTU4MzA3MjcsODU0ND
g4MzMsLTU2Mzk4NTIwNl19
-->