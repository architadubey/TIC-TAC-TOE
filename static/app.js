document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Elements ---
    const mainMenu = document.getElementById('main-menu');
    const gameView = document.getElementById('game-view');
    
    // Toggles
    const modeToggle = document.getElementById('mode-toggle');
    const diffGroup = document.getElementById('difficulty-group');
    const diffToggle = document.getElementById('diff-toggle');
    const turnToggle = document.getElementById('turn-toggle');
    
    // Game Elements
    const boardEl = document.getElementById('board');
    const statusText = document.getElementById('status-text');
    const p1ScoreEl = document.getElementById('p1-score');
    const p2ScoreEl = document.getElementById('p2-score');
    const drawsScoreEl = document.getElementById('draws-score');
    
    const p1Label = document.getElementById('p1-label');
    const p2Label = document.getElementById('p2-label');
    
    // Buttons
    const startBtn = document.getElementById('start-btn');
    const menuBtn = document.getElementById('menu-btn');
    const playAgainBtn = document.getElementById('play-again-btn');
    
    // Win Line
    const winLineSvg = document.getElementById('win-line-svg');
    const winLine = document.getElementById('win-line');

    // --- State ---
    let settings = {
        mode: 'PVC', // 'PVC' or 'PVP'
        difficulty: 'Unbeatable',
        firstTurn: 'Player'
    };
    
    let scores = { p1: 0, p2: 0, draws: 0 };
    let board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ];
    let currentPlayer = 'X';
    let gameOver = false;
    let aiSymbol = 'O'; // updated dynamically via firstTurn
    let humanSymbol = 'X'; 
    let isComputerThinking = false;

    // --- Helper: Toggle Setup ---
    function setupToggle(containerArray, callback) {
        containerArray.forEach(container => {
            const options = container.querySelectorAll('.toggle-option');
            options.forEach(opt => {
                opt.addEventListener('click', () => {
                    options.forEach(o => o.classList.remove('active'));
                    opt.classList.add('active');
                    if(callback) callback(container.id, opt.dataset.val);
                });
            });
        });
    }

    setupToggle([modeToggle, diffToggle, turnToggle], (containerId, val) => {
        if(containerId === 'mode-toggle') {
            settings.mode = val;
            if (val === 'PVP') {
                diffGroup.classList.add('hidden');
                // Update turn options
                turnToggle.children[0].textContent = "Player 1";
                turnToggle.children[0].dataset.val = "P1";
                turnToggle.children[1].textContent = "Player 2";
                turnToggle.children[1].dataset.val = "P2";
            } else {
                diffGroup.classList.remove('hidden');
                turnToggle.children[0].textContent = "Player";
                turnToggle.children[0].dataset.val = "Player";
                turnToggle.children[1].textContent = "Computer";
                turnToggle.children[1].dataset.val = "Computer";
            }
        }
        else if (containerId === 'diff-toggle') settings.difficulty = val;
        else if (containerId === 'turn-toggle') settings.firstTurn = val;
    });

    // --- Transition to Game ---
    startBtn.addEventListener('click', () => {
        mainMenu.classList.remove('active');
        setTimeout(() => {
            gameView.classList.add('active');
            initGame();
        }, 300); // Wait for fade out
    });

    menuBtn.addEventListener('click', () => {
        gameView.classList.remove('active');
        scores = { p1: 0, p2: 0, draws: 0 }; // Full RESET
        setTimeout(() => mainMenu.classList.add('active'), 300);
    });

    playAgainBtn.addEventListener('click', () => {
        playAgainBtn.classList.add('hidden');
        initGame();
    });

    // --- Game Logic ---
    function initGame() {
        // Build empty state
        board = [["", "", ""], ["", "", ""], ["", "", ""]];
        currentPlayer = 'X';
        gameOver = false;
        isComputerThinking = false;
        
        // Hide SVG line
        winLine.style.opacity = '0';
        waitAndResetSVG();

        // Figure out symbols for PVC
        if (settings.mode === 'PVC') {
            if (settings.firstTurn === 'Computer') {
                aiSymbol = 'X';
                humanSymbol = 'O';
            } else {
                aiSymbol = 'O';
                humanSymbol = 'X';
            }
            p1Label.textContent = aiSymbol === 'X' ? 'Computer' : 'Player';
            p2Label.textContent = aiSymbol === 'O' ? 'Computer' : 'Player';
        } else {
            p1Label.textContent = 'Player 1';
            p2Label.textContent = 'Player 2';
        }

        // Render board visuals
        renderBoard();
        updateScores();
        updateStatus();

        // If computer goes first
        if (settings.mode === 'PVC' && settings.firstTurn === 'Computer') {
            triggerComputerMove();
        }
    }

    function waitAndResetSVG() {
        // Reset stroke properties silently
        setTimeout(() => {
            winLine.style.transition = 'none';
            winLine.setAttribute('stroke-dasharray', '0, 1000');
            setTimeout(() => winLine.style.transition = 'stroke-dashoffset 0.5s ease-in-out', 50);
        }, 50);
    }

    function renderBoard() {
        boardEl.innerHTML = '';
        for(let r=0; r<3; r++) {
            for(let c=0; c<3; c++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.r = r;
                cell.dataset.c = c;
                
                // Add token classes if occupied
                if (board[r][c] !== "") {
                    cell.textContent = board[r][c];
                    cell.classList.add(board[r][c].toLowerCase());
                } else {
                    // Update CSS hover state token
                    if (!gameOver && (!isComputerThinking)) {
                        cell.dataset.hover = currentPlayer;
                    }
                }

                cell.addEventListener('click', () => handleCellClick(r, c));
                boardEl.appendChild(cell);
            }
        }
    }

    function updateAllHovers() {
        document.querySelectorAll('.cell').forEach(cell => {
             if (board[cell.dataset.r][cell.dataset.c] === "") {
                 cell.dataset.hover = currentPlayer;
             } else {
                 cell.removeAttribute('data-hover');
             }
        });
    }

    function removeAllHovers() {
        document.querySelectorAll('.cell').forEach(cell => cell.removeAttribute('data-hover'));
    }

    async function handleCellClick(r, c) {
        if (gameOver || isComputerThinking || board[r][c] !== "") return;
        
        // Execute move
        makeMove(r, c);
    }

    function makeMove(r, c) {
        board[r][c] = currentPlayer;
        
        // Switch turn
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        
        renderBoard(); // Update visual state heavily reliant on variables above
        
        const winner = checkWinner();
        if (winner) {
            endGame(winner);
            return;
        }

        if (isDraw()) {
            endGame('Draw');
            return;
        }

        updateStatus();

        // Check if next move is AI's
        if (settings.mode === 'PVC' && currentPlayer === aiSymbol) {
            triggerComputerMove();
        } else {
            updateAllHovers(); 
        }
    }

    function triggerComputerMove() {
        isComputerThinking = true;
        removeAllHovers();
        statusText.textContent = "Computer is thinking...";
        
        // Add dynamic animated text "..."
        let dots = 0;
        const dotInterval = setInterval(() => {
            if(!isComputerThinking) { clearInterval(dotInterval); return; }
            dots = (dots + 1) % 4;
            statusText.textContent = "Computer is thinking" + ".".repeat(dots);
        }, 300);

        // Fetch move from API
        fetch('/api/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                board: board,
                difficulty: settings.difficulty,
                ai_symbol: aiSymbol
            })
        })
        .then(res => res.json())
        .then(data => {
            isComputerThinking = false;
            clearInterval(dotInterval);
            
            const move = data.move; // [r, c]
            if (move[0] !== -1) {
                // slight delay for realism
                setTimeout(() => makeMove(move[0], move[1]), 300);
            }
        })
        .catch(err => {
            console.error("AI Error", err);
            isComputerThinking = false;
        });
    }

    function updateStatus() {
        if (gameOver) return;
        if (settings.mode === 'PVC') {
             statusText.textContent = currentPlayer === humanSymbol ? "Your Turn" : "Computer's Turn";
        } else {
             statusText.textContent = `Player ${currentPlayer === 'X' ? '1' : '2'}'s Turn`;
        }
    }

    function checkWinner() {
        const b = board;
        let line = null;
        let winner = null;

        // Rows
        for(let i=0; i<3; i++) {
            if(b[i][0] === b[i][1] && b[i][1] === b[i][2] && b[i][0] !== "") { winner = b[i][0]; line = {r1:i, c1:0, r2:i, c2:2}; break; }
            if(b[0][i] === b[1][i] && b[1][i] === b[2][i] && b[0][i] !== "") { winner = b[0][i]; line = {r1:0, c1:i, r2:2, c2:i}; break; }
        }
        
        if (!winner) {
            if(b[0][0] === b[1][1] && b[1][1] === b[2][2] && b[0][0] !== "") { winner = b[0][0]; line = {r1:0, c1:0, r2:2, c2:2}; }
            else if(b[0][2] === b[1][1] && b[1][1] === b[2][0] && b[0][2] !== "") { winner = b[0][2]; line = {r1:0, c1:2, r2:2, c2:0}; }
        }

        if (winner) {
            drawWinLine(line);
            return winner;
        }
        return null;
    }

    function isDraw() {
        return board.every(row => row.every(cell => cell !== ""));
    }

    function drawWinLine(lineDef) {
        // Get dimensions
        const rect = boardEl.getBoundingClientRect();
        // Container size is 300x300, gaps are 8px, cells are ~94x94
        function getCenter(r, c) {
            // formula approx: cellSize * idx + gap * idx + padding
            // Easier math: size is 300. Thirds are 100. Center is 50.
            return {
                x: (c * 100) + 50,
                y: (r * 100) + 50
            }
        }

        const p1 = getCenter(lineDef.r1, lineDef.c1);
        const p2 = getCenter(lineDef.r2, lineDef.c2);

        // Extend the line by 30px on each side
        const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
        const extend = 35;

        const x1 = p1.x - Math.cos(angle) * extend;
        const y1 = p1.y - Math.sin(angle) * extend;
        const x2 = p2.x + Math.cos(angle) * extend;
        const y2 = p2.y + Math.sin(angle) * extend;

        const length = Math.hypot(x2 - x1, y2 - y1);

        winLine.setAttribute('x1', x1);
        winLine.setAttribute('y1', y1);
        winLine.setAttribute('x2', x2);
        winLine.setAttribute('y2', y2);
        
        winLine.style.opacity = '1';
        
        // CSS Animation setup
        winLine.setAttribute('stroke-dasharray', length);
        winLine.setAttribute('stroke-dashoffset', length);
        
        // Trigger reflow
        winLine.getBoundingClientRect();
        
        winLine.setAttribute('stroke-dashoffset', 0);
    }

    function endGame(result) {
        gameOver = true;
        removeAllHovers();
        playAgainBtn.classList.remove('hidden');

        if (result === 'Draw') {
            statusText.textContent = "It's a Draw!";
            statusText.style.color = '#fde047'; /* Yellow */
            scores.draws++;
        } else {
            // result is 'X' or 'O'
            let winnerName = "";
            let color = '';
            
            if (settings.mode === 'PVC') {
                if (result === humanSymbol) {
                    winnerName = "Player";
                    scores.p1++; // p1 is always the player visually, or wait, we set it dynamically.
                } else {
                    winnerName = "Computer";
                    scores.p2++; 
                }
            } else {
                if (result === 'X') {
                    winnerName = "Player 1";
                    scores.p1++;
                } else {
                    winnerName = "Player 2";
                    scores.p2++;
                }
            }
            
            statusText.textContent = `${winnerName} Wins!`;
            statusText.style.color = '#4ade80'; /* Green win */
        }
        
        updateScores();
        
        setTimeout(() => {
            statusText.style.color = ''; // reset color after some time
        }, 3000);
    }

    function updateScores() {
        // Wait, depending on who is X or O in PVC, p1 might be computer.
        // Let's standardise the scoreboard visual updating specifically for clarity.
        if (settings.mode === 'PVC') {
             p1ScoreEl.textContent = settings.firstTurn === 'Computer' ? scores.p2 : scores.p1;
             p2ScoreEl.textContent = settings.firstTurn === 'Computer' ? scores.p1 : scores.p2;
        } else {
             p1ScoreEl.textContent = scores.p1;
             p2ScoreEl.textContent = scores.p2;
        }
        drawsScoreEl.textContent = scores.draws;
    }

});
