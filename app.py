import streamlit as st

# Streamlit 페이지 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="고군분투 리메이크 - 하이퍼 스피드 에디션",
    page_icon="🐱",
    layout="wide"
)

st.title("🐱 고군분투: 하이퍼 질주! (Go Go! Pyun-chan!)")
st.markdown("⚡ **속도 대폭 상향 & 와이드 뷰 적용!** 스페이스바를 눌러 점프하고, 벽에 부딪힐 때 **연타**하여 벽을 타고 오르세요. 생선(🐟)을 먹으면 **부스터 모드**가 발동됩니다!")

# HTML5 + Canvas + JS 고성능 아케이드 게임 컴포넌트
game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>고군분투 하이퍼</title>
    <style>
        body {
            margin: 0;
            background-color: #0f0f13;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Arial', sans-serif;
        }
        canvas {
            border: 4px solid #ffcc00;
            box-shadow: 0 0 30px rgba(255, 204, 0, 0.4);
            background: linear-gradient(to bottom, #111, #1a2a3a, #2c3e50);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="1000" height="520"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 게임 상태 변수
let gameState = "START"; // START, PLAYING, GAMEOVER
let score = 0;
let distance = 0;
let coins = 0;
let fishCount = 0;
let combo = 0;
let shakeTimer = 0;
let boosterTimer = 0;

// 플레이어 객체 (초고속 닌자 고양이)
let player = {
    x: 150,
    y: 350,
    width: 40,
    height: 50,
    vy: 0,
    baseSpeed: 9,      // 기본 속도 대폭 상향
    speed: 9,
    isJumping: false,
    isWallSliding: false,
    jumpCount: 0,
    rotation: 0
};

// 물리 상수 (하드코어 아케이드 세팅)
const gravity = 0.75;
const jumpPower = -14.5;
const wallSlideGravity = 1.8;

// 월드 오브젝트
let platforms = [];
let hazards = [];
let items = [];
let particles = [];

// 화면 흔들림 효과 트리거
function triggerShake(frames) {
    shakeTimer = frames;
}

// 게임 초기화
function initGame() {
    score = 0;
    distance = 0;
    coins = 0;
    fishCount = 0;
    combo = 0;
    boosterTimer = 0;
    player.x = 150;
    player.y = 300;
    player.vy = 0;
    player.isJumping = false;
    player.isWallSliding = false;
    player.jumpCount = 0;
    player.speed = player.baseSpeed;
    
    platforms = [
        { x: 0, y: 420, width: 1200, height: 100, type: 'roof' }
    ];
    hazards = [];
    items = [];
    particles = [];
}

// 무한 확장 맵 생성기 (더 다채롭고 넓은 간격)
function generateWorld() {
    let lastPlatform = platforms[platforms.length - 1];
    if (lastPlatform.x + lastPlatform.width < player.x + 1200) {
        let pWidth = Math.floor(Math.random() * 300) + 200;
        let pGap = Math.floor(Math.random() * 130) + 70; // 아슬아슬한 낭떠러지 간격
        let pHeight = Math.floor(Math.random() * 80) + 360;
        
        let newX = lastPlatform.x + lastPlatform.width + pGap;
        platforms.push({ x: newX, y: pHeight, width: pWidth, height: 160, type: 'roof' });

        // 장애물(벽) 배치 확률 증가 및 높이 변화
        if (Math.random() > 0.3) {
            let hHeight = Math.floor(Math.random() * 60) + 100;
            hazards.push({
                x: newX + pWidth - 50,
                y: pHeight - hHeight,
                width: 45,
                height: hHeight,
                type: 'wall'
            });
        }

        // 아이템(금화 및 부스터 생선) 배치
        if (Math.random() > 0.2) {
            items.push({
                x: newX + 80,
                y: pHeight - 70,
                radius: 12,
                type: Math.random() > 0.8 ? 'fish' : 'coin',
                collected: false
            });
        }
    }

    // 화면 지난 오브젝트 메모리 관리
    platforms = platforms.filter(p => p.x + p.width > player.x - 300);
    hazards = hazards.filter(h => h.x + h.width > player.x - 300);
    items = items.filter(i => i.x > player.x - 300);
}

// 이펙트 파티클 생성
function createParticles(x, y, color) {
    for (let i = 0; i < 8; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 8,
            vy: (Math.random() - 0.5) * 8,
            radius: Math.random() * 4 + 2,
            color: color,
            alpha: 1.0
        });
    }
}

