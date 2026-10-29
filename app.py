import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="🍜 슈의 라면가게: 리얼 하드코어 에디션",
    page_icon="🍜",
    layout="wide"
)

# CSS로 레트로 핑크 주방 및 애니메이션 스타일링
st.markdown("""
<style>
    .stApp {
        background-color: #fff0f3;
        font-family: 'Malgun Gothic', sans-serif;
    }
    .header-box {
        background: linear-gradient(90deg, #ff6b81, #ff4757);
        padding: 15px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    .pot-card {
        background-color: #ffffff;
        border: 4px solid #ffb8c6;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .burned-pot {
        background-color: #2f3542;
        border: 4px solid #ff4757;
        color: white;
        animation: shake 0.4s infinite;
    }
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        25% { transform: translate(-2px, 1px) rotate(-1deg); }
        50% { transform: translate(2px, -1px) rect(0,0,0,0) rotate(1deg); }
        75% { transform: translate(-1px, -2px) rotate(0deg); }
        100% { transform: translate(1px, 2px) rotate(-1deg); }
    }
    .shoo-dialog {
        background-color: #ff6b81;
        color: white;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "revenue" not in st.session_state:
    st.session_state.revenue = 0
if "shoo_msg" not in st.session_state:
    st.session_state.shoo_msg = "어서 빨리 맛있는 라면 끓여라오! 배고프다오! 😡"

# 냄비 4개 상태 구조체 (물, 스프, 면, 계란, 파, 불상태, 타임어택)
if "pots" not in st.session_state:
    st.session_state.pots = {
        i: {
            "water": 0,       # 0 ~ 100 (적정선: 70 ~ 90)
            "soup": False,    # 스프 투하 여부
            "noodle": False,  # 면 투하 여부
            "egg": False,     # 계란 여부
            "scallion": False,# 파 여부
            "fire": False,    # 불 켜짐 여부
            "burned": False,  # 타버림 여부
            "status": "비어있음"
        } for i in range(1, 5)
    }

# 타이틀
st.markdown('<div class="header-box">🌸 슈의 라면가게: 리얼 하드코어 리메이크 🌸</div>', unsafe_allow_html=True)

# 게임 시작 전 화면
if not st.session_state.game_started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 📜 [알바생 생존 지침서]
        1. **물 조절**: 주전자로 적정 눈금(70~90%)까지 물을 채우세요. 넘치면 한강!
        2. **재료 투하**: 면과 스프는 필수, 계란과 파는 센스!
        3. **불 조절 및 타임어택**: 불을 켜면 물이 끓지만, 방심하면 **새까맣게 타버립니다!**
        4. **목표**: 제한 시간 동안 최대한 많은 라면을 팔아 매출을 올리세요!
        """)
        if st.button("🔥 알바 지옥 입장하기", use_container_width=True, type="primary"):
            st.session_state.game_started = True
            st.session_state.revenue = 0
            st.rerun()

else:
    # 상단 현황판
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("💰 누적 수입금", f"{st.session_state.revenue:,} 원")
    sc2.metric("👧 알바생 상태", "정신 바짝 차리는 중 👀")
    sc3.metric("🔥 주방 화재 위험", "높음 (광클 필수)")

    # 슈의 대사
    st.markdown(f'<div class="shoo-dialog">👧 슈: "{st.session_state.shoo_msg}"</div>', unsafe_allow_html=True)

    # 4개의 냄비 렌더링 (2x2 그리드)
    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)
    grid_cols = [r1c1, r1c2, r2c1, r2c2]

    for idx, (pot_id, pot) in enumerate(st.session_state.pots.items()):
        with grid_cols[idx]:
            card_class = "burned-pot" if pot["burned"] else "pot-card"
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            
            st.subheader(f"🟡 {pot_id}번 양은 냄비")
            
            if pot["burned"]:
                st.error("🚨 냄비가 새까맣게 타버렸습니다!! (설거지 행)")
                if st.button(f"🧽 냄비 설거지 및 초기화", key=f"reset_{pot_id}"):
                    st.session_state.pots[pot_id] = {"water": 0, "soup": False, "noodle": False, "egg": False, "scallion": False, "fire": False, "burned": False, "status": "비어있음"}
                    st.session_state.shoo_msg = "일 똑바로 해라오! 정신 차려라오!"
                    st.rerun()
            else:
                # 그래픽 물 게이지 바 표현
                w = pot["water"]
                water_bar = "💧" * (w // 20) + "🈳" * (5 - (w // 20))
                st.write(f"**물 높이:** {water_bar} ({w}%)")
                
                # 재료 상태 표시
                ingredients = []
                if pot["noodle"]: ingredients.append("🍜면")
                if pot["soup"]: ingredients.append("🟥스프")
                if pot["egg"]: ingredients.append("🥚계란")
                if pot["scallion"]: ingredients.append("🌿파")
                ing_str = " | ".join(ingredients) if ingredients else "재료 없음"
                st.write(f"**재료:** {ing_str}")
                st.write(f"**불 상태:** {'🔥 펄펄 끓는 중' if pot["fire"] else '❄️ 꺼짐'}")

                # 조작 버튼들
                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("🚰 물붓기", key=f"water_{pot_id}"):
                        pot["water"] += 20
                        if pot["water"] > 100:
                            pot["burned"] = True
                            st.session_state.shoo_msg = "아니 물이 넘쳐서 주방이 한강이다 이 바보야!!"
                        st.rerun()
                with b2:
                    if st.button("🍜 면투하", key=f"noodle_{pot_id}"):
                        pot["noodle"] = True
                        st.rerun()
                with b3:
                    if st.button("🟥 스프", key=f"soup_{pot_id}"):
                        pot["soup"] = True
                        st.rerun()

                b4, b5, b6 = st.columns(3)
                with b4:
                    if st.button("🥚 계란", key=f"egg_{pot_id}"):
                        pot["egg"] = True
                        st.rerun()
                with b5:
                    if st.button("🌿 파", key=f"scallion_{pot_id}"):
                        pot["scallion"] = True
                        st.rerun()
                with b6:
                    if not pot["fire"]:
                        if st.button("🔥 불켜기", key=f"fire_on_{pot_id}"):
                            pot["fire"] = True
                            st.rerun()
                    else:
                        if st.button("❄️ 불끄기", key=f"fire_off_{pot_id}"):
                            pot["fire"] = False
                            st.rerun()

                st.write("")
                # 완성 및 배달 버튼
                if st.button(f"🍜 뚝배기 완성! (슈에게 배달)", key=f"serve_{pot_id}", type="primary", use_container_width=True):
                    # 성공 조건: 물 60~100 사이, 면과 스프 필수
                    if 60 <= pot["water"] <= 100 and pot["noodle"] and pot["soup"]:
                        bonus = 500 if (pot["egg"] and pot["scallion"]) else 0
                        earned = 1000 + bonus
                        st.session_state.revenue += earned
                        st.session_state.shoo_msg = f"오~ 제법인데?! {earned}원 적립이다오! 👍"
                        # 냄비 리셋
                        st.session_state.pots[pot_id] = {"water": 0, "soup": False, "noodle": False, "egg": False, "scallion": False, "fire": False, "burned": False, "status": "비어있음"}
                    else:
                        st.session_state.shoo_msg = "이게 무슨 맛이야!! 면이 안 익었거나 간이 안 맞잖아! 💢"
                        st.session_state.pots[pot_id]["burned"] = True
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # 하단 전체 초기화 버튼
    st.markdown("---")
    if st.button("🚪 알바 때 때치고 도망치기 (처음으로)", use_container_width=True):
        st.session_state.game_started = False
        st.rerun()
