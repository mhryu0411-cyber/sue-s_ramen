import streamlit as st

# Streamlit 페이지 설정 (와이드 레이아웃)
st.set_page_config(
    page_title="고군분투 리메이크 - 익스트림 부스터 에디션",
    page_icon="🐱",
    layout="wide"
)

st.title("🐱 고군분투: 익스트림 하이퍼 질주! (Extreme Go Go!)")
st.markdown("🚀 **벽 삭제 & 낭떠러지 간격 대폭 확장!** 스페이스바를 연타해 아슬아슬하게 지붕 사이를 뛰어넘으세요. **생선(🐟)을 먹으면 화면이 흔들리며 미친듯한 슈퍼 부스터**가 발동됩니다!")

# HTML5 + Canvas + JS 익스트림 아케이드 엔진
game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>고군분투 익스트림</title>
    <style>
        body {
            margin: 0;
            background-color: #0b0b0f;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Arial', sans-serif;
        }
        canvas {
            border: 4px solid #00ffff;
            box-shadow: 0 0 35px rgba(0, 255, 255, 0.4);
            background: linear-gradient(to bottom, #050508, #101820, #1a2634);
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
let shakeTimer = 0;
let boosterTimer = 0;

// 플레이어 객체 (익스트림 닌자 고양이)
let player = {
    x: 150,
    y: 350,
    width: 38,
    height: 48,
    vy: 0,
    baseSpeed: 10,      // 기본 속도감 상향
    speed: 10,
    isJumping: false,
    jumpCount: 0
};

// 물리 상수 (와이드 갭에 최적화된 호쾌한 점프)
const gravity = 0.68;
const jumpPower = -13.8;

// 월드 오브젝트 (지붕 및 아이템)
let platforms = [];
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
    boosterTimer = 0;
    player.x = 150;
    player.y = 300;
    player.vy = 0;
    player.isJumping = false;
    player.jumpCount = 0;
    player.speed = player.baseSpeed;
    
    // 시작 지붕
    platforms = [
        { x: 0, y: 420, width: 1400, height: 100 }
    ];
    items = [];
    particles = [];
}

// 무한 확장 맵 생성기 (벽 제거, 넓고 짜릿한 간격 적용)
function generateWorld() {
    let lastPlatform = platforms[platforms.length - 1];
    if (lastPlatform.x + lastPlatform.width < player.x + 1400) {
        let pWidth = Math.floor(Math.random() * 320) + 220; // 지붕 너비
        let pGap = Math.floor(Math.random() * 160) + 110;   // 넓어진 낭떠러지 간격!
        let pHeight = Math.floor(Math.random() * 90) + 350;  // 높낮이 변화
        
        let newX = lastPlatform.x + lastPlatform.width + pGap;
        platforms.push({ x: newX, y: pHeight, width: pWidth, height: 160 });

        // 아이템(금화 또는 극적 부스터 생선) 배치
        if (Math.random() > 0.15) {
            let isFish = Math.random() > 0.75; // 25% 확률로 생선 등장
            items.push({
                x: newX + pWidth / 2,
                y: pHeight - 75,
                radius: isFish ? 14 : 11,
                type: isFish ? 'fish' : 'coin',
                collected: false
            });
        }
    }

    // 화면 지난 오브젝트 메모리 정리
    platforms = platforms.filter(p => p.x + p.width > player.x - 300);
    items = items.filter(i => i.x > player.x - 300);
}

// 파티클 생성기
function createParticles(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            radius: Math.random() * 5 + 2,
            color: color,
            alpha: 1.0
        });
    }
}

// 키 입력 핸들러 (스페이스바 점프 / 2단 점프)
window.addEventListener("keydown", e => {
    if (e.code === "Space") {
        e.preventDefault();
        if (gameState === "START" || gameState === "GAMEOVER") {
            initGame();
            gameState = "PLAYING";
            return;
        }
        
        if (gameState === "PLAYING") {
            if (!player.isJumping || player.jumpCount < 2) {
                player.vy = jumpPower;
                player.isJumping = true;
                player.jumpCount++;
                triggerShake(4);
                createParticles(player.x + player.width/2, player.y + player.height, "#00ffff", 6);
            }
        }
    }
});

// 게임 루프 업데이트
function update() {
    if (gameState === "PLAYING") {
        // 슈퍼 부스터 모드 계산
        if (boosterTimer > 0) {
            boosterTimer--;
            player.speed = 18; // 광속 하이퍼 스피드!
            if (Math.random() > 0.4) {
                createParticles(player.x, player.y + player.height/2, "#ff00ff", 2);
            }
        } else {
            // 시간이 지날수록 점진적 가속 (최고 기본속도 14 제한)
            if (player.speed < 14) {
                player.speed += 0.0025;
            }
        }

        player.x += player.speed;
        distance = Math.floor(player.x / 8);
        score = distance + (coins * 200) + (fishCount * 1000);

        // 중력 적용
        player.vy += gravity;
        player.y += player.vy;

        // 지붕(땅바닥) 충돌 판정
        let landed = false;
        for (let p of platforms) {
            if (player.x + player.width > p.x && player.x < p.x + p.width) {
                if (player.y + player.height >= p.y && player.y + player.height - player.vy <= p.y + 14 && player.vy >= 0) {
                    player.y = p.y - player.height;
                    player.vy = 0;
                    player.isJumping = false;
                    player.jumpCount = 0;
                    landed = true;
                }
            }
        }

        // 아이템 획득 판정
        for (let item of items) {
            if (!item.collected) {
                let dist = Math.hypot((player.x + player.width/2) - item.x, (player.y + player.height/2) - item.y);
                if (dist < 32) {
                    item.collected = true;
                    if (item.type === 'coin') {
                        coins++;
                        createParticles(item.x, item.y, "#ffd700", 8);
                    } else if (item.type === 'fish') {
                        fishCount++;
                        boosterTimer = 220; // 약 3.5초간 극적인 슈퍼 부스터!
                        triggerShake(25);   // 화면이 쿵 하고 흔들림
                        createParticles(item.x, item.y, "#ff00ff", 25);
                    }
                }
            }
        }

        // 낙사 판정 (낭떠러지 추락)
        if (player.y > canvas.height + 60) {
            gameState = "GAMEOVER";
            triggerShake(30);
        }

        // 파티클 업데이트
        for (let p of particles) {
            p.x += p.vx;
            p.y += p.vy;
            p.alpha -= 0.035;
        }
        particles = particles.filter(p => p.alpha > 0);

        generateWorld();
    }
}