// 키 입력 핸들러 (스페이스바 점프 및 연타 벽타기)
window.addEventListener("keydown", e => {
    if (e.code === "Space") {
        e.preventDefault();
        if (gameState === "START" || gameState === "GAMEOVER") {
            initGame();
            gameState = "PLAYING";
            return;
        }
        
        if (gameState === "PLAYING") {
            if (player.isWallSliding) {
                // 벽 부수고 튀어오르기 (벽킥 콤보)
                player.vy = jumpPower * 1.15;
                player.speed += 0.8; // 가속 붙음
                player.isWallSliding = false;
                combo++;
                triggerShake(8);
                createParticles(player.x, player.y, "#ffcc00");
            } else if (!player.isJumping || player.jumpCount < 2) {
                // 2단 점프
                player.vy = jumpPower;
                player.isJumping = true;
                player.jumpCount++;
                createParticles(player.x, player.y + player.height, "#ffffff");
            }
        }
    }
});

// 게임 루프 업데이트
function update() {
    if (gameState === "PLAYING") {
        // 부스터 모드 체크
        if (boosterTimer > 0) {
            boosterTimer--;
            player.speed = 16; // 슈퍼 하이퍼 스피드
        } else {
            // 시간이 지날수록 기본 속도가 서서히 빨라짐 (최고속도 13.5 제한)
            if (player.speed < 13.5) {
                player.speed += 0.002;
            }
        }

        player.x += player.speed;
        distance = Math.floor(player.x / 8);
        score = distance + (coins * 150) + (fishCount * 500) + (combo * 50);

        // 중력 적용
        if (player.isWallSliding) {
            player.vy = wallSlideGravity;
        } else {
            player.vy += gravity;
        }
        player.y += player.vy;

        // 지붕 충돌 체크
        player.isWallSliding = false;
        for (let p of platforms) {
            if (player.x + player.width > p.x && player.x < p.x + p.width) {
                if (player.y + player.height >= p.y && player.y + player.height - player.vy <= p.y + 12 && player.vy >= 0) {
                    player.y = p.y - player.height;
                    player.vy = 0;
                    player.isJumping = false;
                    player.jumpCount = 0;
                }
            }
        }

        // 장애물(벽) 충돌 및 벽타기 감지
        for (let h of hazards) {
            if (player.y + player.height > h.y && player.y < h.y + h.height) {
                if (player.x + player.width >= h.x && player.x < h.x + 15 && player.vy > 0) {
                    player.isWallSliding = true;
                    player.x = h.x - player.width;
                }
            }
        }

        // 아이템 획득 판정
        for (let item of items) {
            if (!item.collected) {
                let dist = Math.hypot((player.x + player.width/2) - item.x, (player.y + player.height/2) - item.y);
                if (dist < 30) {
                    item.collected = true;
                    if (item.type === 'coin') {
                        coins++;
                        createParticles(item.x, item.y, "#ffd700");
                    } else if (item.type === 'fish') {
                        fishCount++;
                        boosterTimer = 180; // 약 3초간 슈퍼 부스터
                        triggerShake(15);
                        createParticles(item.x, item.y, "#00ffcc");
                    }
                }
            }
        }

        // 낙사 체크
        if (player.y > canvas.height + 60) {
            gameState = "GAMEOVER";
            triggerShake(25);
        }

        // 파티클 업데이트
        for (let p of particles) {
            p.x += p.vx;
            p.y += p.vy;
            p.alpha -= 0.03;
        }
        particles = particles.filter(p => p.alpha > 0);

        generateWorld();
    }
}

