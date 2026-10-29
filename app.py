import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 알록달록 스페셜 팬케이크 팩토리",
    page_icon="🥞",
    layout="centered"
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>슈의 팬케이크 팩토리</title>
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
            overflow: hidden;
        }
        .container {
            width: 740px;
            background: #fffdfa;
            border: 5px solid #ffb6c1;
            border-radius: 25px;
            box-shadow: 0 10px 25px rgba(255, 182, 193, 0.5);
            padding: 15px;
            text-align: center;
            position: relative;
        }
        .header {
            display: flex;
            justify-content: space-between;
            font-size: 17px;
            color: #555;
            background: #fff;
            padding: 10px 15px;
            border-radius: 15px;
            border: 2px solid #ffc0cb;
            margin-bottom: 10px;
        }
        canvas {
            background: #fffacd;
            border: 4px solid #f0e68c;
            border-radius: 15px;
            display: block;
            margin: 0 auto;
            cursor: pointer;
        }
        .action-panel {
            margin-top: 10px;
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .action-btn {
            background: #ff69b4;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 25px;
            font-family: 'Jua', sans-serif;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(255,105,180,0.4);
            transition: 0.1s;
        }
        .action-btn:active { transform: scale(0.95); }
        .action-btn:hover { background: #ff1493; }
        
        .topping-grid {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 8px;
        }
        .top-btn {
            background: #fff;
            border: 3px solid #ffb6c1;
            border-radius: 12px;
            padding: 6px 12px;
            font-family: 'Jua', sans-serif;
            font-size: 14px;
            cursor: pointer;
        }
        .top-btn:hover { background: #ffe4e1; }

        .game-over {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.75);
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            display: none;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <span id="score">점수: 0점</span>
        <span id="combo" style="color: #ff4500;">🔥 콤보: 0</span>
        <span id="timer">남은 시간: 60초</span>
        <span id="lives">실패: 0/3</span>
    </div>

    <canvas id="gameCanvas" width="700" height="360"></canvas>

    <div class="action-panel" id="timingControl">
        <button class="action-btn" onclick="executeTimingAction()">⚡ 타이밍 맞추기! (스페이스바)</button>
    </div>

    <div class="topping-grid" id="toppingControl" style="display:none;">
        <span style="font-size: 16px; align-self: center; color: #d2143a; font-weight: bold;">토핑 선택:</span>
        <button class="top-btn" onclick="selectTopping('딸기')">🍓 딸기</button>
        <button class="top-btn" onclick="selectTopping('바나나')">🍌 바나나</button>
        <button class="top-btn" onclick="selectTopping('블루베리')">🫐 블루베리</button>
        <button class="top-btn" onclick="selectTopping('초코시럽')">🍫 초코시럽</button>
    </div>

    <div id="gameOverScreen" class="game-over">
        <h2 style="font-size: 38px; color: #ffeb3b; margin-bottom: 10px;">🏆 게임 세트 클리어! 🏆</h2>
        <p id="finalScore" style="font-size: 22px; margin-bottom: 20px;"></p>
        <button class="action-btn" style="background: #ffeb3b; color: #333;" onclick="startGame()">다시하기 🔄</button>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let score = 0;
let combo = 0;
let timeLeft = 60;
let lives = 0;
let isPlaying = false;
let timerInterval = null;
let animId = null;

// 게임 단계: 
// 0: 주문 대기 / 시작 준비
// 1: 반죽 짜기 (타이밍)
// 2: 뒤집기 (타이밍)
// 3: 토핑 올리기 (선택)
// 4: 서빙 완료 대기
let gameStage = 1;
let gaugeX = 80;
let gaugeDir = 4;

// 주문 시스템
let currentOrder = null;
let userToppings = [];
const availableToppings = ['딸기', '바나나', '블루베리', '초코시럽'];

const ordersList = [
    { name: "상큼 딸기 팬케이크", req: "딸기" },
    { name: "달콤 바나나 팬케이크", req: "바나나" },
    { name: "건강 블루베리 팬케이크", req: "블루베리" },
    { name: "진한 초코 팬케이크", req: "초코시럽" }
];

function startGame() {
    score = 0;
    combo = 0;
    timeLeft = 60;
    lives = 0;
    isPlaying = true;
    gameStage = 1;
    gaugeX = 80;
    userToppings = [];
    
    generateNewOrder();
    document.getElementById('gameOverScreen').style.display = 'none';
    updateUI();

    if(timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--;
        updateUI();
        if(timeLeft <= 0) {
            endGame();
        }
    }, 1000);

    if(animId) cancelAnimationFrame(animId);
    updateGame();
}

function generateNewOrder() {
    currentOrder = ordersList[Math.floor(Math.random() * ordersList.length)];
    userToppings = [];
}

function updateUI() {
    document.getElementById('score').innerText = `점수: ${score}점`;
    document.getElementById('combo').innerText = `🔥 콤보: ${combo}`;
    document.getElementById('timer').innerText = `남은 시간: ${timeLeft}초`;
    document.getElementById('lives').innerText = `실패: ${lives}/3`;
}

function switchControlPanel(stage) {
    const timingCtrl = document.getElementById('timingControl');
    const toppingCtrl = document.getElementById('toppingControl');
    if(stage === 3) {
        timingCtrl.style.display = 'none';
        toppingCtrl.style.display = 'flex';
    } else {
        timingCtrl.style.display = 'flex';
        toppingCtrl.style.display = 'none';
    }
}

function executeTimingAction() {
    if(!isPlaying) return;

    let targetMin = 280, targetMax = 340;
    let isPerfect = gaugeX >= targetMin && gaugeX <= targetMax;
    let isGood = gaugeX >= targetMin - 50 && gaugeX <= targetMax + 50;

    if(isPerfect) {
        score += 150 + (combo * 25);
        combo++;
        showPopup("✨ 퍼펙트 조리 성공!", "#ff1493");
        progressStage();
    } else if(isGood) {
        score += 70;
        combo = 0;
        showPopup("👍 나쁘지 않아요!", "#20b2aa");
        progressStage();
    } else {
        lives++;
        combo = 0;
        showPopup("💥 태워먹었어요! 실패!", "#ff4500");
        if(lives >= 3) {
            endGame();
            return;
        }
        progressStage();
    }
    updateUI();
}

function progressStage() {
    gameStage++;
    if(gameStage === 3) {
        switchControlPanel(3); // 토핑 패널 오픈
    } else if(gameStage > 4) {
        // 완성 및 서빙 완료!
        score += 200;
        showPopup("🎉 완벽한 서빙 완료! (+200점)", "#9370db");
        gameStage = 1;
        switchControlPanel(1);
        generateNewOrder();
    }
}

function selectTopping(topName) {
    if(!isPlaying || gameStage !== 3) return;
    
    if(topName === currentOrder.req) {
        score += 100;
        showPopup(`✨ 손님이 원한 ${topName} 토핑 얹기 성공!`, "#ff1493");
        gameStage = 4; // 시럽/마무리 단계로
        switchControlPanel(1);
        // 바로 자동 완성 처리 후 다음 주문으로
        setTimeout(() => {
            score += 250;
            showPopup("🍽️ 주문 서빙 대성공!", "#20b2aa");
            gameStage = 1;
            generateNewOrder();
            updateUI();
        }, 800);
    } else {
        lives++;
        showPopup(`❌ 틀린 토핑이에요! (${topName})`, "#ff4500");
        if(lives >= 3) {
            endGame();
        }
    }
    updateUI();
}

window.addEventListener('keydown', (e) => {
    if(e.code === 'Space' && gameStage !== 3) {
        e.preventDefault();
        executeTimingAction();
    }
});

let popupMsg = "";
let popupColor = "#333";
let popupTimer = 0;

function showPopup(msg, color) {
    popupMsg = msg;
    popupColor = color;
    popupTimer = 45; 
}

function updateGame() {
    if(!isPlaying) return;

    if(gameStage === 1 || gameStage === 2 || gameStage === 4) {
        gaugeX += gaugeDir + (combo * 0.2); // 콤보 높을수록 바늘 속도 가속!
        if(gaugeX > 610 || gaugeX < 90) {
            gaugeDir *= -1;
        }
    }

    // 화면 렌더링
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 키친 테이블
    ctx.fillStyle = "#fff8dc";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 손님 주문서 상단 표시
    if(currentOrder) {
        ctx.fillStyle = "#ffe4e1";
        ctx.fillRect(150, 10, 400, 35);
        ctx.strokeStyle = "#ffb6c1";
        ctx.lineWidth = 2;
        ctx.strokeRect(150, 10, 400, 35);

        ctx.fillStyle = "#d2143a";
        ctx.font = "bold 16px 'Jua', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(`💡 손님 주문: [ ${currentOrder.name} ] (요청 토핑: ${currentOrder.req})`, canvas.width / 2, 33);
    }

    // 조리대 프라이팬 및 팬케이크 시각화
    ctx.beginPath();
    ctx.arc(canvas.width / 2, 140, 85, 0, Math.PI * 2);
    ctx.fillStyle = "#d3d3d3";
    ctx.fill();
    ctx.lineWidth = 5;
    ctx.strokeStyle = "#a9a9a9";
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(canvas.width / 2, 140, 60, 0, Math.PI * 2);
    if(gameStage === 1) ctx.fillStyle = "#fffacd"; // 반죽
    else if(gameStage === 2) ctx.fillStyle = "#deb887"; // 익는중
    else if(gameStage === 3) ctx.fillStyle = "#d2691e"; // 토핑 대기
    else ctx.fillStyle = "#8b4513"; // 완성
    ctx.fill();

    // 단계별 가이드 텍스트
    ctx.fillStyle = "#333";
    ctx.font = "bold 18px 'Jua', sans-serif";
    ctx.textAlign = "center";
    let stageDesc = "";
    if(gameStage === 1) stageDesc = "1단계: 반죽을 알맞은 크기로 짜주세요!";
    else if(gameStage === 2) stageDesc = "2단계: 노릇하게 익었을 때 뒤집어주세요!";
    else if(gameStage === 3) stageDesc = "3단계: 손님이 주문한 알맞은 토핑을 선택하세요!";
    else if(gameStage === 4) stageDesc = "4단계: 마지막 시럽 타이밍을 맞추세요!";
    
    ctx.fillText(stageDesc, canvas.width / 2, 235);

    // 타이밍 게이지 바 (토핑 단계 아닐 때만 표시)
    if(gameStage !== 3) {
        ctx.fillStyle = "#ddd";
        ctx.beginPath();
        ctx.roundRect(90, 265, 520, 22, 11);
        ctx.fill();

        // 성공 존
        ctx.fillStyle = "#98fb98";
        ctx.fillRect(280, 265, 60, 22);

        // 바늘
        ctx.beginPath();
        ctx.arc(gaugeX, 276, 12, 0, Math.PI * 2);
        ctx.fillStyle = "#ff1493";
        ctx.fill();
        ctx.strokeStyle = "white";
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // 팝업 메시지 출력
    if(popupTimer > 0) {
        ctx.fillStyle = popupColor;
        ctx.font = "bold 20px 'Jua', sans-serif";
        ctx.fillText(popupMsg, canvas.width / 2, 95);
        popupTimer--;
    }

    animId = requestAnimationFrame(updateGame);
}

function endGame() {
    isPlaying = false;
    if(animId) cancelAnimationFrame(animId);
    clearInterval(timerInterval);
    document.getElementById('finalScore').innerText = `최종 점수: ${score}점 달성! 🏆`;
    document.getElementById('gameOverScreen').style.display = 'flex';
}

// 최초 시작
startGame();
</script>

</body>
</html>
"""

components.html(game_html, height=540, scrolling=False)
