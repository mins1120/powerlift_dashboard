import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os

## 운영 체제별 폰트 설정
system_name = platform.system()
if system_name == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif system_name == 'Darwin':
    plt.rc('font', family='AppleGothic')
elif system_name == 'Linux':
    plt.rc('font', family='NanumGothic')


## 평균을 계산하는 함수
def calculate_averages(data, columns):
    return data[columns].mean()

## 기초 대사량 계산기 함수
def bmr_calculator():
    with st.expander('기초대사량 계산기'):
        st.write('(헤레딕트 방정식 기준)')
        # 활동 수준에 따른 총 에너지 소모량(TDEE) 계산 딕셔너리 정의
        activity_levels = {
            "거의 활동 없음(좌식 생활 및 운동 X)": 1.2,
            "가벼운 활동(활동량 보통 및 운동 1~3회)": 1.375,
            "보통 활동(활동량 보통 및 운동 주 3~5회)": 1.55,
            "활발한 활동(활동량 많거나 운동 주 6~7회)": 1.725,
            "매우 활발한 활동(활동량 매우 많거나 운동 매일 2회)": 1.9
        }
        # 사용자 입력 받기
        bmr_gender = st.radio("성별을 선택하세요.", ('남성', '여성'))
        bmr_age = st.number_input("나이를 입력하세요.", min_value=12, max_value=120, value=30)
        bmr_height = st.number_input("키(cm)를 입력하세요.", value=170)
        bmr_weight = st.number_input("몸무게(kg)를 입력하세요.", value=70)
        activity = st.selectbox("활동량을 입력하세요.", list(activity_levels.keys()))
        goal = st.selectbox("목표를 선택하세요", ('약간의 다이어트(주 0.25kg감량)', '보통의 다이어트(주 0.5kg감량)', '심한 다이어트(주 1kg감량)', '벌크업', '유지'))

        # 계산하기 버튼
        cal_button = st.button("계산하기")

        if cal_button:
            # Harris-Benedict 공식에 따른 기초 대사량 계산
            if bmr_gender == '남성':
                bmr = 88.362 + (13.397 * bmr_weight) + (4.799 * bmr_height) - (5.677 * bmr_age)
            else:
                bmr = 447.593 + (9.247 * bmr_weight) + (3.098 * bmr_height) - (4.330 * bmr_age)

            # 기초 대사량 출력
            st.write(f"기초 대사량(BMR): {bmr:.2f} kcal/일")

            

            # 활동 대사량 계산 및 출력
            tdee = bmr * activity_levels[activity]
            st.write(f"총 일일 에너지 소모량(TDEE): {tdee:.2f} kcal/일")

            # 목표 칼로리 계산 및 출력
            if goal == '약간의 다이어트(주 0.25kg감량)':
                recommended_calories = tdee * 0.89
            elif goal == '보통의 다이어트(주 0.5kg감량)':
                recommended_calories = tdee * 0.77
            elif goal == '심한 다이어트(주 1kg감량)':
                recommended_calories = tdee * 0.55
            elif goal == '벌크업':
                recommended_calories = tdee * 1.20
            elif goal == '유지':
                return
            st.write(f"목표를 위한 권장 일일 에너지 소모량: {recommended_calories:.2f} kcal/일")

            # 일일 필요 섭취 영양소 계산
            st.write("일일 필요 섭취 영양소")
            carbohydrate = recommended_calories * 0.5
            protein = recommended_calories * 0.3
            fat = recommended_calories * 0.2
            st.write(f"탄수화물 :{int(carbohydrate):d} kcal / {carbohydrate/4:.2f}g")
            st.write(f"단백질 :{int(protein):d} kcal / {protein/4:.2f}g")
            st.write(f"지방 :{int(fat):d} kcal / {fat/9:.2f}g")


## 데이터 불러오기
try:
    data_path_1 = 'openpowerliftingathletedata.csv'
    data_1 = pd.read_csv(data_path_1)
except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")

## 대시보드 제목 설정
st.title('파워리프팅 선수 성적 대시보드 및 개인 기록 향상을 위한 애플리케이션')

## 성별에 따른 선수들의 분포
st.subheader('성별 분포')
# 데이터 셋에서의 속성값 추출
gender_count = data_1['Sex'].value_counts()
# 그래프 출력
fig, ax = plt.subplots()
ax.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