// 렌더링 엔진
function draw() {
    ctx.save();
    
    // 화면 흔들림(Shake) 적용
    if (shakeTimer > 0) {
        shakeTimer--;
        let offsetX = (Math.random() - 0.5) * 10;
        let offsetY = (Math.random() - 0.5) * 10;
        ctx.translate(offsetX, offsetY);
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 아파트/기와의 실루엣 레이어
    ctx.fillStyle = "#1b2631";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 배경 달
    ctx.fillStyle = boosterTimer > 0 ? "#ff00ff" : "#f1c40f";
    ctx.beginPath();
    ctx.arc(850, 100, 50, 0, Math.PI * 2);
    ctx.fill();

    // 카메라 추적 변환
    ctx.save();
    ctx.translate(-player.x + 250, 0);

    // 플랫폼(기와 지붕) 렌더링
    for (let p of platforms) {
        ctx.fillStyle = "#2c3e50";
        ctx.fillRect(p.x, p.y, p.width, p.height);
        // 기와 문양 상단 라인
        ctx.fillStyle = "#e74c3c";
        ctx.fillRect(p.x, p.y, p.width, 8);
        ctx.strokeStyle = "#34495e";
        ctx.lineWidth = 3;
        ctx.strokeRect(p.x, p.y, p.width, p.height);
    }

    // 장애물 벽 렌더링
    for (let h of hazards) {
        ctx.fillStyle = "#34495e";
        ctx.fillRect(h.x, h.y, h.width, h.height);
        ctx.strokeStyle = "#111";
        ctx.lineWidth = 3;
        ctx.strokeRect(h.x, h.y, h.width, h.height);
        // 벽 벽돌 무늬 선
        ctx.strokeStyle = "#2c3e50";
        ctx.beginPath();
        ctx.moveTo(h.x, h.y + 20); ctx.lineTo(h.x + h.width, h.y + 20);
        ctx.moveTo(h.x, h.y + 50); ctx.lineTo(h.x + h.width, h.y + 50);
        ctx.stroke();
    }

    // 아이템 렌더링 (금화 & 생선 부스터)
    for (let item of items) {
        if (!item.collected) {
            ctx.beginPath();
            if (item.type === 'coin') {
                ctx.fillStyle = "#f1c40f";
                ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#d4ac0d";
                ctx.lineWidth = 3;
                ctx.stroke();
            } else {
                // 생선 아이템 (부스터)
                ctx.fillStyle = "#00ffff";
                ctx.ellipse(item.x, item.y, 16, 10, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        }
    }

    // 파티클 렌더링
    for (let p of particles) {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.globalAlpha = 1.0;

    // 플레이어 렌더링 (고양이 닌자)
    let playerColor = boosterTimer > 0 ? "#00ffff" : (player.isWallSliding ? "#e67e22" : "#ff5722");
    ctx.fillStyle = playerColor;
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    // 귀 장식
    ctx.fillStyle = "#d35400";
    ctx.beginPath();
    ctx.moveTo(player.x, player.y);
    ctx.lineTo(player.x + 12, player.y - 15);
    ctx.lineTo(player.x + 24, player.y);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(player.x + player.width - 24, player.y);
    ctx.lineTo(player.x + player.width - 12, player.y - 15);
    ctx.lineTo(player.x + player.width, player.y);
    ctx.fill();

    ctx.restore();

    // HUD UI 오버레이 (점수, 코인, 부스터 게이지)
    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
    ctx.fillRect(20, 20, 360, 75);
    ctx.strokeStyle = "#ffcc00";
    ctx.lineWidth = 2;
    ctx.strokeRect(20, 20, 360, 75);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 20px Arial";
    ctx.fillText("점수: " + score, 35, 50);
    ctx.fillText("🪙 코인: " + coins, 200, 50);
    ctx.fillText("🐟 생선: " + fishCount, 300, 50);
    ctx.fillText("🔥 콤보: " + combo, 35, 80);

    if (boosterTimer > 0) {
        ctx.fillStyle = "#00ffff";
        ctx.font = "bold 22px Arial";
        ctx.fillText("⚡ SUPER BOOSTER!", 200, 80);
    }

    // 상태 메시지 (시작 / 게임오버)
    if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#ffcc00";
        ctx.font = "bold 44px Arial";
        ctx.textAlign = "center";
        ctx.fillText("🐱 고 군 분 투 : 하 이 퍼 ⚡", canvas.width / 2, canvas.height / 2 - 40);
        ctx.fillStyle = "#ffffff";
        ctx.font = "20px Arial";
        ctx.fillText("스페이스바를 눌러 초고속 질주를 시작하세요!", canvas.width / 2, canvas.height / 2 + 15);
        ctx.fillText("점프 & 벽에 닿을 때 스페이스바 연타로 벽타기 콤보!", canvas.width / 2, canvas.height / 2 + 55);
        ctx.textAlign = "left";
    } else if (gameState === "GAMEOVER") {
        ctx.fillStyle = "rgba(180, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 44px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 40);
        ctx.font = "22px Arial";
        ctx.fillText("최종 점수: " + score + " 점", canvas.width / 2, canvas.height / 2 + 10);
        ctx.fillText("다시 도전하려면 스페이스바를 누르세요!", canvas.width / 2, canvas.height / 2 + 55);
        ctx.textAlign = "left";
    }

    ctx.restore();
}

// 메인 아케이드 루프
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

st.components.v1.html(game_code, height=560, scrolling=False)
