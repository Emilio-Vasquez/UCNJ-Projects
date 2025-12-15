var cartcookie
const cartlist = document.getElementById("cartlist");
var div = document.createElement('div');
var total = 0
var balance 

AIRJORDAN1LOWSE = `
    <div class="test">
        <img src="../assets/AIRJORDAN1LOWSE.webp">
        <div class="name">Air Jordan 1 Low SE</div>
        <div class="name">$15</div>
    </div>
`;
AIRJORDAN12RETRO = `
    <div><img src="../assets/AIRJORDAN12RETRO.webp">
        <div class="name">Air Jordan 12 Retro</div>
        <div class="name">$20</div>
    </div>
`;
AIRJORDAN4RETRO = `
    <div><img src="../assets/AIRJORDAN4RETRO.webp">
        <div class="name">Air Jordan 4 Retro</div>
        <div class="name">$14</div>
    </div> 
`;
JORDANFLIGHTCOURT = `
    <div><img src="../assets/JORDANFLIGHTCOURT.webp">
        <div class="name">Jordan Flight Court</div>
        <div class="name">$18</div>
    </div>
`;
JORDANZION4 = `
    <div><img src="../assets/JORDANZION4.webp">
        <div class="name">Jordan Zion 4</div>
        <div class="name">$19</div>
    </div>
`;
AIRJORDAN3RETROMEX = `
    <div><img src="../assets/AIRJORDAN3RETROMEX.avif">
        <div class="name">Air Jordan 3 Retro Mex</div>
        <div class="name">$12</div>
    </div>
`;
AIRJORDAN14G = `
    <div><img src="../assets/AIRJORDAN14G.avif">
        <div class="name">Air Jordan 14G</div>
        <div class="name">$10</div>
    </div>
`;
AIRJORDAN9RETROBOOTNRG = `
    <div><img src="../assets/AIRJORDAN9RETROBOOTNRG.avif">
        <div class="name">Air Jordan 9 Retro Boot NRG</div>
        <div class="name">$25</div>
    </div>
`;
JORDANAIRREV = `
    <div><img src="../assets/JORDANAIRREV.avif">
        <div class="name">Jordan Air Rev</div>
        <div class="name">$27</div>
    </div>
`;
SABRINA3 = `
    <div><img src="../assets/SABRINA3.avif">
        <div class="name">Sabrina 3</div>
        <div class="name">$30</div>
    </div>
`;

console.log(document.cookie);
for (let i = 0; i < document.cookie.split("; ").length; i++) {
    if (document.cookie.split("; ")[i].substring(0,4) == "cart") {
        cartcookie = document.cookie.split("; ")[i].slice(5);
    }
    if (document.cookie.split("; ")[i].substring(0,4) == "cpri") {
        pricecookie = document.cookie.split("; ")[i].slice(5);
    }
    if (document.cookie.split("; ")[i].substring(0,4) == "bala") {
        balance = document.cookie.split("; ")[i].slice(5);
    }
}
if (cartcookie) {
    document.getElementById("empty").remove()
}
for (let i = 0; i < pricecookie.split(",").length; i++) {
    total += Number(pricecookie.split(",")[i])
    console.log(total, pricecookie.split(",")[i])
    document.getElementById("subtotal").textContent = "Subtotal - $" + String(total.toFixed(2))
    document.getElementById("tax").textContent = "Tax - $" + String((total * 0.06625).toFixed(2))
    document.getElementById("total").textContent = "Total - $" + String((total * 0.06625 + total).toFixed(2))
    document.getElementById("balance").textContent = "Balance - $" + String(balance.toFixed(2))
}
for (let i = 0; i < cartcookie.split(",").length; i++) {
    if (cartcookie.split(",")[i] == 'AIRJORDAN1LOWSE') {
        aj1lse = document.createElement('div')
        aj1lse.innerHTML = AIRJORDAN1LOWSE
        cartlist.appendChild(aj1lse)
        console.log("hey just added a airjordan1lowse")
    }
    if (cartcookie.split(",")[i] == 'AIRJORDAN12RETRO') {
        aj12r = document.createElement('div')
        aj12r.innerHTML = AIRJORDAN12RETRO
        cartlist.appendChild(aj12r)
        console.log("hey just added a AIRJORDAN12RETRO")
    }
    if (cartcookie.split(",")[i] == 'AIRJORDAN4RETRO') {
        aj4r = document.createElement('div')
        aj4r.innerHTML = AIRJORDAN4RETRO
        cartlist.appendChild(aj4r)
        console.log("hey just added a AIRJORDAN4RETRO")
    }
    if (cartcookie.split(",")[i] == 'JORDANFLIGHTCOURT') {
        jfc = document.createElement('div')
        jfc.innerHTML = JORDANFLIGHTCOURT
        cartlist.appendChild(jfc)
        console.log("hey just added a JORDANFLIGHTCOURT")
    }
    if (cartcookie.split(",")[i] == 'AIRJORDAN3RETROMEX') {
        aj3rm = document.createElement('div')
        aj3rm.innerHTML = AIRJORDAN3RETROMEX
        cartlist.appendChild(aj3rm)
        console.log("hey just added a AIRJORDAN3RETROMEX")
    }
    if (cartcookie.split(",")[i] == 'JORDANZION4') {
        jz4 = document.createElement('div')
        jz4.innerHTML = JORDANZION4
        cartlist.appendChild(jz4)
        console.log("hey just added a JORDANZION4")
    }
    if (cartcookie.split(",")[i] == 'AIRJORDAN14G') {
        aj14g = document.createElement('div')
        aj14g.innerHTML = AIRJORDAN14G
        cartlist.appendChild(aj14g)
        console.log("hey just added a AIRJORDAN14G")
    }
    if (cartcookie.split(",")[i] == 'AIRJORDAN9RETROBOOTNRG') {
        aj9rbn = document.createElement('div')
        aj9rbn.innerHTML = AIRJORDAN9RETROBOOTNRG
        cartlist.appendChild(aj9rbn)
        console.log("hey just added a AIRJORDAN9RETROBOOTNRG")
    }
    if (cartcookie.split(",")[i] == 'JORDANAIRREV') {
        jar = document.createElement('div')
        jar.innerHTML = JORDANAIRREV
        cartlist.appendChild(jar)
        console.log("hey just added a JORDANAIRREV")
    }
    if (cartcookie.split(",")[i] == 'SABRINA3') {
        s3 = document.createElement('div')
        s3.innerHTML = SABRINA3
        cartlist.appendChild(s3)
        console.log("hey just added a SABRINA3")
    }
}
function clearcart() {
    document.cookie = "cart=" + ";path=/";
    document.cookie = "cpri=" + ";path=/";
    console.log(document.cookie);
    window.location.reload();
}
function checkout() {
    if (balance >= (total * 0.06625 + total)) {
        document.cookie = "cart=" + ";path=/";
        document.cookie = "cpri=" + ";path=/";
        balance -= (total * 0.06625 + total)
        window.location.reload();
    }
}
console.log(document.cookie);