## 체급별 최고 성적
st.subheader('체급별 최고 성적')
# 데이터셋의 체급 값을 문자열로 변환
origin_weight_class = data_1['WeightClassKg'].astype(str)
origin_weight_class_numeric = origin_weight_class[~origin_weight_class.str.contains("\+") & origin_weight_class.str.isnumeric()]
# 오름차순으로 정렬
origin_weight_class_numeric = sorted(origin_weight_class_numeric.unique(), key=lambda x: float(x))
# 선택박스
weight_class = st.selectbox('체급을 선택하세요.', options=origin_weight_class_numeric)
selected_weight_class_data = data_1[data_1['WeightClassKg'] == weight_class]
# 선수 최고기록 추출
best_squat = selected_weight_class_data['BestSquatKg'].max()
best_bench = selected_weight_class_data['BestBenchKg'].max()
best_deadlift = selected_weight_class_data['BestDeadliftKg'].max()
# 평균 추출
average_lifts_by_weight = calculate_averages(selected_weight_class_data, ['BestSquatKg', 'BestBenchKg', 'BestDeadliftKg'])
# 그래프 추출 및 설정
fig, ax = plt.subplots()
ax.bar(['Squat Avg', 'Bench Avg', 'Deadlift Avg'], average_lifts_by_weight, color='orange', label='Average Lifts')
ax.set_ylabel('Weight (kg)')
ax.set_title(f'{weight_class}kg 체급에서의 평균 3대 중량 분포')
ax.legend()
# 그래프 출력 및 텍스트 출력
st.pyplot(fig)
st.write(f"선택된 체급 ({weight_class}kg):")
st.write(f"{weight_class}Kg 최고기록 = 스쿼트: {best_squat}kg, 벤치프레스: {best_bench}kg, 데드리프트: {best_deadlift}kg")

## 연령대별 성적 분포
st.subheader('연령대별 성적 분포')
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
data_1['AgeGroup'] = pd.cut(data_1['Age'], bins=age_bins, labels=age_labels)
# 오름차순으로 정렬
age_groups = data_1['AgeGroup'].dropna().sort_values().unique()
age_group_selected = st.selectbox('연령대를 선택하세요.', options=age_groups)
selected_age_group_data = data_1[data_1['AgeGroup'] == age_group_selected]
# 각 연령대별 벤치프레스, 스쿼트, 데드리프트의 평균을 구하기.
average_lifts_by_age = calculate_averages(selected_age_group_data, ['BestBenchKg', 'BestSquatKg', 'BestDeadliftKg'])
# 그래프 출력
fig, ax = plt.subplots()
ax.bar(['Bench Press', 'Squat', 'Deadlift'], average_lifts_by_age, color=['blue', 'red', 'green'])
ax.set_ylabel('Average Weight (kg)')
ax.set_title('Average Lifts by Age Group')
st.pyplot(fig)


## 장비별 성적 분석
st.subheader('장비별 성적 분석')
equipment_options = data_1['Equipment'].unique()
# 선택박스
equipment = st.selectbox('장비를 선택하세요.', options=equipment_options)
selected_equipment_data = data_1[data_1['Equipment'] == equipment]
# 데이터 셋에서의 속성값 추출
equipment_means = calculate_averages(selected_equipment_data, ['BestSquatKg', 'BestBenchKg', 'BestDeadliftKg'])
# 그래프 출력
fig, ax = plt.subplots()
equipment_means.plot(kind='bar', ax=ax)
ax.set_title('장비별 평균 성적')
ax.set_ylabel('무게(kg)')
st.pyplot(fig)

## 성별 및 체급별 Wilks 점수 평균 분포
st.subheader('성별 및 체급별 Wilks 점수 평균 분포')
# 체급별 Wilks 점수 평균 계산 및 정렬
gender_weight_class_group = data_1.groupby(['Sex', 'WeightClassKg'])['Wilks'].mean().reset_index()
# '+' 포함된 체급 제외
gender_weight_class_group = gender_weight_class_group[~gender_weight_class_group['WeightClassKg'].str.contains("\+", na=False)]
# 체급별로 정렬하는 함수
def sort_weight_classes(weight_class):
    try:
        return float(weight_class)  # 숫자로 변환 가능한 경우만 정렬
    except ValueError:
        return float('inf')  # 숫자로 변환 불가능한 경우 제외
