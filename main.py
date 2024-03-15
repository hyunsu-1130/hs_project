import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib import font_manager, rc
import matplotlib.font_manager as fm
from streamlit_option_menu import option_menu

# CSV 파일을 로드하는 함수
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# 실제 한글 폰트 파일의 경로로 변경
font_path = "c:\WINDOWS\Fonts\HANCOM GOTHIC BOLD.TTF"
fontprop = fm.FontProperties(fname=font_path, size=15)


# txt 파일 읽기 함수 - 소비자 물가 지수 추이 설명
def read_price_trend_detail(year, month):
    file_path = f"C:\\workspace\\hs_project\\물가동향\\{year}년 {month}월 소비자 물가 동향.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "해당 시점의 정보를 찾을 수 없습니다."

    

# 메인 함수
def main():
    #st.title('🔍 우리나라 물가 데이터 대시보드')
    st.markdown("""
        <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: black;
            background-color: #F0F8FF;
            padding: 10px;
            border-radius: 20px;
        }
        </style>
        <div class="
        title">🔍 우리나라 물가 데이터 대시보드</div>
    """, unsafe_allow_html=True)


    #st.write("통계청 자료를 기반으로 작성되었습니다.")
    st.markdown("""
          <style>
          .bottomRight {
              position: fixed;
              bottom: 10px;
              right: 10px;
              color: grey;
          }
          </style>
          <div class="bottomRight">통계청 자료를 기반으로 작성되었습니다.</div>
      """, unsafe_allow_html=True)

    with st.sidebar:
      tab = option_menu("Menu", ["주요 소비재 가격 변동", "소비자 물가 지수 추이"],
                          icons=['bi bi-graph-up', 'bi bi-collection'],
                          menu_icon="bi bi-broadcast", default_index=0,
                          styles={
          "container": {"padding": "4!important", "background-color": "#fafafa"},
          "icon": {"color": "black", "font-size": "25px"},
          "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#C6E2FF"},
          "nav-link-selected": {"color" : "black", "background-color": "#F0F8FF"},
      }
      )
    
    # 탭 설정 - 스타일 변동
    # tab = st.sidebar.radio("LIST", ("주요 소비재 가격 변동", "소비자 물가 지수 추이")) # 다른 기능을 추가하려면 여기에 추가
    
    # 주요 소비재 가격 변동 탭 선택 시
    if tab == "주요 소비재 가격 변동":
        # CSV 파일 로드
        file_path = '주요_소비재_가격_변동.csv'
        df = load_data(file_path)
        
        # 주요 소비재 가격 변동 그래프 시각화
        st.markdown('# 💰 주요 소비재 가격 변동')

        # '시도별' 열 삭제
        df.drop(columns=['시도별'], inplace=True)


        # 품목 목록 드롭다운 메뉴
        selected_item = st.selectbox('품목 선택', df['품목별'].unique(),
                                      help='원하시는 소비재를 선택하세요.')

        #format_func=lambda x: f'<span style="color:blue; font-size:20px; background-color: #F0F8FF;">{x}</span>')

        # 선택한 품목에 대한 데이터 추출
        selected_df = df[df['품목별'] == selected_item].drop(columns=['품목별'])

        # 선택한 품목의 물가 지수 그래프 생성
        plt.figure(figsize=(15, 8))
        plt.plot(selected_df.columns, selected_df.values.flatten(), marker='o')
        plt.xlabel('시점',fontproperties=fontprop)
        plt.ylabel('값(%)',fontproperties=fontprop)
        plt.title(f'{selected_item} 가격 변동',fontproperties=fontprop)
        plt.xticks(rotation=45)
        plt.grid(True)

        # Streamlit에 그래프 출력
        st.pyplot()



    # 주요 소비재 가격 변동 탭 선택 시
    if tab == "소비자 물가 지수 추이":
        # CSV 파일 로드
        file_path = '월별_소비자물가_등락률.csv'
        df = load_data(file_path)

        # '시점'을 datetime 객체로 변환하여 정렬합니다. (필요한 경우)
        #df['시점'] = pd.to_datetime(df['시점'], format='%Y.%m')


        st.markdown('''
          <div style="border: 3px solid #318CE7; border-radius: 10px; padding: 10px;">
          <h1 style="font-size: 36px; font-weight: bold; color: black;">💹 소비자 물가 지수 추이</h1>
          <p><span style="font-weight: bold; color: #FF4B4B;">등락률</span> : 기준시점에 대한 비교시점의 증감률, 단위는 퍼센트(%) 📊</p>
          <p><span style="font-weight: bold; color: black;">전월대비</span> : 전월과 비교한 금월의 물가수준 등락률 🔵</p>
          <p><span style="font-weight: bold; color: black;">전년동월대비</span> : 전년도 같은 달과 비교한 금월의 물가수준 등락률 🔴</p>
          </div>
          ''', unsafe_allow_html=True)

        # 데이터 프레임을 변환
        df_transposed = df.transpose()


        # Plotly 그래프 생성
        fig = go.Figure()

        # 각 행에 대한 그래프 추가
        #for column in df_transposed.columns:
            #fig.add_trace(go.Scatter(x=df_transposed.index, y=df_transposed[column], mode='lines+markers', name=column))
        

        # '전월대비', '전년동월대비' 각각에 대한 선 그래프 추가
        for column in df_transposed.columns:
            # 조건을 통해 각 선의 이름과 색상을 설정합니다.
            if column == 0:
                color = "blue"
                legend_name = "전월대비"
            else:
                color = "red"
                legend_name = "전년동월대비"


            fig.add_trace(go.Scatter(
                x=df_transposed.index,  # 날짜를 x축으로 설정
                y=df_transposed[column],  # '전월대비' 혹은 '전년동월대비' 값을 y축으로 설정
                mode='lines+markers',
                name=legend_name,  # 여기에서 범례 이름을 설정합니다.
                line=dict(color=color)
            ))

        # 그래프 설정
        fig.update_layout(
            title='소비자 물가 지수 추이 그래프',
            xaxis_title='시점',
            yaxis_title='값(%)',
            hovermode='x unified'
            )

        # Streamlit에 그래프 출력
        st.plotly_chart(fig, use_container_width=True)


        # 사용자로부터 연도와 월을 선택하게 하는 옵션
        #st.markdown("## 📜 특정 시점의 소비자 물가 지수 Comment")
        st.markdown("""
            <style>
            .sub-title {
                font-size: 30px;
                font-weight: bold;
                color: black;
                background-color: #F0F8FF;
                padding: 10px;
                border-radius: 20px;
            }
            </style>
            <div class="
            sub-title">📜 특정 시점의 소비자 물가 지수 Comment</div>
            """, unsafe_allow_html=True)

        year = st.selectbox("년도를 선택하세요", (2020, 2021, 2022, 2023, 2024))
        month = st.selectbox("월을 선택하세요", range(1, 13))

        # 선택된 시점에 대한 물가 동향 정보 읽어오기
        details = read_price_trend_detail(year, month)
        
        # 정보 출력
        st.text_area("상세 정보", value=details, height=300)


if __name__ == "__main__":
    main()