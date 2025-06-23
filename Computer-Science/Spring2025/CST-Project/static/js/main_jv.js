// Function to open the popup
function openPopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'flex';

    // Fetch current balance (cash and lives) when popup is opened
    fetch('/get_balance', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Balance response:", data);
        if (data.cash !== undefined && data.lives !== undefined) {
            document.getElementById('cash-display').textContent = `Cash: $${data.cash}`;
            document.getElementById('lives-display').textContent = `Lives: ${data.lives}`;
        } else {
            alert("Error fetching balance. Please log in again.");
        }
    })
    .catch(error => {
        console.error("Error fetching balance:", error);
    });
}

// Function to close the popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

// Function to show the logout confirmation popup
function showLogoutPopup() {
    document.getElementById("logout-popup").style.display = "flex";
}

// Function to confirm logout
function confirmLogout(confirm) {
    document.getElementById("logout-popup").style.display = "none";
    if (confirm) {
        window.location.href = "/logout";
    }
}

// Function to purchase a life
function purchaseLife() {
    fetch('/purchase_life', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Purchase response:", data);
        if (data.message) {
            alert(data.message);
            openPopup(); // Refresh balance
        } else {
            alert(data.error || "Error purchasing life");
        }
    })
    .catch(error => {
        console.error("Error purchasing life:", error);
    });
}
