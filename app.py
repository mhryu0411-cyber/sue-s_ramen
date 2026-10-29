import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 알록달록 무지개 파스타 가게",
    page_icon="🍝",
    layout="centered"
)

# 스트림릿 메인 UI 및 완벽한 슈 게임 감성 웹앱 삽입
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>슈의 파스타 가게</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: #fff0f5;
            font-family: 'Jua', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .game-container {
            width: 650px;
            background: #fffaed;
            border: 5px solid #ffb6c1;
            border-radius: 25px;
            box-shadow: 0 10px 25px rgba(255, 182, 193, 0.4);
            padding: 20px;
            text-align: center;
            position: relative;
        }
        .header-board {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            color: #555;
            background: #fff;
            padding: 10px 20px;
            border-radius: 15px;
            border: 2px solid #ffc0cb;
            margin-bottom: 15px;
        }
        .order-box {
            background: #ffe4e1;
            border: 2px dashed #ff69b4;
            border-radius: 15px;
            padding: 12px;
            margin-bottom: 15px;
        }
        .order-title {
            font-size: 20px;
            color: #d2143a;
            margin-bottom: 5px;
        }
        .order-recipe {
            font-size: 15px;
            color: #666;
        }
        .pot-section {
            background: #e0ffff;
            border: 4px solid #20b2aa;
            border-radius: 20px;
            padding: 15px;
            margin-bottom: 15px;
            min-height: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .pot-title {
            font-size: 16px;
            color: #008b8b;
            margin-bottom: 5px;
        }
        .pot-items {
            font-size: 18px;
            color: #333;
            min-height: 25px;
        }
        .ingredients-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }
        .ingredient-btn {
            background: #fff;
            border: 3px solid #ff69b4;
            border-radius: 15px;
            padding: 12px;
            font-family: 'Jua', sans-serif;
            font-size: 16px;
            cursor: pointer;
            transition: 0.1s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .ingredient-btn:hover {
            background: #fff0f5;
            transform: translateY(-3px);
        }
        .ingredient-btn:active {
            transform: translateY(1px);
        }
        .action-row {
            display: flex;
            gap: 10px;
        }
        .btn-serve {
            flex: 2;
            background: #ff1493;
            color: white;
            border: none;
            border-radius: 15px;
            padding: 12px;
            font-family: 'Jua', sans-serif;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(255,20,147,0.3);
            transition: 0.1s;
        }
        .btn-serve:hover { background: #ff69b4; }
        .btn-reset {
            flex: 1;
            background: #d3d3d3;
            color: #333;
            border: none;
            border-radius: 15px;
            padding: 12px;
            font-family: 'Jua', sans-serif;
            font-size: 16px;
            cursor: pointer;
        }
        .btn-reset:hover { background: #c0c0c0; }
        
        /* 게임 오버 오버레이 */
        .game-over-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            display: none;
        }
        .btn-restart {
            background: #ffeb3b;
            color: #333;
            border: none;
            padding: 12px 30px;
            font-size: 20px;
            font-family: 'Jua', sans-serif;
            border-radius: 30px;
            cursor: pointer;
            margin-top: 15px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <div class="header-board">
        <span id="score-board">점수: 0점</span>
        <span id="time-board">남은 시간: 60초</span>
        <span id="life-board">실패: 0/3</span>
    </div>

    <div class="order-box">
        <div id="order-title" class="order-title">💡 손님의 주문: 로딩중...</div>
        <div id="order-recipe" class="order-recipe">레시피 표시</div>
    </div>

    <div class="pot-section">
        <div class="pot-title">🍲 조리 냄비 (순서대로 투입됩니다)</div>
        <div id="pot-items" class="pot-items">재료를 선택해주세요!</div>
    </div>

    <div class="ingredients-grid">
        <button class="ingredient-btn" style="border-color: #ffd700;" onclick="addIngredient('noodle_yellow', '일반 면')">💛 일반 면</button>
        <button class="ingredient-btn" style="border-color: #8fbc8f;" onclick="addIngredient('noodle_green', '시금치 면')">💚 시금치 면</button>
        <button class="ingredient-btn" style="border-color: #ff4500;" onclick="addIngredient('sauce_tomato', '토마토 소스')">❤️ 토마토 소스</button>
        <button class="ingredient-btn" style="border-color: #dda0dd;" onclick="addIngredient('sauce_cream', '크림 소스')">🤍 크림 소스</button>
        <button class="ingredient-btn" style="border-color: #ffa07a;" onclick="addIngredient('topping_shrimp', '새우')">🦐 새우</button>
        <button class="ingredient-btn" style="border-color: #f0e68c;" onclick="addIngredient('topping_cheese', '치즈')">🧀 치즈</button>
    </div>

    <div class="action-row">
        <button class="btn-serve" onclick="serveDish()">🍽️ 손님에게 서빙하기!</button>
        <button class="btn-reset" onclick="resetPot()">냄비 비우기</button>
    </div>

    <div id="game-over" class="game-over-screen">
        <h2 style="font-size: 36px; color: #ffeb3b; margin-bottom: 10px;">✨ 게임 종료! ✨</h2>
        <p id="final-score" style="font-size: 22px; margin-bottom: 20px;"></p>
        <button class="btn-restart" onclick="startGame()">다시하기 🔄</button>
    </div>
</div>

<script>
let score = 0;
let timeLeft = 60;
let lives = 0;
let isPlaying = false;
let gameTimer = null;
let currentOrder = null;
let userIngredients = [];
let userIngredientNames = [];

const recipes = [
    { name: '새우 토마토 파스타', items: ['noodle_yellow', 'sauce_tomato', 'topping_shrimp'], names: ['일반 면', '토마토 소스', '새우'] },
    { name: '치즈 크림 파스타', items: ['noodle_yellow', 'sauce_cream', 'topping_cheese'], names: ['일반 면', '크림 소스', '치즈'] },
    { name: '초록 시금치 로제 파스타', items: ['noodle_green', 'sauce_tomato', 'topping_cheese'], names: ['시금치 면', '토마토 소스', '치즈'] },
    { name: '특제 해물 크림 파스타', items: ['noodle_green', 'sauce_cream', 'topping_shrimp'], names: ['시금치 면', '크림 소스', '새우'] }
];

function startGame() {
    score = 0;
    timeLeft = 60;
    lives = 0;
    isPlaying = true;
    document.getElementById('game-over').style.display = 'none';
    document.getElementById('score-board').innerText = `점수: ${score}점`;
    document.getElementById('life-board').innerText = `실패: ${lives}/3`;
    
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
    userIngredientNames = [];
    
    document.getElementById('order-title').innerText = `💡 손님의 주문: "${currentOrder.name}"`;
    document.getElementById('order-recipe').innerText = `[레시피: ${currentOrder.names.join(' ➔ ')}]`;
    updatePotUI();
}

function addIngredient(id, name) {
    if(!isPlaying) return;
    if(userIngredients.length < 3) {
        userIngredients.push(id);
        userIngredientNames.push(name);
        updatePotUI();
    }
}

function resetPot() {
    if(!isPlaying) return;
    userIngredients = [];
    userIngredientNames = [];
    updatePotUI();
}

function updatePotUI() {
    const potEl = document.getElementById('pot-items');
    if(userIngredientNames.length === 0) {
        potEl.innerText = '재료를 순서대로 골라주세요!';
    } else {
        potEl.innerText = userIngredientNames.join(' ➔ ');
    }
}

function serveDish() {
    if(!isPlaying) return;
    if(userIngredients.length === 0) {
        alert("냄비가 비어있어요! 재료를 넣어주세요.");
        return;
    }

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
        alert("✨ 완벽해요! 손님이 아주 맛있게 먹었습니다!");
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

function endGame() {
    isPlaying = false;
    clearInterval(gameTimer);
    document.getElementById('final-score').innerText = `최종 점수: ${score}점 달성! 🏆`;
    document.getElementById('game-over').style.display = 'flex';
}

// 게임 시작
startGame();
</script>

</body>
</html>
"""

# 뷰어 영역 높이를 넉넉하게 지정하여 잘림 방지
components.html(game_html, height=550, scrolling=False)
