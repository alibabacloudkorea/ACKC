---


---

<h1 id="alibaba-cloud-devops-flow를-이용하여-alibaba-cloud에-최적화된-devopscicd-환경-구현하기">Alibaba Cloud DevOps Flow를 이용하여 Alibaba Cloud에 최적화된 DevOps(CI/CD) 환경 구현하기</h1>
<h2 id="배경--설명">1. 배경  설명</h2>
<p>비즈니스가  다양한  형태로  확장되면서  우리의  IT 환경의  다양성도  증가하고  있다.</p>
<p>같은  기업, 같은  팀에서  조차  업무의  특성에  따라  서로  다른  플랫폼, 툴  심지어는  클라우드  환경마저  다른  환경을  사용하고  있다.</p>
<p>하지만  대부분의  기업은  Legacy한  개발  환경과  프로세스를  그대로  유지하고  있다. 이  두가지의  간극으로  기업들은  큰  투자로  도입한  혁신적인  플랫폼을  효율적으로  사용하지  못하고  있다.</p>
<p>이러한  문제를  해결할  수  있는  프로세스의  혁신이  바로  DevOps이다. DevOps의  핵심  3요소(People, Process, Technology) 중  Technology(기술)의  영역, 즉  <strong>CI/CD의  구현이  필수가  되었다.</strong></p>
<p>오늘  이  글에서  우리는  Alibaba Cloud의  DevOps 플랫폼인  <strong>FLOW</strong> 에  대해서  알아보도록  하겠다.</p>
<h2 id="solution-overview">2. Solution Overview</h2>
<p><img src="https://user-images.githubusercontent.com/34003729/130347804-f8325a20-c321-4545-8d0a-0f009f7ed732.png" alt="image"></p>
<p><a href="https://www.alibabacloud.com/help/doc-detail/210075.htm?spm=a2c63.p38356.b99.3.34263e4frG6VGv"><strong>Alibaba Cloud DevOps Flow</strong></a>(이하 Flow)는  Alibaba Cloud에서  제공하는  DevOps SaaS 플랫폼이다. 비슷한  서비스를  제공하는  오픈소스로는  <a href="https://www.jenkins.io/">Jenkins</a>, <a href="https://www.atlassian.com/ko/software/bamboo">Bamboo</a>, <a href="https://argoproj.github.io/argo-cd/">ArgoCD</a> 등이  있다.</p>
<p>기본적으로, 모든  CI/CD Step을  아래  캡쳐와  같이  GUI로  제공하고  있으며  특정한  스크립트  언어, 구체적인  사용법을  몰라도  쉽게  접근하고  사용할  수  있다.</p>
<blockquote>
<p>전통적인  CI/CD툴들은  대부분  특정한  script 언어를  사용하며  구성이  어렵다.</p>
</blockquote>
<p><img src="https://user-images.githubusercontent.com/34003729/130347845-35dbf3ca-f007-43bf-b1fc-3855d47d3614.png" alt="image"></p>
<h2 id="solution-기능--설명">3. Solution 기능  설명</h2>
<h3 id="용어">3.1 용어</h3>
<ul>
<li><strong>Source</strong> : Git repository 같은 Delivery 도구</li>
<li><strong>Phase</strong> : Pipeline에서  실행되는 Task의  모음, 자동  혹은  수동으로  실행  가능, 2개의 phase를  연속적으로  실행  가능</li>
<li><strong>Task</strong> : 실제 action, 2개의 task는  동시에  실행되거나  연속적으로  실행할  수  있음 / 보통 Task는 code scanning, unit test, building, deployment, code merging, manual approval 등을  포함 / Agent task, agent less task 두 종류가  존재</li>
<li><strong>Step</strong> : Flow의  핵심  기본  기능으로 실제 Operation이 포함</li>
</ul>
<h3 id="장점">3.2 장점</h3>
<ul>
<li>Easy Deployment : workspace를  만들고  몇 분  후에 바로 pipeline 사용  가능</li>
<li>Simple management : GUI로  간편하게  파이프라인  관리</li>
<li>Tenant Isolation : Multiple workspace를  만들어서  서로간의  격리  가능</li>
<li>High stability and reliability : Multiple zone에  배포  가능</li>
<li>Various supported pipeline sources : Github, Gitlab 등  DSCM과의  통합</li>
<li>Guaranteed business delivery with high quality : Code scanning, security scanning, Unit test 등  기업  환경에  맞는  기능  제공</li>
</ul>
<h3 id="기능">3.3 기능</h3>
<h4 id="pipeline-source">3.3.1 Pipeline Source</h4>
<p>Pipeline을  시작하기  위한  Source Code Repository를  정의한다. 기본  설정으로  GitHub과  General Git를 사용  가능하다</p>
<blockquote>
<p>GitHub은  사용자의  계정을  연결하여  Repository에  대한  Credential을  처리할  수  있으나, General Git은  옵션에서  Key 등을  설정해야  한다</p>
</blockquote>
<p><img src="https://user-images.githubusercontent.com/34003729/130347857-0a193192-3deb-4af3-a84a-ac48d768604b.png" alt="image"></p>
<h4 id="tasks">3.3.2 Tasks</h4>
<p>Task는  Alibaba Cloud에서  제공하는  각  CI/CD Step에서의  필요한 Action을  정의한다.</p>
<p>Alibaba Cloud에서는  다양한  CI/CD Task를  Pre-define하여  제공하며  아래  대표적인  Task 들에  대해  설명을  하겠다.</p>
<h4 id="java-code-scan">3.3.2.1 Java Code Scan</h4>
<p>Java Source에  대한  Code scanning을  수행한다. Alibaba Cloud에서  제공하는  Script를  이용하여  각  코드에  있는  위험도  높은  code를  분석하여  리포트를  제공한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130347876-b8a4b559-9267-4c2e-8f75-76a48bcaf458.png" alt="image"></p>
<ul>
<li><em>Task Name</em> : 모든  Task에  포함되며  Task의  subject를  정의</li>
<li><em>Build Cluster</em> : Cluster가  포함된  region을  정의</li>
<li><em>Step Name</em> : Task에  포함될  Step의  subject를  정의</li>
<li><em>JDK Version</em> : JDK 버전  선택</li>
<li><em>Maven Version</em> : Maven Version 선택</li>
<li><em>Enable Incremental Scan</em> : Incremental Scanning 정책  사용</li>
<li><em>Use Custom Rule</em> : 사용자의  code repository에  있는  p3c rule file 사용</li>
<li><em>Sub Folder</em> : Repository에서  검증할  directory를  정할  때  사용, 빈칸일  경우  root directory 사용</li>
<li><em>Excluded Folder</em> : Scanning에  포함하지  않을  directory를  정의</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130347895-cefda870-85a4-47e2-895b-47518b7839ec.png" alt="image"></p>
<blockquote>
<p>파이프라인이  수행된  후  Code Scanning 보고서를  참조할  수  있다. 어떤  소스코드에서  이슈가  있는지  상세히  파악할  수  있다</p>
</blockquote>
<h4 id="maven-unit-test">3.3.2.2 Maven Unit Test</h4>
<p>Maven을  이용한  Unit Test진행을  위해  옵션을  설정한다</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130347911-43ac8a6c-7ce2-467a-9d2d-241d5e76575d.png" alt="image"></p>
<ul>
<li><em>JDK Version / Maven Version</em> : JDK와  Maven의  버전을  선택</li>
<li><em>Test Command</em> : Test에  사용할  Command를  정의, 기본적으로  surefice를  이용한  리포팅을  제공</li>
<li><em>Test Report Folder</em> : Test리포트를  저장할  폴더  정의</li>
<li><em>Test Report Entry File</em> : Test report entry file을  정의</li>
</ul>
<h4 id="java-build">3.3.2.3 Java Build</h4>
<p>Java 소스코드에  대한  Build를  수행하는  Task이며, 기본  셋팅에서는  Maven build를  사용한다. Flow에서  제공하는  Java Build를  사용하면  개발  배포시  별도의  빌드  서버를  이용하지  않고  쉽게  빌드를  수행할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130347931-8e172bfa-86c1-4029-8fa2-9480e52391d2.png" alt="image"></p>
<ul>
<li><em>JDK Version</em> : Java 빌드에  사용할  JDK 버전을  정의</li>
<li><em>Maven Version</em> : Maven 버전을  정의</li>
<li><em>Build Command</em> : 빌드를  수행할  때  입력할  커맨드를  커스터마이징, mvn 옵션  등을  정의하는  데  사용</li>
</ul>
<h4 id="java-image-build">3.3.2.4 Java Image Build</h4>
<p>주로  컨테이너  배포를  할  때  사용된다. 보통  로컬  환경에서  컨테이너  배포할  때, 개발자는  Base Image를  registry에서  pull한  후  자바  빌드를  수행한다. 그  이후  빌드한  라이브러리와  Base Image를  병합하여  실제  운영할  이미지를  만든다.</p>
<p>Java Image Build를  사용하게  되면  사용자는  별도의  빌드  서버나  Docker build를  수행하지  않아도  쉽게  소스코드를  컨테이너  이미지로  만들  수  있다.</p>
<blockquote>
<p>Configuration에  포함되는  Java Build는  위의  내용과  같다</p>
</blockquote>
<p><img src="https://user-images.githubusercontent.com/34003729/130347956-9e04097e-5eb4-45c1-90f6-9e663e91f071.png" alt="image"></p>
<p>먼저  Docker build를  위한  Alibaba Cloud의  Container Registry 서비스인  ACR 빌드의  옵션을  정의한다.</p>
<ul>
<li><em>Choose Service Connection</em> : ACR 서비스와  credential을  연결할  서비스  선택</li>
<li><em>Region</em> : ACR을  사용할  리전  선택</li>
<li><em>Repository</em> : 기  배포된  ACR의  Repo 선택, 생성이  되어있지  않다면  +로  생성  가능</li>
<li><em>Dockerfile Path</em> : 이미지를  배포할  때  참조할  Dockerfile Path 입력</li>
<li><em>Context Path</em> : Docker build command입력할  때의  Context path 입력</li>
<li>No Cache : 만약  체크된다면  docker build의  –no-cache=true 옵션  사용</li>
</ul>
<h4 id="ecs-deployment">3.3.2.5 ECS Deployment</h4>
<p>배포할  때  사용할  ECS에  대해서  정의한다. 설정에  따라  다수의  ECS에  배포할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130347978-2764fdc3-8675-40a3-9023-6c9784223651.png" alt="image"></p>
<ul>
<li><em>Artifact</em> : Artifact Name 정의</li>
<li><em>Deployment Group</em> : Deployment Group 정의</li>
<li><em>Download path</em> : Host에서  다운로드  할  Artifact Path를  정의, 빈칸은  Download 없음을  표시</li>
<li><em>Execute User</em> : ECS에서  실행될  User 정의</li>
<li><em>Deployment Script</em> : ECS/VM을  배포할  때  사용할  Script</li>
<li><em>Suspend Strategy</em> : Suspend First Batch, Suspend Per Batch 또는 Without Suspension과  같은  호스트  그룹에서  사용되는  일시  중단  방법에  대한  선택. Suspend First Batch를  권고</li>
<li><em>Batches</em> : 호스트  그룹의  시스템을  나눌  배치  수  정의</li>
</ul>
<h4 id="kubectl-apply">3.3.2.6 Kubectl Apply</h4>
<p>배포에  Kubernetes를  이용할  경우에  Kubectl Apply task를  적용할  수  있다. 배포할  때  단일  컨테이너를  사용할  수도  있지만  요구사항에  따라  Blue/Green이나  Canary 배포를  이용할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130347997-02e0203d-d1fe-4a19-8587-5268f7523602.png" alt="image"></p>
<ul>
<li><em>Service Connection</em> : 배포될  Kubernetes와  연결될  Service Connection 선택</li>
<li><em>Kubectl Version</em> : 배포될  Kubernetes 버전  선택</li>
<li><em>Namespace</em> : 컨테이너가  배포될  Namespace 정의</li>
<li><em>YAML PATH</em> : 배포시  사용할  YAML file path를  정의, 주로  manifests file을  사용</li>
<li><em>Use Replace Mode</em> : ‘kubectl apply’ 대신 'kubectl install’을  사용하여  대상  리소스를  생성할  때  대체  모드  사용</li>
<li><em>Skip TLS Validation</em> : Kubernetes 구성에서 'insecure-skip-tls-verify’가 true로  구성된  경우  사용</li>
</ul>
<h4 id="manual-approval">3.3.2.7 Manual Approval</h4>
<p>배포시  특정  작업에  대한  승인  절차가  필요할  때  사용한다. 기본적으로  FLOW에  등록된  Account에서  승인을  처리할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348013-297a2f18-a18b-4002-97a8-36a7b20d0ca2.png" alt="image"></p>
<ul>
<li><em>Validation Method</em> : 승인할  User의  그룹을  선택  (Anyone / All)</li>
<li><em>Validator Type</em> : 승인권자의  Type을  선택  (User / Tenant Role)</li>
</ul>
<blockquote>
<p>그  밖에  Blue-green deployment, Node.js build / test, Execute command, 커스텀  이미지  레포토리  빌드 등의 Task를 이용할 수 있다.</p>
</blockquote>
<h4 id="추가--기능">3.3.3 추가  기능</h4>
<p>FLOW의  콘솔에서는  사용자의  파이프라인  관리를  위해  다양한  추가  기능을  제공한다.</p>
<h4 id="webhook-trigger">3.3.3.1 WebHook Trigger</h4>
<p>사용자는  WebHook Trigger를  이용해  GIT repository와  CI를  긴밀하게  연결할  수  있다. 메뉴에서  표시되는  API를  GIT의  Webhook에  추가해주면  쉽게  사용할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348026-bd45bcc6-2a4d-4733-8db2-3a89f9dbf2d6.png" alt="image"></p>
<h4 id="scheduled-trigger">3.3.3.2 Scheduled Trigger</h4>
<p>주로  PM 같은  정기적인  작업시  파이프라인  실행을  자동화하는  기능이다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348043-a0543cd6-d7fc-4274-96dc-f0cba37aaa00.png" alt="image"></p>
<h4 id="variable">3.3.3.3 Variable</h4>
<p>파이프라인  환경에서  변수로  사용할  Object를  정의한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348070-5fae3322-cfc3-4597-9514-9e065ff44269.png" alt="image"></p>
<h4 id="cache">3.3.3.4 Cache</h4>
<p>파이프라인  배포시  속도를  가속화하기  위해  캐싱  기능을  이용한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348084-08a8d41a-be3e-4b56-86ba-95793c85dcc1.png" alt="image"></p>
<h2 id="테스트--배경--및--요구사항">4. 테스트  배경  및  요구사항</h2>
<p><a href="https://flow.alibabacloud.com/">Alibaba Cloud DevOps FLOW</a> 에  접속하면  Alibaba Cloud International 계정으로  Workspace를  만들  수  있다. 이를  이용해  쉽게  파이프라인  환경을  구성할  수  있다.</p>
<p>5번  항목에서부터, 아래의  특정  조건을  가진  고객이  있다고  가정하고  GitHub에  저장된  소스코드를  이용하여  ECS Single Instance 배포를  하는  파이프라인을  만드는  가이드를  확인할  수  있다.</p>
<h3 id="배경">4.1 배경</h3>
<p>예시 환경에서는 아래와 같은 배경을 가지고 있다.</p>
<ul>
<li>Code development in Java</li>
<li>Delivery in the JAR or WAR format</li>
<li>Execution on ECS or a self-managed host</li>
</ul>
<h3 id="요구사항">4.2 요구사항</h3>
<p>예시 환경 구현에 필요한 기술적 요구사항은 다음과 같다.</p>
<ul>
<li>Perform some quality checks on the source code such as unit testing and code scanning.</li>
<li>Build source code into a deliverable such as a JAR or WAR file.</li>
<li>Publish a deliverable to an ECS virtual host</li>
</ul>
<h2 id="main-steps">5. Main Steps</h2>
<p>본  예시에서는  크게  4단계의  파이프라인을  구성할  것이다.</p>
<p><em><strong>GitHub Repository연결 &gt; Java Code Scan / Maven Unit Test &gt; Java Build &amp; Archive &gt; ECS 배포</strong></em>  순으로  구성하는  방법을  확인할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348103-8e41c344-eb21-4abb-ab36-502c3c19f8c0.png" alt="image"></p>
<blockquote>
<p>예시  소스코드는  <a href="https://github.com/Jason-Jongjin-Lim/Flowtest">https://github.com/Jason-Jongjin-Lim/FLOWtest</a> 에서 Folk할  수  있다.</p>
</blockquote>
<h3 id="flow-접속--및--create-pipeline">5.1 FLOW 접속  및  Create Pipeline</h3>
<p><a href="https://flow.alibabacloud.com/">FLOW Console</a>에  접속하고  Workspace를  만들면  아래와  같은  화면을  확인할  수  있다. 여기서  우리는  파이프라인을  구성하기  위해  <em>Create Pipeline</em>을  선택한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348127-3bb3def1-8d23-4910-9c73-21ef73c31320.png" alt="image"></p>
<h3 id="template-확인--및--선택">5.2 Template 확인  및  선택</h3>
<p><em>Create Template</em>을  선택하면  기  정의되어있는  Template list를  확인할  수  있다. 우리는  여기서  첫번째  Template을  이용하여  설정할  것이다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348153-a9cccb9d-8ee6-4d38-b467-e1f3d74284d6.png" alt="image"></p>
<h3 id="add-pipeline-source">5.3 Add Pipeline Source</h3>
<p>본  가이드에서는  Pipeline Source로  GitHub을 사용할  것이다. 먼저, FLOW에  <em>GitHub 계정을  Associate</em>한  후  아래  가이드를  따라  설정할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348177-7d13170b-cf39-4ef7-8b7e-fd9bcf4b6a3d.png" alt="image"></p>
<ul>
<li><em>Namespace</em> : GitHub에서  사용할  Namespace 선택</li>
<li><em>Repository</em> : Namespace에서  배포할  소스코드가  있는  Repository 선택</li>
<li><em>Default Branch</em> : 배포할  Branch 선택</li>
<li><em>Clone Submodule / Custom Clone Depth</em> : False 선택</li>
</ul>
<h3 id="source-trigger-추가">5.4 Source Trigger 추가</h3>
<p><em>Enable Code Source Trigger 옵션</em>을 켜면 Git 프로세스에서 제공하는  Webhook 기능을  이용하여  파이프라인을  자동으로  시작할  수  있다. 본  옵션  설정  이후에  개발자는  <strong>Commit/Push의  동작  만으로  파이프라인을  실행</strong>한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348202-521cf590-4d02-4bf1-8962-76cec383cbc3.png" alt="image"></p>
<ul>
<li>기능을  Enable하고  Webhook API를  복사</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348232-b52903c1-4666-4496-ab7b-46e101b5e317.png" alt="image"></p>
<ul>
<li>복사한  API를  <em>GitHub Repository &gt; Settings &gt; Webhook &gt; Payload URL</em>에  입력</li>
</ul>
<h3 id="java-code-scan-설정">5.5 Java Code Scan 설정</h3>
<p>샘플  자바코드의  잠재적  이슈를  확인하기  위한  스캐닝  정책을  설정한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348276-3026451b-bec2-4b35-87a4-783e7bf0faa9.png" alt="image"></p>
<blockquote>
<p>본  예시에서는  기본  옵션을  사용한다. 특별히  사용하는  JDK, Maven 버전이  있으면  지정할  수  있다</p>
</blockquote>
<h3 id="maven-unit-test-설정">5.6 Maven Unit Test 설정</h3>
<p>Maven Unit Test를  위해  옵션을  지정한다. 본  시나리오에서  사용하는  예제로  surefire를  이용한  리포팅  기능을  사용할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348294-f085f8cd-5d33-46e5-84c5-48e0ed8650aa.png" alt="image"></p>
<blockquote>
<p>본  예시에서는  기본  옵션을  사용한다.</p>
</blockquote>
<h3 id="build-archive-task-설정">5.7 Build, Archive task 설정</h3>
<p>Java build를  위해  각  옵션들을  지정한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348364-0745be98-f3e9-4680-a600-a288d6517a41.png" alt="image"></p>
<ul>
<li>나머지는  기본  옵션을  사용하며  <em>Archive Paths에  deploy.sh를  추가</em>해준다. 이  스크립트는  배포할  때  아카이브로  압축되어  ECS에  저장된다.</li>
</ul>
<h3 id="ecs-deployment-설정">5.8 ECS Deployment 설정</h3>
<p>ECS로  배포할  때  사용할  옵션을  지정한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348418-5c74627c-2f02-4345-a3f0-a4802ee776e5.png" alt="image"></p>
<ul>
<li>배포시  사용할  ECS의  그룹이  필요하다. 이를  위해  <em>Create Deployment Group</em>을  클릭한다.</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348471-516fb9b4-04de-4e47-9e2c-e8488059245c.png" alt="image"></p>
<ul>
<li>팝업창에서  <em>Service Authorization을  생성</em>하고  배포할  Region을  선택한다.</li>
<li>배포  서버로  사용될  <em>Instance를  선택</em>한다. 다수의  인스턴스도  선택이  가능하다.</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348490-1af3f527-f3d0-44bb-901f-cff2773fe329.png" alt="image"></p>
<ul>
<li>다음  Step에서는  선택한  Server Group이  사용될  Group Environment와  Tag를  지정한다. 본  환경에서는  <em>Daily Environment를  사용</em>할  것이다</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348504-e909c539-2528-4f89-b28c-b32b6ee4b97e.png" alt="image"></p>
<ul>
<li>
<p>Deployment Script에  Archive로  저장한  package의  압축을  해제하고  Deploy.sh를  실행하는  스크립트를  심어준다.</p>
<p><code>mkdir -p /home/admin/application/</code><br>
<code>tar zxvf /home/admin/app/package.tgz -C /home/admin/application/</code><br>
<code>sh /home/admin/application/deploy.sh restart</code></p>
</li>
</ul>
<h3 id="save-and-run">5.9 Save and Run</h3>
<p>파이프라인  작성이  완료되면  FLOW Console 우측  상단의  <em>Save and Run</em>을  수행한다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348551-240548c4-a07e-4674-8908-6844be70f16d.png" alt="image"></p>
<h3 id="진행--확인">5.10 진행  확인</h3>
<p>파이프라인을  실행한  후  FLOW Console의  Dashboard에서  파이프라인  진행  상황에  대해  여러가지  정보를  확인할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348560-61832810-54ee-4edb-9dc4-65159ceb1b60.png" alt="image"></p>
<ul>
<li>좌측  패널에서  파이프라인을  실행한  User, 실행  시간, Source, 변수  등에  대한  기본  정보  확인  가능</li>
<li>Pipeline 패널에서  각  Step에  대한  로그, 리포트  등  세부  정보  확인  가능</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348594-489081c5-eed6-4995-9412-3be6b46fcf41.png" alt="image"></p>
<ul>
<li>각  Step을  클릭하면  세부  정보와  프로세스, Status를  확인  가능</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348615-0fbfc07c-60b3-4db7-a62e-35ad832d757f.png" alt="image"></p>
<ul>
<li>Java Build Step에서  Log를  클릭하면  각  Build step의  Log 정보  확인  가능</li>
</ul>
<p><img src="https://user-images.githubusercontent.com/34003729/130348892-2f76ade5-47d5-495b-9738-a114a682bfde.png" alt="image"></p>
<ul>
<li>파이프라인이 종료되게 되면 상태창에 모두 <strong>Complete</strong>으로 표시</li>
</ul>
<h2 id="트러블--슈팅">6. 트러블  슈팅</h2>
<p>파이프라인을  진행하다  보면  다양한  Step에서  문제가  발생한다. 그  문제가  발생한  Step의  <em>Detail page</em>를  확인하면  상세  정보, Log, Retry, Skip 등의  트러블  슈팅을  할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348908-5af306fe-9afd-4eef-835f-3326bcf53e66.png" alt="image"></p>
<p>또한  <em>Running History</em>에서  이전에  실행했던  파이프라인의  상태를  확인할  수  있다.</p>
<p><img src="https://user-images.githubusercontent.com/34003729/130348915-7e31c7be-61a8-4ca8-9f44-5c9aa276c95e.png" alt="image"></p>
<h2 id="결론">7. 결론</h2>
<p>지금까지  Alibaba Cloud DevOps FLOW에  대해  알아보았다.</p>
<p>물론  현재  많이  쓰이고  있는  Pipeline 툴인  Jenkins, Bamboo 등에  비해서  Plug-in 등이  많이  지원되지  않아  복잡한  DevOps 환경을  사용하는  기업  사용자에게는  조금  가벼워  보일  수  있다.</p>
<p>하지만  Alibaba Cloud를  사용하는  고객  중 Java나  Node.js 기반의  심플한  서비스를  운영하는  고객이라면  <strong>소스코드  개발  후  Commit/Push만으로  빌드, 테스트, 승인, 인스턴스와 컨테이너로 배포  등을  자동화하여  할  수  있으므로  무거운  Pipeline 툴보다  더  적합한  솔루션</strong>이라고  할  수  있다.</p>

