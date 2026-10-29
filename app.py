import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 알록달록 무지개 파스타 가게",
    page_icon="🍝",
    layout="centered"
)

st.markdown("""
    <style>
    .title { text-align: center; color: #ff4b4b; font-family: 'Jua', sans-serif; }
    .subtitle { text-align: center; color: #666; font-size: 16px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>🍝 슈의 알록달록 무지개 파스타 가게</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>제한 시간 내에 손님이 원하는 레시피대로 파스타를 완성해서 서빙하세요!</div>", unsafe_allow_html=True)

# HTML5 Canvas 기반의 슈 게임 감성 코어 엔진
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Shoo's Pasta Game</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #fff0f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Maplestory', 'Arial', sans-serif;
            overflow: hidden;
        }
        #game-container {
            width: 700px;
            height: 500px;
            background: #fffaed;
            border: 5px solid #ffb6c1;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(255, 182, 193, 0.5);
            position: relative;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #fff;
            cursor: pointer;
        }
        .ui-layer {
            position: absolute;
            top: 15px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            color: #555;
            pointer-events: none;
        }
        .game-over-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            display: none;
        }
        .btn {
            background: #ff69b4;
            color: white;
            border: none;
            padding: 10px 25px;
            font-size: 20px;
            border-radius: 30px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: 0.2s;
        }
        .btn:hover { background: #ff1493; transform: scale(1.05); }
    </style>
</head>
<body>

<div id="game-container">
    <div class="ui-layer">
        <span id="score-board">점수: 0점</span>
        <span id="time-board">남은 시간: 60초</span>
        <span id="life-board">실패: 0/3</span>
    </div>
    
    <canvas id="canvas" width="700" height="500"></canvas>

    <div id="game-over" class="game-over-screen">
        <h2 id="final-msg" style="font-size: 32px; color: #ffeb3b; margin-bottom: 10px;">게임 종료!</h2>
        <p id="final-score" style="font-size: 20px; margin-bottom: 20px;"></p>
        <button class="btn" onclick="restartGame()">다시 하기 ✨</button>
    </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// 게임 상태 변수
let score = 0;
let timeLeft = 60;
let lives = 0;
let isPlaying = false;
let gameTimer = null;
let currentOrder = null;
let userIngredients = [];

// 레시피 및 재료 정의
const ingredientTypes = [
    { id: 'noodle_yellow', name: '일반 면', color: '#ffd700', x: 80, y: 380, radius: 35 },
    { id: 'noodle_green', name: '시금치 면', color: '#8fbc8f', x: 180, y: 380, radius: 35 },
    { id: 'sauce_tomato', name: '토마토 소스', color: '#ff4500', x: 280, y: 380, radius: 35 },
    { id: 'sauce_cream', name: '크림 소스', color: '#fffff0', x: 380, y: 380, radius: 35 },
    { id: 'topping_shrimp', name: '새우', color: '#ffa07a', x: 480, y: 380, radius: 35 },
    { id: 'topping_cheese', name: '치즈', color: '#ffffe0', x: 580, y: 380, radius: 35 }
];

const recipes = [
    { name: '새우 토마토 파스타', items: ['noodle_yellow', 'sauce_tomato', 'topping_shrimp'] },
    { name: '치즈 크림 파스타', items: ['noodle_yellow', 'sauce_cream', 'topping_cheese'] },
    { name: '초록 시금치 로제 파스타', items: ['noodle_green', 'sauce_tomato', 'topping_cheese'] },
    { name: '특제 해물 크림 파스타', items: ['noodle_green', 'sauce_cream', 'topping_shrimp'] }
];

// 냄비 위치
const pot = { x: 350, y: 220, radius: 75 };
// 완성 접시 버튼 위치
const serveButton = { x: 350, y: 460, width: 140, height: 32 };

function startGame() {
    score = 0;
    timeLeft = 60;
    lives = 0;
    userIngredients = [];
    isPlaying = true;
    document.getElementById('game-over').style.display = 'none';
    generateNewOrder();
    
    if(gameTimer) clearInterval(gameTimer);
    gameTimer = setInterval(() => {
        timeLeft--;
        document.getElementById('time-board').innerText = `남은 시간: ${timeLeft}초`;
        if(timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function generateNewOrder() {
    const randomIndex = Math.floor(Math.random() * recipes.length);
    currentOrder = recipes[randomIndex];
    userIngredients = [];
}

function endGame() {
    isPlaying = false;
    clearInterval(gameTimer);
    document.getElementById('final-score').innerText = `최종 점수: ${score}점 달성!`;
    document.getElementById('game-over').style.display = 'flex';
}

function restartGame() {
    startGame();
}

// 마우스 클릭 이벤트 (재료 투입 및 서빙)
canvas.addEventListener('click', (e) => {
    if(!isPlaying) return;
    
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    // 1. 재료 클릭 확인
    ingredientTypes.forEach(ing => {
        const dist = Math.hypot(mouseX - ing.x, mouseY - ing.y);
        if(dist < ing.radius) {
            if(userIngredients.length < 3) {
                userIngredients.push(ing.id);
            }
        }
    });

    // 2. 완성 서빙 버튼 클릭 확인
    if(mouseX >= serveButton.x - 70 && mouseX <= serveButton.x + 70 &&
       mouseY >= serveButton.y - 16 && mouseY <= serveButton.y + 16) {
        checkRecipe();
    }
});

function checkRecipe() {
    if(userIngredients.length === 0) return;

    let isMatch = true;
    if(userIngredients.length !== currentOrder.items.length) {
        isMatch = false;
    } else {
        for(let i=0; i<userIngredients.length; i++) {
            if(userIngredients[i] !== currentOrder.items[i]) {
                isMatch = false;
                break;
            }
        }
    }

    if(isMatch) {
        score += 100;
        alert("✨ 완벽해요! 손님이 감동했어요!");
    } else {
        lives += 1;
        score = Math.max(0, score - 50);
        alert("💥 주문과 다른 요리예요! 손님이 화를 냅니다!");
        if(lives >= 3) {
            endGame();
            return;
        }
    }
    
    document.getElementById('score-board').innerText = `점수: ${score}점`;
    document.getElementById('life-board').innerText = `실패: ${lives}/3`;
    generateNewOrder();
}

// 렌더링 루프
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 아기자기한 주방 타일 느낌
    ctx.fillStyle = '#fffdfa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 상단 주문서 영역 배경
    ctx.fillStyle = '#fff0f5';
    ctx.fillRect(50, 40, 600, 75);
    ctx.strokeStyle = '#ffb6c1';
    ctx.lineWidth = 2;
    ctx.strokeRect(50, 40, 600, 75);

    // 손님 주문 표시
    if(currentOrder) {
        ctx.fillStyle = '#333';
        ctx.font = 'bold 18px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`💡 손님의 주문: "${currentOrder.name}"`, canvas.width / 2, 70);
        
        ctx.font = '14px sans-serif';
        ctx.fillStyle = '#ff1493';
        let recipeStr = currentOrder.items.map(id => ingredientTypes.find(i => i.id === id).name).join(' ➔ ');
        ctx.fillText(`[레시피: ${recipeStr}]`, canvas.width / 2, 98);
    }

    // 중앙 냄비 그리기
    ctx.beginPath();
    ctx.arc(pot.x, pot.y, pot.radius, 0, Math.PI * 2);
    ctx.fillStyle = '#e0ffff';
    ctx.fill();
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#20b2aa';
    ctx.stroke();

    ctx.fillStyle = '#20b2aa';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('🍲 조리 냄비', pot.x, pot.y - 45);

    // 냄비에 담긴 현재 재료 표시
    ctx.font = '13px sans-serif';
    ctx.fillStyle = '#555';
    let currentStr = userIngredients.length > 0 ? 
        userIngredients.map(id => ingredientTypes.find(i => i.id === id).name).join(', ') : 
        '재료를 아래에서 순서대로 넣으세요!';
    ctx.fillText(currentStr, pot.x, pot.y + 5);

    // 서빙 완료 버튼
    ctx.fillStyle = '#ff69b4';
    ctx.roundRect(serveButton.x - 70, serveButton.y - 18, 140, 36, 18);
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText('🍽️ 서빙하기!', serveButton.x, serveButton.y + 5);

    // 하단 재료 아이콘들 그리기
    ctx.textAlign = 'center';
    ctx.font = '12px sans-serif';
    ingredientTypes.forEach(ing => {
        ctx.beginPath();
        ctx.arc(ing.x, ing.y, ing.radius, 0, Math.PI * 2);
        ctx.fillStyle = ing.color;
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#ff69b4';
        ctx.stroke();

        ctx.fillStyle = '#333';
        ctx.fillText(ing.name, ing.x, ing.y + 48);
    });

    requestAnimationFrame(draw);
}

// 게임 최초 시작
startGame();
draw();
</script>

</body>
</html>
"""

components.html(game_html, height=530, scrolling=False)