gender_weight_class_group['WeightClassKg'] = gender_weight_class_group['WeightClassKg'].astype(str)  # 체급을 문자열로 변환
gender_weight_class_group.sort_values(by='WeightClassKg', key=lambda x: x.map(sort_weight_classes), inplace=True)
# 성별 선택
gender_choice = st.selectbox('성별을 선택하세요.', options=['M', 'F'], format_func=lambda x: '남성' if x == 'M' else '여성', key='gender_select')
# 선택된 성별에 따른 데이터 필터링
selected_gender_data = gender_weight_class_group[gender_weight_class_group['Sex'] == gender_choice]
# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='WeightClassKg', y='Wilks', hue='Sex', data=selected_gender_data, ax=ax)
ax.set_title('성별 및 체급별 Wilks 점수 평균')
ax.set_xlabel('체급(Kg)')
ax.set_ylabel('Wilks 점수 평균')
plt.xticks(rotation=45)
st.pyplot(fig)


## Wilks 점수에 따른 성능 비교
st.subheader('Wilks 점수에 따른 성능 비교')
# 성별 선택
user_gender = st.selectbox('성별을 선택하세요.', options=['M', 'F'], format_func=lambda x: '남성' if x == 'M' else '여성', key='gender_wilks_select')
# 사용자가 입력한 Wilks 점수
user_wilks = st.number_input('Wilks 점수를 입력하세요.', value=0)
# 성별에 따라 데이터 필터링
filtered_data_wilks = data_1[data_1['Sex'] == user_gender]
# Wilks 점수 차이의 절대값을 계산하여 새 열에 저장
filtered_data_wilks['WilksDifference'] = abs(filtered_data_wilks['Wilks'] - user_wilks)
# Wilks 점수 차이가 가장 작은 상위 10개의 데이터를 선택
closest_wilks = filtered_data_wilks.nsmallest(10, 'WilksDifference')
# 결과 표시
st.write(closest_wilks[['Name', 'Sex', 'BodyweightKg', 'TotalKg', 'Wilks']])
st.write('Wilks 점수란? 체중 대비 삼대 운동 중량으로 계산된 점수로, 포인트가 높을수록 체중 대비 높은 중량으로 운동한다는 뜻입니다.')


## 개인 성적 분석 및 조언 기능
st.subheader('개인 성적 분석 및 조언')

## 사용자 체급 입력 받기를 위한 데이터 전처리
access_user_weight = data_1['WeightClassKg'].astype(str)
access_user_weight_numeric = access_user_weight[~access_user_weight.str.contains("\+") & access_user_weight.str.isnumeric()]
access_user_weight_sorted = sorted(access_user_weight_numeric.unique(), key=lambda x: float(x))

