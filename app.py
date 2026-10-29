import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="슈의 라면가게 - Streamlit",
    page_icon="🍜",
    layout="centered"
)

st.title("🍜 슈의 라면가게 (Streamlit 인터랙티브 버전)")
st.markdown("버튼을 눌러 물을 맞추고, 재료를 순서대로 넣어 완벽한 라면을 끓여보세요!")

# 세션 상태 초기화 (게임 진행 상태 유지)
if "step" not in st.session_state:
    st.session_state.step = 0  # 0: 대기, 1: 물 맞추기, 2: 재료 넣기, 3: 결과
    st.session_state.water = 50
    st.session_state.has_noodles = False
    st.session_state.has_soup = False
    st.session_state.has_egg = False
    st.session_state.has_onion = False

# ----------------------------------------------------
# 0단계: 시작 화면
# ----------------------------------------------------
if st.session_state.step == 0:
    st.markdown("### 추억의 라면가게 알바를 시작해볼까요?")
    st.image("https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80", use_column_width=True)
    
    if st.button("🎮 게임 시작하기", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ----------------------------------------------------
# 1단계: 물 양 맞추기
# ----------------------------------------------------
elif st.session_state.step == 1:
    st.subheader("STEP 1. 물 양 맞추기")
    st.write("적정 물 양은 **70 ~ 80%** 입니다. 눈금을 잘 맞춰보세요!")
    
    water_val = st.slider("물 조절 레버", 0, 100, 50)
    
    if st.button("💧 물 붓기 완료!", use_container_width=True):
        st.session_state.water = water_val
        st.session_state.step = 2
        st.rerun()

# ----------------------------------------------------
# 2단계: 재료 투하
# ----------------------------------------------------
elif st.session_state.step == 2:
    st.subheader("STEP 2. 재료 넣기")
    st.write(f"현재 물 양: **{st.session_state.water}%**")
    st.info("면과 스프는 필수이며, 계란과 파를 적절히 넣어주세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍜 면 넣기", use_container_width=True):
            st.session_state.has_noodles = True
        if st.button("🧂 스프 넣기", use_container_width=True):
            st.session_state.has_soup = True
            
    with col2:
        if st.button("🥚 계란 톡!", use_container_width=True):
            st.session_state.has_egg = True
        if st.button("🌿 파 썰어넣기", use_container_width=True):
            st.session_state.has_onion = True

    st.markdown("---")
    st.write("📋 **현재 준비된 재료:**")
    st.write(f"- 면: {'✅ 넣음' if st.session_state.has_noodles else '❌ 안 넣음'}")
    st.write(f"- 스프: {'✅ 넣음' if st.session_state.has_soup else '❌ 안 넣음'}")
    st.write(f"- 계란: {'✅ 넣음' if st.session_state.has_egg else '❌ 안 넣음'}")
    st.write(f"- 파: {'✅ 넣음' if st.session_state.has_onion else '❌ 안 넣음'}")

    if st.button("🔥 라면 끓이기 완료!", type="primary", use_container_width=True):
        st.session_state.step = 3
        st.rerun()

# ----------------------------------------------------
# 3단계: 결과 발표
# ----------------------------------------------------
elif st.session_state.step == 3:
    st.subheader("🎉 라면 완성 결과")
    
    water = st.session_state.water
    score = 100
    feedback = []
    
    # 물 양 채점
    if water < 60:
        feedback.append("⚠️ 물이 너무 적어서 볶음면이 되어버렸습니다! (감점)")
        score -= 40
    elif water > 85:
        feedback.append("🌊 한강 라면이 되어 밍밍합니다! (감점)")
        score -= 40
    else:
        feedback.append("✨ 물 양 조절 완벽 성공!")

    # 재료 채점
    if not st.session_state.has_noodles or not st.session_state.has_soup:
        feedback.append("❌ 가장 중요한 면이나 스프를 빼먹었습니다! 대실패!")
        score -= 50
    else:
        feedback.append("✨ 기본 재료 세팅 완료!")
        
    if st.session_state.has_egg and st.session_state.has_onion:
        feedback.append("🌟 계란과 파까지 완벽하게 들어가 최고의 맛입니다!")
        score += 10
    
    score = max(0, min(100, score))
    
    st.metric("최종 점수", f"{score}점")
    
    for f in feedback:
        st.write(f)
        
    st.markdown("---")
    if st.button("🔄 다시 도전하기", type="primary", use_container_width=True):
        st.session_state.step = 0
        st.session_state.water = 50
        st.session_state.has_noodles = False
        st.session_state.has_soup = False
        st.session_state.has_egg = False
        st.session_state.has_onion = False
        st.rerun()
