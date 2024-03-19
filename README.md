# 파워리프팅 대쉬보드 및 사용자 역량 분석

## 개요
파워리프팅 선수들의 3대운동 역량 데이터를 분석하여 사용자의 운동 역량 향상에 도움이 되는 정보를 제공하는 앱을 제작하였습니다. 사용자는 자신의 운동 역량 수준과 목표로 하는 체급을 달성하기 위한 계산기등을 제공받을 수 있습니다.

## 기능

1. 성별 분포
![c81df016847a0489b0341ce07b80e9806e39b0a8e1f11aa82a1a1b21](https://github.com/mins1120/powerlift_dashboard/assets/162934135/057f6fd9-908d-4319-9c4e-3fdd5b726265)
데이터 셋에 있는 성별의 분포도를 시각화 했습니다.

2. 체급별 최고 성적
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/0360a375-c1a4-4307-84f6-ff9e577ab7b8)
데이터 셋에 있는 체급에서의 최고 3대 중량 분포를 시각화 했습니다. 체급 별로 그래프를 보기 위해 체급을 검색하면 그에 따른 그래프가 출력되도록 작성했습니다.

3. 연령대별 성적 분포
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/8905c51b-c386-4ee4-b2e6-9fe3f387632d)
연령대별 평균 3대 중량 분포를 시각화 했습니다. 체급과 같이 연령대를 검색하는 기능을 추가했습니다.

4. 장비별 성적 분석
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/70e9f625-ba55-417b-b740-036c16f4f613)
장비별 평균 3대 중량 분포를 시각화 했습니다. 다른 기능들과 같이 원하는 장비를 검색할 수 있도록 했습니다.

5. 성별 및 체급별 Wiklks 점수 평균 분포
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/73c6d01d-53b3-4709-9c39-c04ee0561ebd)
성별별 체급에 대한 그래프를 시각화 했습니다. 남성과 여성으로 구분되어 그래프를 골라서 볼 수 있도록 했습니다.

6. Wilks 점수에 따른 성능 비교
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/db86bd39-f68d-480f-966a-4fc72504f00f)
Wilks 점수에 따른 성능 비교를 데이터 프레임 형태로 출력했습니다. 성별과 보고 싶은 Wilks 점수를 입력하면, 근사값인 프레임 10개가 출력되도록 진행했습니다.
 
7. 개인 성적 분석 및 조언
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/956651b1-e86e-4c79-84ec-bd57012d5143)
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/df2b0300-4c66-4180-a4e9-57cc1c1af755)
개인 성적을 분석하고 조언해주는 부분을 구현했습니다.

8. 개인 데이터 제공 동의
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/c81a6b6a-4169-422c-9aac-0105034d8bd3)
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/db3c44a4-dab6-40da-be03-270afb0992fc)
해당 데이터셋은 운동 선수들의 데이터를 이용한 분석이지만, 사용자들은 대부분 일반인들일 가능성이 높을 것 같아 일반인 사용자들을 위한 데이터셋을 구축하기 위해서 사용자들의 데이터를 새로운 데이터 셋에 저장하고 싶었습니다. 그래서 일단 사용자의 데이터를 입력받고 이를 새로운 데이터 셋에 저장하는 기능을 구현하였습니다.

9. 기초대사량 계산기
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/ed432cd0-d47a-499c-a0ea-50b83145163f)
![image](https://github.com/mins1120/powerlift_dashboard/assets/162934135/678266a7-80ac-4437-9e7a-7c3b61148a9b)
사용자에게 데이터를 그냥 제공해달라고 하면 제공해주지 않을 것 같아서, 데이터 제공을 유도하기 위한 기초대사량 계산기를 구현했습니다. 사용자가 데이터 제공을 하면, 계산기 함수가 발동되도록 st.session_state 메서드를 이용해 구현하였습니다.

