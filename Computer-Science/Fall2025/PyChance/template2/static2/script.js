/* ================= USER INFO ================= */
const currentUser = localStorage.getItem("pychance_user");
let accounts = JSON.parse(localStorage.getItem("pychance_accounts")) || {}; 
    if (!currentUser || !accounts[currentUser]) {
    // Not logged in or user missing
    window.location.href = "login.html";
}
function updateUserInfo() {
    const username = localStorage.getItem("username") || "Player1";
    const points = localStorage.getItem("points") || 50;

    document.querySelectorAll("#usernameDisplay, #usernameCenter")
            .forEach(el => el.textContent = username);
    document.getElementById("pointsDisplay").textContent = points;
}

// Call on page load
updateUserInfo();


// Display on UI
document.getElementById('pointsDisplay').textContent = points;
document.getElementById('usernameDisplay').textContent = currentUser;

let points = parseInt(localStorage.getItem('points'));
document.getElementById('pointsDisplay').textContent = points;
document.getElementById('usernameDisplay').textContent = localStorage.getItem('username');

/* ================= PAGE SWITCHING ================= */
function openGame(id){
    document.getElementById('homePage').style.display='none';
    document.querySelectorAll('.game-view').forEach(v=>v.style.display='none');
    document.getElementById(id+'View').style.display='flex';
}
function backHome(){
    document.querySelectorAll('.game-view').forEach(v=>v.style.display='none');
    document.getElementById('homePage').style.display='flex';
}

/* ================= HISTORY ================= */
function addHistory(listId, game, result){
    const li = document.createElement('li');
    const now = new Date();
    const time = now.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    li.innerHTML=`<span>${game}: ${result}</span><span class='history-time'>${time}</span>`;
    document.getElementById(listId).appendChild(li);
}
/* ================= MENU TOGGLE ================= */
function toggleMenu() {
  const menu = document.getElementById("menuLinks");
  menu.style.display = menu.style.display === "flex" ? "none" : "flex";
}

function updateUserInfo() {
  const username = localStorage.getItem("username") || "Player1";
  const points = parseInt(localStorage.getItem("points") || 25);
  document.getElementById("usernameDisplay").textContent = username;
  document.getElementById("pointsDisplay").textContent = points;
}

updateUserInfo();



/* ================= ROULETTE WHEEL ================= */
let rouletteWins = 0;
function spinRoulette(){
    const wheel = document.getElementById("rouletteWheel");
    const ball = document.getElementById("rouletteBall");

    wheel.classList.remove("spin");
    void wheel.offsetWidth;
    wheel.classList.add("spin");

    const result = Math.floor(Math.random()*36)+1;
    const angle = (result / 36) * 360;
    ball.style.transform = `rotate(${angle}deg) translate(120px)`;

    setTimeout(()=>{
        document.getElementById('rouletteResult').textContent = "Number: " + result;
        if(result % 2 === 0){ points += 10; rouletteWins++; }
        else { points -= 5; }
        document.getElementById('pointsDisplay').textContent = points;
        document.getElementById('rouletteWins').textContent = rouletteWins;
        localStorage.setItem('points',points);
        addHistory('rouletteHistory','Roulette',result);
    },3000);
}

/* ================= COIN FLIP ================= */
let coinWins = 0; let userGuess = null;
function setGuess(choice){ userGuess=choice; document.getElementById('coinResult').textContent="You picked "+choice; }
function flipCoin() {
    if(!userGuess) return alert("Pick Heads or Tails");
    if(round >= maxRounds) return alert("Game over. Click Back to restart.");

    const coin = document.getElementById('coin');

    // Start coin flip animation
    coin.classList.add("flip-animate");

    // Wait for animation to finish (2s)
    setTimeout(() => {
        // Remove animation class so it can flip again
        coin.classList.remove("flip-animate");

        // Determine result
        const result = Math.random() < 0.5 ? "Heads" : "Tails";
        let pointsChange = 0;
        let roundMessage = "";

        if(userGuess === result){
            coinWins++;
            pointsChange = +10;
            roundPoints += pointsChange;
            roundMessage = "You won this round!";
            confetti({ particleCount: 100, spread: 70, origin: {y:0.6} });
        } else {
            computerWins++;
            pointsChange = -5;
            roundPoints += pointsChange;
            roundMessage = "Computer won this round.";
        }

        round++;

        document.getElementById('coinResult').textContent = `Coin: ${result}`;
        document.getElementById('gameMessage').textContent = roundMessage;
        document.getElementById('coinWins').textContent = coinWins;
        document.getElementById('roundDisplay').textContent = `Round: ${round} / ${maxRounds}`;

        addHistory('coinHistory', 'Coin Flip', result, pointsChange);

        userGuess = null;

        if(round === maxRounds){
            let msg;
            if(coinWins > computerWins){
                points += roundPoints;
                msg = `You won the game! You keep ${roundPoints} points.`;
            } else {
                roundPoints = 0;
                msg = "Computer won the game. All earned points lost.";
            }

            document.getElementById('gameMessage').textContent = msg;
            document.getElementById('pointsDisplay').textContent = points;
            localStorage.setItem('points', points);

            // Reset for next game
            round = coinWins = computerWins = roundPoints = 0;
            document.getElementById('roundDisplay').textContent = `Round: 0 / ${maxRounds}`;
            document.getElementById('coinWins').textContent = coinWins;
        }
    }, 2000); // match CSS animation duration
}


/* ================= SLOTS ================= */
let slotsWins = 0;
function spinSlots(){
    const symbols=["🍒","🍋","🍊","🍇","🍉"];
    const reels=document.querySelectorAll('#slotsReels .reel');
    reels.forEach((reel,i)=>{
        let spins=10+i*5;
        let interval=setInterval(()=>{ reel.textContent=symbols[Math.floor(Math.random()*symbols.length)]; },50);
        setTimeout(()=>{ clearInterval(interval); }, spins*50);
    });
    setTimeout(()=>{
        const final=Array.from({length:3},()=>symbols[Math.floor(Math.random()*symbols.length)]);
        reels.forEach((r,i)=> r.textContent=final[i]);
        let setSize=new Set(final).size;
        if(setSize===1){ points+=20; slotsWins++; } 
        else if(setSize===2){ points+=10; } 
        else { points-=5; }
        document.getElementById('pointsDisplay').textContent=points;
        document.getElementById('slotsWins').textContent=slotsWins;
        localStorage.setItem('points',points);
        addHistory('slotsHistory','Slots',final.join(" | "));
    },1000);
}