## 사용자 입력 받기
user_sex = st.selectbox('성별을 선택하세요.', options=['M', 'F'], format_func=lambda x: '남성' if x == 'M' else '여성', key = 'user_input_select')
user_age = st.number_input('나이를 입력하세요.', min_value=0, value=30, step=1)
user_weight_class = st.selectbox('체급을 선택하세요.', options=access_user_weight_sorted, key='user_weight_class')
user_best_squat = st.number_input('최고 스쿼트 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
user_best_bench = st.number_input('최고 벤치프레스 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
user_best_deadlift = st.number_input('최고 데드리프트 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
focus_lift = st.selectbox('중점적으로 발전시키고 싶은 운동을 선택하세요.', options=['스쿼트', '벤치프레스', '데드리프트'])

## 장비 추천 및 체급 목표 설정
if st.button('분석 및 조언 받기'):
    # 데이터 필터링
    filtered_data = data_1[(data_1['Sex'] == user_sex) & (data_1['WeightClassKg'] == user_weight_class)]
    # 필터링된 데이터 평균 게산
    average_lifts_by_comparison = calculate_averages(filtered_data, ['BestSquatKg', 'BestBenchKg', 'BestDeadliftKg'])
    # 중점 운동에 따라 장비 추천
    recommended_equipment = 'Raw' if focus_lift == 'Bench' else 'Wraps' if focus_lift == 'Squat' else 'Single-ply'
    
   # 평균 성적 정보 출력
    st.write(f'체급 {user_weight_class}kg에서의 평균 스쿼트: {average_lifts_by_comparison["BestSquatKg"]:.1f}kg')
    st.write(f'체급 {user_weight_class}kg에서의 평균 벤치프레스: {average_lifts_by_comparison["BestBenchKg"]:.1f}kg')
    st.write(f'체급 {user_weight_class}kg에서의 평균 데드리프트: {average_lifts_by_comparison["BestDeadliftKg"]:.1f}kg')
    
    # 개인 기록과 비교
    comparison = {
        'Squat': user_best_squat - average_lifts_by_comparison['BestSquatKg'],
        'Bench': user_best_bench - average_lifts_by_comparison['BestBenchKg'],
        'Deadlift': user_best_deadlift - average_lifts_by_comparison['BestDeadliftKg']
    }
    
    # 결과 출력하기
    st.write(f"장비 추천: {recommended_equipment}")
    st.write(f"체급 내에서 당신의 스쿼트는 평균보다 {comparison['Squat']:.1f}kg 높습니다." if comparison['Squat'] > 0 else f"당신의 스쿼트는 평균보다 {-comparison['Squat']:.1f}kg 낮습니다.")
    st.write(f"체급 내에서 당신의 벤치프레스는 평균보다 {comparison['Bench']:.1f}kg 높습니다." if comparison['Bench'] > 0 else f"당신의 벤치프레스는 평균보다 {-comparison['Bench']:.1f}kg 낮습니다.")
    st.write(f"체급 내에서 당신의 데드리프트는 평균보다 {comparison['Deadlift']:.1f}kg 높습니다." if comparison['Deadlift'] > 0 else f"당신의 데드리프트는 평균보다 {-comparison['Deadlift']:.1f}kg 낮습니다.")
    
    # 추가적인 조언 제공
    if user_age < 24:
        st.write("연령대가 24세 미만이므로, 경험이 쌓이면서 성적이 더욱 향상될 수 있는 잠재력이 있습니다.")
    if user_best_squat + user_best_bench + user_best_deadlift < average_lifts_by_comparison.sum():
        st.write("전체적인 성적 향상을 위해 균형잡힌 훈련 프로그램을 고려해보세요.")
    else:
        st.write("탁월한 성적을 유지하기 위해서는 현재 훈련 방식을 계속 유지하면서, 부상 예방에 주의하세요.")

try:
    data_path_2 = 'openpowerliftingordinarydata.csv'
    data_2 = pd.read_csv(data_path_2)
except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")

## 사용자 데이터 제공 동의 및 데이터 입력 섹션
st.subheader('개인 데이터 제공 동의')
st.write('데이터 채집을 동의하시면 목표 체급까지의 기초대사량 정보를 제공받을 수 있습니다.')
st.write('다른 사용자들에게 더 큰 도움을 주기 위해서 데이터 채집을 동의해주세요.')
st.write('채집된 데이터는 차후에 사용자 데이터을 통한 분석에 반영될 예정입니다.')

if "calculator_kick_start" not in st.session_state:
    st.session_state["calculator_kick_start"] = False

with st.expander("개인 정보 수집 동의"):
    with st.form("my_form"):
        st.subheader('성적 데이터 입력')
        # 사용자 데이터 입력 받기
        agree_name = st.text_input('이름', '')
        agree_sex = st.selectbox('성별', options=['M', 'F'], format_func=lambda x: '남성' if x == 'M' else '여성', key='user_agree_input_select')
        agree_age = st.number_input('나이', min_value=13, max_value=99, value=30, step=1)
        agree_user_weight_class = st.text_input('체급(kg)', '')
        agree_user_best_squat = st.number_input('최고 스쿼트(kg)', min_value=0.0, value=0.0, step=1.0)
        agree_user_best_bench = st.number_input('최고 벤치프레스(kg)', min_value=0.0, value=0.0, step=1.0)
        agree_user_best_deadlift = st.number_input('최고 데드리프트(kg)', min_value=0.0, value=0.0, step=1.0)
        agree_user_total = agree_user_best_squat + agree_user_best_bench + agree_user_best_deadlift

        # 데이터 제출 버튼
        submit = st.form_submit_button('데이터 제출')

        if submit:
            # 새로운 데이터를 데이터프레임에 추가
            new_data = pd.DataFrame({
                'Name': [agree_name],
                'Sex': [agree_sex],
                'Age': [agree_age],
                'WeightClassKg': [agree_user_weight_class],
                'BestSquatKg': [agree_user_best_squat],
                'BestBenchKg': [agree_user_best_bench],
                'BestDeadliftKg': [agree_user_best_deadlift],
                'TotalKg': [agree_user_total],
            })

            # 데이터 추가
            updated_data = pd.concat([data_2, new_data], ignore_index=True)

            # 데이터를 CSV 파일로 저장
            updated_data.to_csv(data_path_2, index=False)
            
            st.session_state["calculator_kick_start"] = True

            st.success('데이터가 성공적으로 추가되었습니다!')



## 사용자가 데이터를 제출했다면 BMR 계산기 출력
if st.session_state["calculator_kick_start"]:
    bmr_calculator()


# 기능 추가(식단 기능)
# README 파일 작성