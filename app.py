import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="슈의 라면가게 - Streamlit",
    page_icon="🍜",
    layout="centered"
)

st.title("🍜 슈의 라면가게 (Streamlit 버전)")
st.markdown("추억의 플래시 게임 '슈의 라면가게'를 웹에서 즐겨보세요! 물 조절과 파, 계란 타이밍이 핵심입니다.")

# 게임 플레이 영역 (HTML5 웹 게임 임베드)
# 웹상에 구현된 오픈소스/공유 웹게임 플레이어 링크를 활용합니다.
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        iframe {
            width: 100%;
            height: 600px;
            border: none;
            max-width: 800px;
        }
    </style>
</head>
<body>
    <!-- 슈의 라면가게 플레이 가능한 오픈 에뮬레이터/임베드 소스 -->
    <iframe src="https://phosphorus.github.io/app.html?id=255755198&turbo=false&full-screen=true" allowfullscreen></iframe>
</body>
</html>
"""

components.html(game_html, height=620)

st.markdown("---")
st.markdown("### 💡 게임 팁")
st.write("- **물의 양:** 한강 라면이 되지 않도록 눈금을 잘 맞추세요!")
st.write("- **면과 스프:** 물이 끓으면 면과 스프를 알맞은 타이밍에 넣어야 합니다.")
st.write("- **계란과 파:** 마지막 완성 직전에 계란과 파를 톡톡!")
