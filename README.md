# Weather Diary Service

사용자가 게시글을 업로드한 시점의 **날씨**와 **일기**를 적을 수 있는 서비스

</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 주체](#프로젝트-주체)
      - [💭 프로젝트 설명](#-프로젝트-설명)
      - [🛠 개발 조건](#-개발-조건)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)
  * [Troubleshooting](#troubleshooting)
  * [TIL](#til)


</br>

## 개발 기간
**2022.09.06 ~ 2022.09.07** : 기능 구현

**2022.09.12** : 버그 수정 및 테스트 코드  작성
</br>
</br>
  
## 프로젝트 개요


#### 프로젝트 주체 


![띵스플로우](https://user-images.githubusercontent.com/83492367/189649735-4498ba67-b27f-4653-850d-b4f42586547f.png)


[thingsflow](https://thingsflow.com/ko/home)

</br>

#### 💭 프로젝트 설명
사용자가 게시글을 업로드한 시점의 **날씨**와 **일기**를 적을 수 있도록

아래의 개발 조건을 만족하는 REST API 서버 개발

</br>

#### 🛠 개발 조건

> - `제목`과 `본문`으로 이루어진 게시글은 이모지를 포함할 수 있고 각 20자, 200자로 제한됨
> 	
> - 회원가입, 로그인 없이 `비밀번호`만 일치하면 수정·삭제가 가능하며 비밀번호는 암호화 되어야 함
> 	
> - `비밀번호`는 6자 이상이어야 하며 숫자 1개 이상 반드시 포함되어야 함
> 	
> - 모든 게시글은 최신글 순서로 확인 가능
> - 게시글은 20개 단위로 Pagination되어야 함
> - Weather API를 활용하여 게시글 등록시 날씨가 반영되어야 함

</br>

#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST framework
- **ETC** : Git, Github, Azure

</br>

#### 📰 모델링
![무제 2](https://user-images.githubusercontent.com/83492367/189656844-fd1224fa-a9cc-4bdc-8dbc-bafa28819f5a.jpg)

</br>

#### 🛠 API Test

요구사항을 바탕으로 한 15개의 테스트 구현



>     1. 본문(content)
>         1) 본문이 200자 초과할 때 : 실패
>         2) 본문이 200자 초과하지 않을 때 : 성공
>         3) 본문에 이모지 포함되어 있을 때 : 성공
> 
>     2. 제목(title)
>         1) 제목이 20자 초과할 때 : 실패
>         2) 제목이 20자 초과하지 않을 때 : 성공
>         3) 제목에 이모지 포함되어 있을 때 : 성공
> 
>     3. diary create시
>         1) 비밀번호가 6자 이하일 때 : 실패
>         2) 비밀번호가 6자 이상일 때 : 성공
>         3) 비밀번호가 문자로만 이루어져 있을 때 : 실패
>         4) 비밀번호가 1개 이상의 숫자로 이루어져 있을 때 : 성공
>         5) 비밀번호가 암호화 되어 있는지 확인
> 
>     4. diary update시
>         1) 비밀번호가 틀렸을 때 : 실패
>         2) 비밀번호가 맞을 때 : 성공
> 
>     5. diary delete시
>         1) 비밀번호가 틀렸을 때 : 실패
>         2) 비밀번호가 맞을 때 : 성공






</br>

## 프로젝트 분석
- **일기**를 중심으로 이에 대한 **CRUD**를 구현 (DRF의` Viewset` 이용)
- **비밀번호 암호화**를 위해  직접 알고리즘을 구현할 수 있지만, 보안과 관련된 만큼 검증된 `bcrypt `라이브러리 이용
	- 모델에서 **Password 필드 정의** 시 **Custom한 Validator**를 통해 비밀번호 조건을 검증
	- 비밀번호 유효성 검증은 S**erializer의 Create, Update method를 override**하여 구현
- **이모지**를 포함하기 위해 DB마다 다른 접근법이 요구됨을 확인
	- `Sqlite`, `PostgreSQL` : 이모지 포함 가능 ( 이번 프로젝트의 경우`Sqlite`, `PostgreSQL` 를 이용하므로 **설정 변경 없음**)
	-  `MariaDB` , `MySQL` : 4 byte로 이루어진 일반적인 `UTF-8` 과 달리 `UTF-8`인코딩시 각 char는 3 byte로 구성
		- 4 byte의 이모지를 저장하기 위해서는` UTF-8` 인코딩 방식 이용 불가
		- `UTF-8mb4 `인코딩 방식을 이용해야 함
