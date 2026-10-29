import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 아슬아슬 팬케이크 챌린지",
    page_icon="🥞",
    layout="centered"
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>슈의 팬케이크 가게</title>
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
            width: 700px;
            background: #fffdfa;
            border: 5px solid #ffb6c1;
            border-radius: 25px;
            box-shadow: 0 10px 25px rgba(255, 182, 193, 0.4);
            padding: 15px;
            text-align: center;
            position: relative;
        }
        .header {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            color: #555;
            background: #fff;
            padding: 10px 20px;
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
        .controls {
            margin-top: 12px;
        }
        .action-btn {
            background: #ff69b4;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 35px;
            font-family: 'Jua', sans-serif;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(255,105,180,0.4);
            transition: 0.1s;
        }
        .action-btn:active {
            transform: scale(0.95);
        }
        .game-over {
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
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <span id="score">점수: 0점</span>
        <span id="combo" style="color: #ff4500;">🔥 콤보: 0</span>
        <span id="timer">남은 시간: 45초</span>
        <span id="lives">실패: 0/3</span>
    </div>

    <canvas id="gameCanvas" width="660" height="380"></canvas>

    <div class="controls">
        <button id="actionBtn" class="action-btn" onclick="handleAction()">🥞 반죽 붓기 / 타이밍 맞추기!</button>
    </div>

    <div id="gameOverScreen" class="game-over">
        <h2 style="font-size: 38px; color: #ffeb3b; margin-bottom: 10px;">✨ 게임 종료! ✨</h2>
        <p id="finalScore" style="font-size: 22px; margin-bottom: 20px;"></p>
        <button class="action-btn" style="background: #ffeb3b; color: #333;" onclick="startGame()">다시하기 🔄</button>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let score = 0;
let combo = 0;
let timeLeft = 45;
let lives = 0;
let isPlaying = false;
let timerInterval = null;

// 게임 단계: 1(반죽 타이밍), 2(뒤집기 타이밍), 3(시럽 뿌리기 타이밍)
let gameStep = 1; 
let gaugeX = 0;
let gaugeDir = 5;
let instructionText = "반죽 게이지가 중앙(초록색)에 왔을 때 버튼을 누르세요!";

const stepsInfo = {
    1: { name: "1단계: 반죽 붓기", targetMin: 260, targetMax: 300, desc: "노란 원 중앙에 맞추세요!" },
    2: { name: "2단계: 뒤집기 타이밍", targetMin: 240, targetMax: 320, desc: "노릇하게 익었을 때 뒤집기!" },
    3: { name: "3단계: 메이플 시럽 뿌리기", targetMin: 270, targetMax: 290, desc: "완벽한 순간에 시럽 투척!" }
};

function startGame() {
    score = 0;
    combo = 0;
    timeLeft = 45;
    lives = 0;
    isPlaying = true;
    gameStep = 1;
    gaugeX = 50;
    
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

    requestAnimationFrame(updateGame);
}

function updateUI() {
    document.getElementById('score').innerText = `점수: ${score}점`;
    document.getElementById('combo').innerText = `🔥 콤보: ${combo}`;
    document.getElementById('timer').innerText = `남은 시간: ${timeLeft}초`;
    document.getElementById('lives').innerText = `실패: ${lives}/3`;
}

function handleAction() {
    if(!isPlaying) return;

    let currentStepInfo = stepsInfo[gameStep];
    let isPerfect = gaugeX >= currentStepInfo.targetMin && gaugeX <= currentStepInfo.targetMax;
    let isGood = gaugeX >= currentStepInfo.targetMin - 40 && gaugeX <= currentStepInfo.targetMax + 40;

    if(isPerfect) {
        score += 150 + (combo * 20);
        combo++;
        showPopup("✨ 퍼펙트! 꿀맛 팬케이크!", "#ff1493");
        nextStep();
    } else if(isGood) {
        score += 80;
        combo = 0;
        showPopup("👍 나쁘지 않아요!", "#20b2aa");
        nextStep();
    } else {
        lives++;
        combo = 0;
        showPopup("💥 타이밍 실패! 태워먹었어요!", "#ff4500");
        if(lives >= 3) {
            endGame();
            return;
        }
        nextStep();
    }
    updateUI();
}

let popupMsg = "";
let popupColor = "#333";
let popupTimer = 0;

function showPopup(msg, color) {
    popupMsg = msg;
    popupColor = color;
    popupTimer = 30; // 30프레임 동안 표시
}

function nextStep() {
    gameStep++;
    if(gameStep > 3) {
        gameStep = 1; // 한 세트 완성! 추가 보너스 점수
        score += 300;
        showPopup("🎉 특대형 무지개 팬케이크 완성! (+300점)", "#9370db");
    }
}

function updateGame() {
    if(!isPlaying) return;

    // 게이지바 왕복 이동 (난이도 조절 가능)
    gaugeX += gaugeDir * (1 + (combo * 0.15)); // 콤보가 쌓일수록 점점 빨라져서 긴장감 극대화!
    if(gaugeX > 580 || gaugeX < 80) {
        gaugeDir *= -1;
    }

    // 렌더링
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 조리대 연출
    ctx.fillStyle = "#fff8dc";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 팬케이크 프라이팬 그림
    ctx.beginPath();
    ctx.arc(canvas.width / 2, 160, 90, 0, Math.PI * 2);
    ctx.fillStyle = "#d3d3d3";
    ctx.fill();
    ctx.lineWidth = 6;
    ctx.strokeStyle = "#a9a9a9";
    ctx.stroke();

    // 팬케이크 단계별 시각 효과
    ctx.beginPath();
    ctx.arc(canvas.width / 2, 160, 65, 0, Math.PI * 2);
    if(gameStep === 1) ctx.fillStyle = "#fffacd"; // 반죽 색
    else if(gameStep === 2) ctx.fillStyle = `#deb887`; // 익어가는 색
    else ctx.fillStyle = "#d2691e"; // 완성 직전 색
    ctx.fill();

    // 현재 단계 안내 텍스트
    ctx.fillStyle = "#333";
    ctx.font = "bold 20px 'Jua', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(stepsInfo[gameStep].name, canvas.width / 2, 45);
    
    ctx.font = "15px 'Jua', sans-serif";
    ctx.fillStyle = "#666";
    ctx.fillText(stepsInfo[gameStep].desc, canvas.width / 2, 70);

    // 타이밍 게이지 바 배경
    ctx.fillStyle = "#ddd";
    ctx.roundRect(80, 290, 500, 25, 12);
    ctx.fill();

    // 퍼펙트 존 (초록색 영역)
    let target = stepsInfo[gameStep];
    ctx.fillStyle = "#98fb98";
    ctx.fillRect(target.targetMin, 290, target.targetMax - target.targetMin, 25);

    // 움직이는 타이밍 바늘
    ctx.beginPath();
    ctx.arc(gaugeX, 302, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff1493";
    ctx.fill();
    ctx.strokeStyle = "white";
    ctx.lineWidth = 3;
    ctx.stroke();

    // 피드백 팝업 텍스트 출력
    if(popupTimer > 0) {
        ctx.fillStyle = popupColor;
        ctx.font = "bold 22px 'Jua', sans-serif";
        ctx.fillText(popupMsg, canvas.width / 2, 115);
        popupTimer--;
    }

    requestAnimationFrame(updateGame);
}

// 최초 시작
startGame();
</script>

</body>
</html>
"""

components.html(game_html, height=540, scrolling=False)
