import streamlit as st

# Streamlit 페이지 설정
st.set_page_config(
    page_title="고군분투 리메이크 - 30년 차 개발자 에디션",
    page_icon="🐱",
    layout="centered"
)

st.title("🐱 고군분투! (Go Go! Pyun-chan!)")
st.markdown("30년 차 개발자의 손길로 재현한 추억의 플래시 게임입니다. **스페이스바**를 눌러 점프하고, 벽에 부딪힐 때 **스페이스바를 연타**하여 벽에 붙어보세요!")

# HTML5 + Canvas + JS 기반의 고군분투 게임 컴포넌트
game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>고군분투 게임</title>
    <style>
        body {
            margin: 0;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Arial', sans-serif;
        }
        canvas {
            border: 4px solid #fff;
            box-shadow: 0 0 20px rgba(255,255,255,0.3);
            background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="800" height="450"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 게임 상태 변수
let gameState = "START"; // START, PLAYING, GAMEOVER
let score = 0;
let distance = 0;
let coins = 0;

// 플레이어 객체 (고양이 닌자)
let player = {
    x: 100,
    y: 300,
    width: 35,
    height: 45,
    vy: 0,
    speed: 6,
    isJumping: false,
    isWallSliding: false,
    facing: 'right',
    jumpCount: 0
};

// 물리 상수
const gravity = 0.6;
const jumpPower = -11;
const wallSlideGravity = 1.5;

// 월드 오브젝트 (지붕, 벽, 장애물, 코인)
let platforms = [];
let hazards = [];
let items = [];

// 게임 초기화
function initGame() {
    score = 0;
    distance = 0;
    coins = 0;
    player.x = 100;
    player.y = 250;
    player.vy = 0;
    player.isJumping = false;
    player.isWallSliding = false;
    player.jumpCount = 0;
    
    platforms = [
        { x: 0, y: 360, width: 900, height: 90, type: 'roof' }
    ];
    hazards = [];
    items = [];
}

// 맵 제너레이터 (무한 질주 생성)
function generateWorld() {
    let lastPlatform = platforms[platforms.length - 1];
    if (lastPlatform.x + lastPlatform.width < player.x + 900) {
        let pWidth = Math.floor(Math.random() * 250) + 180;
        let pGap = Math.floor(Math.random() * 90) + 50; // 낭떠러지 간격
        let pHeight = Math.floor(Math.random() * 60) + 320;
        
        let newX = lastPlatform.x + lastPlatform.width + pGap;
        platforms.push({ x: newX, y: pHeight, width: pWidth, height: 150, type: 'roof' });

        // 일정 확률로 벽(장애물 건물) 생성
        if (Math.random() > 0.4) {
            hazards.push({
                x: newX + pWidth - 40,
                y: pHeight - 120,
                width: 40,
                height: 120,
                type: 'wall'
            });
        }

        // 코인 생성
        if (Math.random() > 0.3) {
            items.push({
                x: newX + 50,
                y: pHeight - 60,
                radius: 10,
                collected: false
            });
        }
    }

    // 화면 지난 오브젝트 제거
    platforms = platforms.filter(p => p.x + p.width > player.x - 200);
    hazards = hazards.filter(h => h.x + h.width > player.x - 200);
    items = items.filter(i => i.x > player.x - 200);
}

// 키 입력 처리
window.addEventListener("keydown", e => {
    if (e.code === "Space") {
        e.preventDefault(); // 스크롤 방지
        if (gameState === "START" || gameState === "GAMEOVER") {
            initGame();
            gameState = "PLAYING";
            return;
        }
        
        if (gameState === "PLAYING") {
            if (player.isWallSliding) {
                // 벽에서 반대 방향으로 뛰어오르기 (벽킥)
                player.vy = jumpPower * 1.1;
                player.speed += 2; // 가속
                player.isWallSliding = false;
            } else if (!player.isJumping || player.jumpCount < 2) {
                // 2단 점프
                player.vy = jumpPower;
                player.isJumping = true;
                player.jumpCount++;
            }
        }
    }
});

// 메인 게임 루프
function update() {
    if (gameState === "PLAYING") {
        // 자동 질주
        player.x += player.speed;
        distance = Math.floor(player.x / 10);
        score = distance + (coins * 100);

        // 중력 적용
        if (player.isWallSliding) {
            player.vy = wallSlideGravity;
        } else {
            player.vy += gravity;
        }
        player.y += player.vy;

        // 플랫폼(지붕) 충돌 체크
        player.isWallSliding = false;

        for (let p of platforms) {
            if (player.x + player.width > p.x && player.x < p.x + p.width) {
                if (player.y + player.height >= p.y && player.y + player.height - player.vy <= p.y + 10 && player.vy >= 0) {
                    player.y = p.y - player.height;
                    player.vy = 0;
                    player.isJumping = false;
                    player.jumpCount = 0;
                }
            }
        }

        // 벽(장애물 건물 벽면) 충돌 및 벽타기 체크
        for (let h of hazards) {
            if (player.y + player.height > h.y && player.y < h.y + h.height) {
                if (player.x + player.width >= h.x && player.x < h.x + 10 && player.vy > 0) {
                    player.isWallSliding = true;
                    player.x = h.x - player.width;
                }
            }
        }

        // 코인 획득 체크
        for (let item of items) {
            if (!item.collected) {
                let dist = Math.hypot((player.x + player.width/2) - item.x, (player.y + player.height/2) - item.y);
                if (dist < 25) {
                    item.collected = true;
                    coins++;
                }
            }
        }

        // 낙사 체크 (낭떠러지 추락)
        if (player.y > canvas.height + 50) {
            gameState = "GAMEOVER";
        }

        // 월드 확장
        generateWorld();
        
        // 속도 서서히 증가 (난이도 상승)
        if (player.speed < 12) {
            player.speed += 0.001;
        }
    }
}

// 화면 렌더링
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 달
    ctx.fillStyle = "#fff3cd";
    ctx.beginPath();
    ctx.arc(700, 90, 40, 0, Math.PI * 2);
    ctx.fill();

    // 카메라 스크롤 (플레이어 중심 추적)
    ctx.save();
    ctx.translate(-player.x + 200, 0);

    // 플랫폼(지붕) 그리기
    for (let p of platforms) {
        ctx.fillStyle = "#3e2723";
        ctx.fillRect(p.x, p.y, p.width, p.height);
        ctx.strokeStyle = "#5d4037";
        ctx.lineWidth = 4;
        ctx.strokeRect(p.x, p.y, p.width, p.height);
    }

    // 장애물(벽) 그리기
    for (let h of hazards) {
        ctx.fillStyle = "#455a64";
        ctx.fillRect(h.x, h.y, h.width, h.height);
        ctx.strokeStyle = "#263238";
        ctx.strokeRect(h.x, h.y, h.width, h.height);
    }

    // 코인 그리기
    for (let item of items) {
        if (!item.collected) {
            ctx.fillStyle = "#ffeb3b";
            ctx.beginPath();
            ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#fbc02d";
            ctx.lineWidth = 3;
            ctx.stroke();
        }
    }

    // 플레이어 (고양이 닌자) 그리기
    ctx.fillStyle = player.isWallSliding ? "#ff9800" : "#ff5722";
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    // 고양이 귀 표현
    ctx.fillStyle = "#e64a19";
    ctx.beginPath();
    ctx.moveTo(player.x, player.y);
    ctx.lineTo(player.x + 10, player.y - 12);
    ctx.lineTo(player.x + 20, player.y);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(player.x + player.width - 20, player.y);
    ctx.lineTo(player.x + player.width - 10, player.y - 12);
    ctx.lineTo(player.x + player.width, player.y);
    ctx.fill();

    ctx.restore();

    // UI (점수 및 상태 표시 - 화면 고정)
    ctx.fillStyle = "white";
    ctx.font = "bold 20px Arial";
    ctx.fillText("점수: " + score, 30, 40);
    ctx.fillText("금화: 🪙 " + coins, 200, 40);

    if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "white";
        ctx.font = "bold 36px Arial";
        ctx.textAlign = "center";
        ctx.fillText("🐱 고 군 분 투 🐱", canvas.width / 2, canvas.height / 2 - 30);
        ctx.font = "18px Arial";
        ctx.fillText("스페이스바를 눌러서 시작하세요!", canvas.width / 2, canvas.height / 2 + 20);
        ctx.fillText("점프 & 벽에 닿을 때 스페이스바 연타로 벽타기!", canvas.width / 2, canvas.height / 2 + 60);
        ctx.textAlign = "left";
    } else if (gameState === "GAMEOVER") {
        ctx.fillStyle = "rgba(180, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "white";
        ctx.font = "bold 36px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 30);
        ctx.font = "18px Arial";
        ctx.fillText("최종 점수: " + score + "점", canvas.width / 2, canvas.height / 2 + 15);
        ctx.fillText("다시 시작하려면 스페이스바를 누르세요!", canvas.width / 2, canvas.height / 2 + 55);
        ctx.textAlign = "left";
    }
}

// 메인 루프 실행
function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

initGame();
loop();
</script>

</body>
</html>
"""

st.components.v1.html(game_code, height=480, scrolling=False)
