        window.startBrickGame = function() {
            overlay.classList.remove('d-flex');
            overlay.classList.add('d-none');
            x = canvas.width/2;
            y = canvas.height-30;
            dx = 4;
            dy = -4;
            paddleX = (canvas.width-paddleWidth)/2;
            score = 0;
            lives = 3;
            initBricks();
            isPlaying = true;
            draw();
        }

        function gameOver(win) {
            isPlaying = false;
            cancelAnimationFrame(animationId);
            overlay.classList.remove('d-none');
            overlay.classList.add('d-flex');
            if(win) {
                title.innerText = "YOU WIN!";
                title.className = "text-success fw-bold mb-4";
            } else {
                title.innerText = "GAME OVER";
                title.className = "text-danger fw-bold mb-4";
            }
            btn.innerText = "PLAY AGAIN";
        }
