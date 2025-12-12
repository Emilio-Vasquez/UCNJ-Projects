async function makePrediction() {
    document.getElementById('resultArea').classList.add('d-none');
    document.getElementById('errorArea').classList.add('d-none');

    const data = {
        borough: document.getElementById('borough').value,
        zip_code: document.getElementById('zip_code').value,
        prop_type: document.getElementById('propertyType').value,
        gross_sqft: document.getElementById('gross_sqft').value,
        land_sqft: document.getElementById('land_sqft').value,
        year_built: document.getElementById('year_built').value
    }

    if(!data.borough || !data.zip_code || !data.prop_type || !data.gross_sqft || !data.land_sqft || !data.year_built){
        alert('Please enter all values')
        return;
    }

    try{
        const response = await fetch('/predictor', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if(response.ok){
            const formatter = new Intl.NumberFormat('en-US', {
                style: 'currency', currency: 'USD', maximumFractionDigits: 0
            })

            document.getElementById('priceDisplay').innerText = formatter.format(result.estimated_price);
            document.getElementById('rangeDisplay').innerText = 
                `${formatter.format(result.range_low)} - ${formatter.format(result.range_high)}`;
            document.getElementById('resultArea').classList.remove('d-none');
        }else{
            document.getElementById('errorArea').innerText = "Error: " + result.error;
            document.getElementById('errorArea').classList.remove('d-none');
        }
    }catch(error){
        console.error(error);
        document.getElementById('errorArea').innerText = "Server error";
        document.getElementById('errorArea').classList.remove('d-none');
    }
}