const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const player = {
  x: canvas.width / 2,
  y: canvas.height - 70,
  width: 70,
  height: 70,
  speed: 0,  // Initial speed
  acceleration: 0.5,  // Acceleration factor
  friction: 0.5,     // Friction factor
  maxSpeed: 5
};

const target = {
  width: 70,
  height: 70,
}

const bullets = [];
const targets = [];
let score = 0;


function drawPlayer() {
  const jetImage = new Image();
  jetImage.src = 'jet.png'; // Replace 'jet.png' with your image file name
  ctx.drawImage(jetImage, player.x, player.y, player.width, player.height);
}

function drawBullets() {
  ctx.fillStyle = 'red';
  bullets.forEach(bullet => {
    ctx.fillRect(bullet.x, bullet.y, 5, 10);
  });
}

function drawTargets() {
  targets.forEach(target => {
    const enemyImage = new Image();
    enemyImage.src = 'bad.png'; // Replace with appropriate enemy jet image
    ctx.drawImage(enemyImage, target.x, target.y, target.width = 50, target.height = 50);
  });
}

function moveBullets() {
  bullets.forEach(bullet => {
    bullet.y -= 5;
  });
  bullets.filter(bullet => bullet.y > 0);
}

function moveTargets() {
  targets.forEach(target => {
    target.y += 2;
    if (target.y > canvas.height) {
      target.y = 0;
      target.x = Math.random() * (canvas.width - 30);
    }
  });
}

function checkCollisions() {
  bullets.forEach(bullet => {
    for (let i = targets.length - 1; i >= 0; i--) {
      const target = targets[i];
      if (
        bullet.x > target.x && bullet.x < target.x + 30 &&
        bullet.y > target.y && bullet.y < target.y + 30
      ) {
        score += 10; // Increment score by 10 points
        targets.splice(i, 1);
        bullet.y = -10; // Move bullet off-screen
      }
    }
  });
}



function createTarget() {
  const target = {
    x: Math.random() * (canvas.width - 30),
    y: 0,
    width: 30,
    height: 30,
  };
  targets.push(target);
}

function updatePlayerPosition() {
  if (isMovingLeft) {
    player.speed -= player.acceleration;
  } else if (isMovingRight) {
    player.speed += player.acceleration;
  } else {
    player.speed *= player.friction;
  }

  if (player.speed > player.maxSpeed) {
    player.speed = player.maxSpeed;
  } else if (player.speed < -player.maxSpeed) {
    player.speed = -player.maxSpeed;
  }

  player.x += player.speed;

  if (player.x < 0) {
    player.x = 0;
    player.speed = 0;
  } else if (player.x > canvas.width - player.width) {
    player.x = canvas.width - player.width;
    player.speed = 0;
  }
}


function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  updatePlayerPosition();
  drawPlayer();
  drawBullets();
  drawTargets();

  moveBullets();
  moveTargets();
  checkCollisions();

  // Generate new target periodically
  if (Math.random() < 0.01) {
    createTarget();
  }

  // Update the score display
  document.getElementById('score').textContent = 'Score: ' + score;

  requestAnimationFrame(draw);
}


function gameLoop() {
  draw();
}

let isMovingLeft = false;
let isMovingRight = false;

document.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') {
    isMovingLeft = true;
  } else if (event.key === 'ArrowRight') {
    isMovingRight = true;
  }
  
  if (event.key === ' ') {
    bullets.push({ x: player.x + player.width / 2 - 2.5, y: player.y });
  }
});

document.addEventListener('keyup', event => {
  if (event.key === 'ArrowLeft') {
    isMovingLeft = false;
  } else if (event.key === 'ArrowRight') {
    isMovingRight = false;
  }
});

gameLoop();
