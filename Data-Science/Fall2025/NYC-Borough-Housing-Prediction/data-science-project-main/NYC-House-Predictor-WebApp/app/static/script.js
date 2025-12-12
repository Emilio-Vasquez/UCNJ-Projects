document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("submitBtn");
    const output = document.getElementById("card-text");
    const zipInput = document.getElementById("zip_code");

    button.addEventListener("click", async function () {
        const zipValue = zipInput.value;
        
        if (!zipValue) {
            output.innerText = "Please enter a ZIP code.";
            return;
        }

        try {
            console.log("hi")
            const response = await fetch("/lookup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ zip_code: zipValue })
            });

            if (!response.ok) {
                output.innerText = "Server error: " + response.status;
                return;
            }

            const data = await response.json();

            
       

        } catch (err) {
            console.error(err);
        }
    });
});
