import time
import random
import streamlit as st

# 페이지 설정 (와이드 모드)
st.set_page_config(
    page_title="🔥 슈의 미친 라면가게: 리부트 🔥",
    page_icon="🍜",
    layout="centered"
)

# 커스텀 CSS (레트로 아케이드 & 매운맛 감성 폭발)
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: 'Malgun Gothic', sans-serif;
    }
    .big-title {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        color: #ff4757;
        text-shadow: 2px 2px #ffa502;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #7bed9f;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .pot-box {
        background: #2f3542;
        border: 4px dashed #ff4757;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0px;
    }
    .burned-pot {
        background: #000000;
        border: 4px solid #2f3542;
        animation: shake 0.5s infinite;
    }
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        20% { transform: translate(-3px, 0px) rotate(-1deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        60% { transform: translate(-1px, 2px) rotate(0deg); }
        80% { transform: translate(-3px, 1px) rotate(-1deg); }
        100% { transform: translate(1px, -2px) rotate(1deg); }
    }
    .shoo-dialog {
        background-color: #ff6b81;
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "START" # START, COOKING, GAMEOVER, SUCCESS
if "score" not in st.session_state:
    st.session_state.score = 0
if "water_level" not in st.session_state:
    st.session_state.water_level = 0
if "fire_power" not in st.session_state:
    st.session_state.fire_power = 50
if "is_burned" not in st.session_state:
    st.session_state.is_burned = False
if "shoo_msg" not in st.session_state:
    st.session_state.shoo_msg = "어서 빨리 라면 끓여라오! 배고프다오! 😡"

# 타이틀
st.markdown('<p class="big-title">🍜 슈의 미친 라면가게 2026</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">슬라이더? 그런 밍밍한 건 없다. 연타와 광클의 타임어택 지옥!</p>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. 시작 화면
# -------------------------------------------------------------
if st.session_state.game_state == "START":
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 📜 [알바생 준수사항]
        1. **물 폭탄 조심**: 물 버튼을 너무 연타하면 넘쳐서 한강 된다!
        2. **냄비 방화 금지**: 불이 너무 세면 냄비가 새까맣게 타버림 (슈 극대노 주의)
        3. **타임어택**: 꾸물거리면 손님이 테이블엎고 도망감!
        """)
        if st.button("🔥 아르바이트 시작하기 (지옥행)", use_container_width=True, type="primary"):
            st.session_state.game_state = "COOKING"
            st.session_state.score = 0
            st.session_state.water_level = 0
            st.session_state.fire_power = 30
            st.session_state.is_burned = False
            st.session_state.shoo_msg = "알바생! 물부터 빨리 부어라오!"
            st.rerun()

# -------------------------------------------------------------
# 2. 게임 플레이 화면 (조리 중)
# -------------------------------------------------------------
elif st.session_state.game_state == "COOKING":
    
    # 상단 상태바
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 현재 매출 (점수)", f"{st.session_state.score} 원")
    c2.metric("🔥 화력 상태", f"{st.session_state.fire_power}%")
    c3.metric("💦 냄비 물 채우기", f"{st.session_state.water_level}% (목표: 80~90%)")

    # 슈의 실시간 잔소리 박스
    st.markdown(f'<div class="shoo-dialog">👧 슈: "{st.session_state.shoo_msg}"</div>', unsafe_allow_html=True)
    st.write("")

    # 냄비 그래픽 시각화 영역 (물 높이와 불타는 상태 표현)
    pot_class = "burned-pot" if st.session_state.is_burned else "pot-box"
    
    # 물 게이지 바 렌더링
    water_bar = "💧" * int(st.session_state.water_level // 10) + "🈳" * (10 - int(st.session_state.water_level // 10))
    fire_bar = "🔥" * int(st.session_state.fire_power // 15)
    
    st.markdown(f"""
    <div class="{pot_class}">
        <h2>🍲 냄비 현황판</h2>
        <p style="font-size: 1.5rem; letter-spacing: 2px;">{water_bar}</p>
        <p style="font-size: 1.2rem; color: #ff4757;">화력: {fire_bar}</p>
        <p><b>상태:</b> {'🚨 새까맣게 타버림!! (망함)' if st.session_state.is_burned else '보글보글 끓는 중...'}</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ 액션 버튼 영역 (광클 및 타이밍 요소) ------------------
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("💧 물 조절 (광클 필수!)")
        if st.button("🚰 쫄쫄쫄 물 붓기 (+15%)", use_container_width=True):
            if not st.session_state.is_burned:
                st.session_state.water_level += 15
                if st.session_state.water_level > 100:
                    st.session_state.is_burned = True
                    st.session_state.shoo_msg = "아니 물바다잖아!! 멍청아!!"
                else:
                    st.session_state.shoo_msg = "조금 더 부어라오!"
                st.rerun()

    with col_b:
        st.subheader("🔥 불 조절 (방심 금지!)")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔥 화력 UP (+20%)", use_container_width=True):
                st.session_state.fire_power += 20
                if st.session_state.fire_power >= 100:
                    st.session_state.is_burned = True
                    st.session_state.shoo_msg = "악! 다 태워먹었어! 내 라면 내놔!!"
                st.rerun()
        with b2:
            if st.button("❄️ 불 줄이기 (-20%)", use_container_width=True):
                st.session_state.fire_power = max(0, st.session_state.fire_power - 20)
                st.rerun()

    st.markdown("---")

    # 완성 제출 버튼
    if st.button("🍜 라면 완성! (슈에게 배달)", use_container_width=True, type="primary"):
        if st.session_state.is_burned:
            st.session_state.game_state = "GAMEOVER"
        elif 75 <= st.session_state.water_level <= 95 and 40 <= st.session_state.fire_power <= 80:
            st.session_state.score += 1000
            st.session_state.game_state = "SUCCESS"
        else:
            st.session_state.game_state = "GAMEOVER"
        st.rerun()

    # 타아메어택 시뮬레이션용 자동 화력 증가 (시간 지날수록 불타오름)
    if not st.session_state.is_burned:
        st.session_state.fire_power += 2
        if st.session_state.fire_power >= 100:
            st.session_state.is_burned = True
            st.session_state.shoo_msg = "방치해서 냄비에 구멍 뚫렸다 이 자식아!!"
            time.sleep(0.5)
            st.rerun()

# -------------------------------------------------------------
# 3. 결과 화면 (성공 or 게임오버)
# -------------------------------------------------------------
elif st.session_state.game_state in ["SUCCESS", "GAMEOVER"]:
    st.markdown("---")
    if st.session_state.game_state == "SUCCESS":
        st.markdown('<h1 style="text-align: center; color: #2ed573;">🎉 완벽한 라면 배달 성공! 🎉</h1>', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>획득 매출: {st.session_state.score}원</h3>", unsafe_allow_html=True)
        st.markdown('<div class="shoo-dialog">👧 슈: "음~ 면발 꼬들함이 예술이네! 합격이다오! 👍"</div>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 style="text-align: center; color: #ff4757;">💥 알바 해고 / 냄비 폭발 💥</h1>', unsafe_allow_html=True)
        st.markdown('<div class="shoo-dialog">👧 슈: "당장 내 가게에서 나가라오!!!!!!!! 👊💢"</div>', unsafe_allow_html=True)

    st.write("")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🔄 다시 알바 뛰기", use_container_width=True, type="primary"):
            st.session_state.game_state = "START"
            st.rerun()
    with col_r2:
        if st.button("🚪 도망치기 (게임 종료)", use_container_width=True):
            st.session_state.game_state = "START"
            st.rerun()
