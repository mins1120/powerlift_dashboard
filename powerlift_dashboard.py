import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
data_path_1 = 'openpowerliftingathletedata.csv'
data_1 = pd.read_csv(data_path_1)

# 대시보드 제목 설정
st.title('파워리프팅 선수 성적 대시보드')

# 성별에 따른 선수들의 분포
st.subheader('성별 분포')
gender_count = data_1['Sex'].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# 체급별 최고 성적
st.subheader('체급별 최고 성적')
weight_class = st.selectbox('체급을 선택하세요.', options=data_1['WeightClassKg'].unique())
selected_weight_class_data = data_1[data_1['WeightClassKg'] == weight_class]

best_squat = selected_weight_class_data['BestSquatKg'].max()
best_bench = selected_weight_class_data['BestBenchKg'].max()
best_deadlift = selected_weight_class_data['BestDeadliftKg'].max()

st.write(f"선택된 체급 ({weight_class}kg):")
st.write(f"최고 스쿼트: {best_squat}kg, 최고 벤치프레스: {best_bench}kg, 최고 데드리프트: {best_deadlift}kg")

# 연령대별 성적 분포
st.subheader('연령대별 성적 분포')
age_groups = pd.cut(data_1['Age'], bins=[0, 18, 25, 35, 45, 55, 65, 100], labels=['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
data_1['AgeGroup'] = age_groups
age_group_selected = st.selectbox('연령대를 선택하세요.', options=age_groups.unique())
selected_age_group_data = data_1[data_1['AgeGroup'] == age_group_selected]

fig, ax = plt.subplots()
sns.boxplot(x='AgeGroup', y='TotalKg', data=data_1, ax=ax, order=age_groups.unique())
st.pyplot(fig)

# 장비별 성적 분석
st.subheader('장비별 성적 분석')
equipment_options = data_1['Equipment'].unique()
equipment = st.selectbox('장비를 선택하세요.', options=equipment_options)
selected_equipment_data = data_1[data_1['Equipment'] == equipment]
equipment_means = selected_equipment_data[['BestSquatKg', 'BestBenchKg', 'BestDeadliftKg']].mean()
fig, ax = plt.subplots()
equipment_means.plot(kind='bar', ax=ax)
ax.set_title('장비별 평균 성적')
ax.set_ylabel('무게(kg)')
st.pyplot(fig)

# 성별 및 체급별 Wilks 점수 평균
st.subheader('성별 및 체급별 Wilks 점수 평균')
gender_weight_class_group = data_1.groupby(['Sex', 'WeightClassKg'])['Wilks'].mean().reset_index()
gender_selected = st.selectbox('성별을 선택하세요.', options=gender_weight_class_group['Sex'].unique())
selected_gender_data = gender_weight_class_group[gender_weight_class_group['Sex'] == gender_selected]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='WeightClassKg', y='Wilks', hue='Sex', data=selected_gender_data, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Wilks 점수를 이용한 성능 비교
st.subheader('Wilks 점수에 따른 성능 비교')
top_wilks = data_1.nlargest(10, 'Wilks')
st.write(top_wilks[['Name', 'Sex', 'BodyweightKg', 'TotalKg', 'Wilks']])

# 개인 성적 분석 및 조언 기능
st.subheader('개인 성적 분석 및 조언')

# 사용자 입력 받기를 위한 데이터 전처리
weight_classes = data_1['WeightClassKg'].astype(str)
weight_classes_numeric = weight_classes[~weight_classes.str.contains("\+") & weight_classes.str.isnumeric()]
weight_classes_sorted = sorted(weight_classes_numeric.unique(), key=lambda x: float(x))

# 사용자 입력 받기
user_sex = st.selectbox('성별을 선택하세요.', options=['M', 'F'], format_func=lambda x: '남성' if x == 'M' else '여성')
user_age = st.number_input('나이를 입력하세요.', min_value=0, value=30, step=1)
user_weight_class = st.selectbox('체급을 선택하세요.', options=weight_classes_sorted)
user_best_squat = st.number_input('최고 스쿼트 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
user_best_bench = st.number_input('최고 벤치프레스 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
user_best_deadlift = st.number_input('최고 데드리프트 기록(kg)을 입력하세요.', min_value=0.0, value=100.0, step=0.1)
focus_lift = st.selectbox('중점적으로 발전시키고 싶은 운동을 선택하세요.', options=['스쿼트', '벤치프레스', '데드리프트'])

# 장비 추천 및 체급 목표 설정
if st.button('분석 및 조언 받기'):
    # 성별과 체급에 따른 평균 기록을 계산
    average_lifts = data[(data['Sex'] == user_sex) & (data['WeightClassKg'] == user_weight_class)][['BestSquatKg', 'BestBenchKg', 'BestDeadliftKg']].mean()
    
    # 중점 운동에 따라 장비 추천
    recommended_equipment = 'Raw' if focus_lift == 'Bench' else 'Wraps' if focus_lift == 'Squat' else 'Single-ply'
    
    # 체급에서의 성적 비교
    st.write(f'체급 {user_weight_class}kg에서의 평균 스쿼트: {average_lifts["BestSquatKg"]:.1f}kg')
    st.write(f'체급 {user_weight_class}kg에서의 평균 벤치프레스: {average_lifts["BestBenchKg"]:.1f}kg')
    st.write(f'체급 {user_weight_class}kg에서의 평균 데드리프트: {average_lifts["BestDeadliftKg"]:.1f}kg')
    
    # 개인 기록과 비교
    comparison = {
        'Squat': user_best_squat - average_lifts['BestSquatKg'],
        'Bench': user_best_bench - average_lifts['BestBenchKg'],
        'Deadlift': user_best_deadlift - average_lifts['BestDeadliftKg']
    }
    
    st.write(f"장비 추천: {recommended_equipment}")
    st.write(f"체급 내에서 당신의 스쿼트는 평균보다 {comparison['Squat']:.1f}kg 높습니다." if comparison['Squat'] > 0 else f"당신의 스쿼트는 평균보다 {-comparison['Squat']:.1f}kg 낮습니다.")
    st.write(f"체급 내에서 당신의 벤치프레스는 평균보다 {comparison['Bench']:.1f}kg 높습니다." if comparison['Bench'] > 0 else f"당신의 벤치프레스는 평균보다 {-comparison['Bench']:.1f}kg 낮습니다.")
    st.write(f"체급 내에서 당신의 데드리프트는 평균보다 {comparison['Deadlift']:.1f}kg 높습니다." if comparison['Deadlift'] > 0 else f"당신의 데드리프트는 평균보다 {-comparison['Deadlift']:.1f}kg 낮습니다.")
    
    # 추가적인 조언 제공
    if user_age < 24:
        st.write("연령대가 24세 미만이므로, 경험이 쌓이면서 성적이 더욱 향상될 수 있는 잠재력이 있습니다.")
    if user_best_squat + user_best_bench + user_best_deadlift < average_lifts.sum():
        st.write("전체적인 성적 향상을 위해 균형잡힌 훈련 프로그램을 고려해보세요.")
    else:
        st.write("탁월한 성적을 유지하기 위해서는 현재 훈련 방식을 계속 유지하면서, 부상 예방에 주의하세요.")


data_path_2 = 'openpowerliftingordinarydata.csv'
data_2 = pd.read_csv(data_path_2)

# 사용자 데이터 제공 동의 및 데이터 입력 섹션
st.subheader('개인 데이터 제공 동의')
st.write('데이터 채집을 동의하시면 목표 체급까지의 식단 정보를 제공받을 수 있습니다.')

# '본인의 데이터 채집 동의하기' 버튼
if st.button('본인의 데이터 채집 동의하기'):
    consent = True
else:
    consent = False

if consent:
    st.subheader('성적 데이터 입력')
    # 사용자 데이터 입력 받기
    name = st.text_input('이름', '')
    sex = st.selectbox('성별', ['M', 'F'])
    age = st.number_input('나이', min_value=13, max_value=99, value=30, step=1)
    weight_class = st.selectbox('체급', sorted(data_2['WeightClassKg'].unique()))
    best_squat = st.number_input('최고 스쿼트(kg)', min_value=0.0, value=0.0, step=1.0)
    best_bench = st.number_input('최고 벤치프레스(kg)', min_value=0.0, value=0.0, step=1.0)
    best_deadlift = st.number_input('최고 데드리프트(kg)', min_value=0.0, value=0.0, step=1.0)
    total = best_squat + best_bench + best_deadlift

    submit = st.button('데이터 제출')

    if submit:
        # 새로운 데이터를 데이터프레임에 추가
        new_data = pd.DataFrame({
            'Name': [name],
            'Sex': [sex],
            'Age': [age],
            'WeightClassKg': [weight_class],
            'BestSquatKg': [best_squat],
            'BestBenchKg': [best_bench],
            'BestDeadliftKg': [best_deadlift],
            'TotalKg': [total],
        })

        # 기존 데이터셋에 새 데이터 추가 (실제 데이터 저장 방법은 별도로 구현 필요)
        updated_data = pd.concat([data, new_data], ignore_index=True)
        
        st.success('성적 데이터가 성공적으로 추가되었습니다!')

# 코드 오류 없애기 일반인 데이터셋은 엑셀 파일로 되어 있어 오류, csv로 바꿔줘야함
# 기능 추가
# 대쉬보드 개선
# README 파일 작성