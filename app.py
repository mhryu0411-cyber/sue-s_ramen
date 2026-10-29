import json
import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 (와이드 모드)
st.set_page_config(
    page_title="서울 라면맵 - 참여형 맛집 지도",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS로 깔끔한 UI 다듬기
st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    .stButton>button { width: 100%; border-radius: 6px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #E03E3E; color: white; }
    div.stMetric { background-color: #FFFFFF; padding: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 데이터 파일 경로
DATA_FILE = "seoul_ramen_places.json"

# 초기 데이터 로드 (서울 중심 대표 라면 가게)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        initial_data = [
            {
                "name": "공릉동 멸치국수 본점",
                "address": "서울특별시 노원구 화랑로 415",
                "lat": 37.6251,
                "lon": 127.0728,
                "price": 5000,
                "rating": 4.6,
                "comment": "시원한 멸치 육수가 일품인 가성비 최고 국수/라면집!"
            },
            {
                "name": "틈새라면 명동본점",
                "address": "서울특별시 중구 명동10길 19-3",
                "lat": 37.5610,
                "lon": 126.9850,
                "price": 6000,
                "rating": 4.7,
                "comment": "원조 매운 라면의 성지. 빨계떡 강력 추천합니다."
            },
            {
                "name": "라멘모토 서울역점",
                "address": "서울특별시 중구 세종대로 14",
                "lat": 37.5563,
                "lon": 126.9723,
                "price": 9500,
                "rating": 4.4,
                "comment": "진한 츠케멘과 매운 라멘을 맛볼 수 있는 곳."
            },
            {
                "name": "우정가든 라면",
                "address": "서울특별시 종로구 율곡로 3",
                "lat": 37.5758,
                "lon": 126.9814,
                "price": 4500,
                "rating": 4.2,
                "comment": "경복궁 근처 옛날 감성 분식집 라면."
            }
        ]
        save_data(initial_data)
        return initial_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

places_data = load_data()
df = pd.DataFrame(places_data)

# 3. 상단 헤더 영역
st.title("🍜 서울 라면맵 (Seoul Ramen Map)")
st.markdown("거지맵 스타일의 참여형 서울 라면 맛집 공유 플랫폼입니다. 나만의 숨은 라면 성지를 제보해 주세요!")
st.divider()

# 4. 사이드바 구성 (검색, 필터, 제보)
with st.sidebar:
    st.header("🔍 검색 및 필터")
    search_query = st.text_input("식당 이름 검색", placeholder="예: 틈새라면")
    max_price = st.slider("최대 가격 제한 (원)", min_value=3000, max_value=15000, value=10000, step=500)
    
    st.divider()
    
    st.subheader("➕ 서울 라면집 제보하기")
    with st.add_form := st.form("add_form", clear_on_submit=True):
        new_name = st.text_input("가게 이름")
        new_address = st.text_input("서울 주소 (예: 서울시 중구 ...)")
        
        c1, c2 = st.columns(2)
        with c1:
            new_lat = st.number_input("위도 (Lat)", value=37.5665, format="%.4f")
        with c2:
            new_lon = st.number_input("경도 (Lon)", value=126.9780, format="%.4f")
            
        new_price = st.number_input("대표 메뉴 가격 (원)", min_value=1000, max_value=30000, value=5000, step=500)
        new_rating = st.slider("평점", 1.0, 5.0, 4.5, 0.5)
        new_comment = st.text_area("한 줄 추천 평")
        
        submitted = st.form_submit_button("맛집 등록하기")
        if submitted:
            if new_name and new_address:
                new_entry = {
                    "name": new_name,
                    "address": new_address,
                    "lat": float(new_lat),
                    "lon": float(new_lon),
                    "price": int(new_price),
                    "rating": float(new_rating),
                    "comment": new_comment
                }
                places_data.append(new_entry)
                save_data(places_data)
                st.success("성공적으로 등록되었습니다!")
                st.rerun()
            else:
                st.warning("가게 이름과 주소를 입력해주세요.")

# 데이터 필터링
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, na=False)]
filtered_df = filtered_df[filtered_df['price'] <= max_price]

# 5. 메인 레이아웃: 좌측(지도) / 우측(깔끔한 카드 리스트)
map_col, list_col = st.columns([1.6, 1])

with map_col:
    st.subheader("📍 서울 맛집 지도")
    
    # 서울 중심좌표 고정 또는 필터된 결과의 중심점 활용
    center_lat, center_lon = 37.5665, 126.9780
    if not filtered_df.empty and search_query:
        center_lat = filtered_df['lat'].mean()
        center_lon = filtered_df['lon'].mean()

    # 깔끔한 톤의 Folium 지도 생성 (CartoDB Positron 적용)
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=13, 
        tiles="CartoDB positron"
    )

    # 마커 루프 (거지맵처럼 가격이 보이도록 툴팁 및 팝업 구성)
    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style="font-family:sans-serif; width:180px;">
            <h4 style="margin:0 0 5px 0; color:#333;">{row['name']}</h4>
            <p style="margin:2px 0; font-size:13px;"><b>가격:</b> {row['price']:,}원</p>
            <p style="margin:2px 0; font-size:13px;"><b>평점:</b> ⭐ {row['rating']}</p>
            <p style="margin:5px 0 0 0; font-size:11px; color:#666;">{row['comment']}</p>
        </div>
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{row['name']} ({row['price']:,}원)",
            icon=folium.Icon(color="orange", icon="utensils", prefix="fa")
        ).add_to(m)

    st_folium(m, width="100%", height=600)

with list_col:
    st.subheader(f"📋 검색 결과 목록 ({len(filtered_df)}곳)")
    
    with st.container(height=580):
        if filtered_df.empty:
            st.info("조건에 맞는 서울 라면 가게가 없습니다.")
        else:
            for _, row in filtered_df.iterrows():
                with st.container():
                    st.markdown(f"#### **{row['name']}**")
                    st.caption(f"📍 {row['address']}")
                    
                    col_p, col_r = st.columns(2)
                    with col_p:
                        st.markdown(f"💰 **{row['price']:,}원**")
                    with col_r:
                        st.markdown(f"⭐ **{row['rating']} / 5.0**")
                        
                    if row['comment']:
                        st.info(f"💬 {row['comment']}")
                    st.markdown("---")