// 렌더링 엔진
function draw() {
    ctx.save();
    
    // 화면 흔들림(Shake) 연출
    if (shakeTimer > 0) {
        shakeTimer--;
        let offsetX = (Math.random() - 0.5) * 14;
        let offsetY = (Math.random() - 0.5) * 14;
        ctx.translate(offsetX, offsetY);
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 배경 실루엣
    ctx.fillStyle = boosterTimer > 0 ? "#1a0033" : "#0d1b2a";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 배경 달 (부스터 시 네온 퍼플로 변함)
    ctx.fillStyle = boosterTimer > 0 ? "#ff00ff" : "#00ffff";
    ctx.beginPath();
    ctx.arc(850, 90, 45, 0, Math.PI * 2);
    ctx.fill();

    // 카메라 스크롤 변환
    ctx.save();
    ctx.translate(-player.x + 250, 0);

    // 지붕 렌더링
    for (let p of platforms) {
        ctx.fillStyle = "#1b2631";
        ctx.fillRect(p.x, p.y, p.width, p.height);
        // 기와 상단 네온 라인
        ctx.fillStyle = boosterTimer > 0 ? "#ff00ff" : "#00ffff";
        ctx.fillRect(p.x, p.y, p.width, 6);
        ctx.strokeStyle = "#415a77";
        ctx.lineWidth = 3;
        ctx.strokeRect(p.x, p.y, p.width, p.height);
    }

    // 아이템 렌더링
    for (let item of items) {
        if (!item.collected) {
            ctx.beginPath();
            if (item.type === 'coin') {
                ctx.fillStyle = "#f1c40f";
                ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 2;
                ctx.stroke();
            } else {
                // 생선 부스터 아이템 (반짝이는 네온 효과)
                ctx.fillStyle = "#ff00ff";
                ctx.ellipse(item.x, item.y, 18, 11, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#00ffff";
                ctx.lineWidth = 3;
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
    let playerColor = boosterTimer > 0 ? "#ff00ff" : "#ff5722";
    ctx.fillStyle = playerColor;
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    // 귀 디자인
    ctx.fillStyle = boosterTimer > 0 ? "#00ffff" : "#d35400";
    ctx.beginPath();
    ctx.moveTo(player.x, player.y);
    ctx.lineTo(player.x + 10, player.y - 14);
    ctx.lineTo(player.x + 20, player.y);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(player.x + player.width - 20, player.y);
    ctx.lineTo(player.x + player.width - 10, player.y - 14);
    ctx.lineTo(player.x + player.width, player.y);
    ctx.fill();

    ctx.restore();

    // HUD UI 오버레이
    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(20, 20, 380, 75);
    ctx.strokeStyle = boosterTimer > 0 ? "#ff00ff" : "#00ffff";
    ctx.lineWidth = 2;
    ctx.strokeRect(20, 20, 380, 75);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 20px Arial";
    ctx.fillText("점수: " + score, 35, 50);
    ctx.fillText("🪙 코인: " + coins, 190, 50);
    ctx.fillText("🐟 생선: " + fishCount, 295, 50);

    if (boosterTimer > 0) {
        ctx.fillStyle = "#ff00ff";
        ctx.font = "bold 22px Arial";
        ctx.fillText("⚡ EXTREME SUPER BOOSTER!!", 35, 80);
    } else {
        ctx.fillStyle = "#00ffff";
        ctx.font = "16px Arial";
        ctx.fillText("팁: 생선(🐟)을 먹으면 광속 질주!", 35, 80);
    }

    // 상태 메시지 (시작 / 게임오버)
    if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#00ffff";
        ctx.font = "bold 40px Arial";
        ctx.textAlign = "center";
        ctx.fillText("🐱 고 군 분 투 : 익 스 트 림 ⚡", canvas.width / 2, canvas.height / 2 - 40);
        ctx.fillStyle = "#ffffff";
        ctx.font = "19px Arial";
        ctx.fillText("스페이스바를 눌러 넓은 낭떠러지 질주를 시작하세요!", canvas.width / 2, canvas.height / 2 + 10);
        ctx.fillText("스페이스바 연타로 아슬아슬한 2단 점프 활용!", canvas.width / 2, canvas.height / 2 + 50);
        ctx.textAlign = "left";
    } else if (gameState === "GAMEOVER") {
        ctx.fillStyle = "rgba(150, 0, 0, 0.85)";
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

st.components.v1.html(game_code, height=560, scrolling=False)