- **게시글의 잦은 CRUD 작업**이 발생될 것을 판단하여 데이터의 중복 또는 누락을 막기 위해 `Cursor-base-Pagination`를 이용
-  `IP 주소`를 바탕으로 **사용자**마다 현재 지역의 **날씨 정보**를 가져옴
	- `XFF(X-Forwarded-For) HEADER` 로부터 IP 주소 가져옴
		- IP Spoofing 등의 보안상 이슈가 있음을 확인하였으나, 민감한 개인정보를 다루지 않으므로 괜찮다고 판단
		- IP 주소를 얻지 못하는 경우 `Seoul`를 기준으로 함
	
</br>

## API ENDPOINT


URL|Method|Action|Description|
|------|---|---|---|
|"api/v1/diaries"|GET|List|diary 전체 목록 조회|
|"api/v1/diaries"|POST|Create|diary 생성
|"api/v1/diaries/int:pk"|GET|Retrieve|diary 세부내역 조회
|"api/v1/diaries/int:pk"|PUT|Update|diary 세부내역 업데이트|
|"api/v1/diaries/int:pk"|PATCH|Partial_Update|diary 세부내역 업데이트|
|"api/v1/diaries/int:pk/"|DELETE|Delete|diary 삭제 불가능|
|"api/v1/diaries/int:pk/delete"|POST|POST|diary 삭제|

* Delete시 비밀번호 유효성 검증을 위해 `viewset`의 `Delete` 대신 POST 방식의` @action decorator `이용

</br>

## Troubleshooting


<details>
<summary>`암호화`에 대한 부족한 이해</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

- 초반에 Django에서 제공하는 기본 암호화 함수가 아니라 `Argon2`라는 라이브러리를 이용하여 암호화를 진행
-  최신 알고리즘인 만큼 문서가 부족하여 PasswordHasher() 함수에 대해 이해하는데 많은 시간을 소요함
- Password를 str 형태로 비교해야한다는 점을 알지 못해 이로 인한 시간을 낭비함
-  결국은 viewset의 문제점들로 대중적인 bcrypt를 이용하여 기능을 구현
-  과제를 마무리하기 위해 시간을 효율적으로 관리해야 할 필요성에 대해 체감

</details>

<details>
<summary>`Serializer`에서 유효성 검증의 어려움</summary>

<!-- summary 아래 한칸 공백 두어야함 -->


- 유효성 검증을 **Serializer**와 **View** 중 어느 수준에서 진행해야 하는지에 대해 많은 시간 소요
	- View에서는 perform_create, perform_update, perform_destory 등 인스턴스를 DB에 처리하는 로직을 가지고 있을 뿐
	- DRF의 Source Code를 참고했을때 실질적인 데이터의 유효성 검증 및 생성은 Serilizer에서 진행된다고 판단
	- Serializer에서는 Create시, Update시에만 유효성 검증 가능 
		- Delete Serializer를 따로 구현하여 Update method 로직을 바꿔 Delete method로 이용하려했으나 실패
		-  **기간안에** **Delete시 유효성 검증에 대한 적절한 방법을 찾지 못함**
			- 후에 @action decorator를 이용하여 delete하도록 변경하여 기능 구현

- 유효성 검증이라는 Serializer의 기능에 대한 이해 부족으로 판단되어 추후 학습 예정
			
</details>


<details>
<summary>`Viewset`의 단점</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

- 반복되는 코드를 줄이고자 Viewset을 이용하여 CRUD를 구현하였으나, 각 method에 대한 정확한 이해가 부족
-  특히 Viewset의 Destory method는 유효성을 검증하는 로직이 없음을 확인하는데 오랜 시간을 소요함
-  Viewset 대신 Apiview를 이용할 필요성에 대해 체감,  API v2를 Apiview를 이용하여 추후 구현 예정


</details>

</br>

## TIL

- [[TIL] Django에서 IP 주소 가져오기 (Feat. XFF 헤더)](https://medium.com/@heeee/til-django%EC%97%90%EC%84%9C-ip-%EC%A3%BC%EC%86%8C-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0-feat-xff-%ED%97%A4%EB%8D%94-52acd7274139)



