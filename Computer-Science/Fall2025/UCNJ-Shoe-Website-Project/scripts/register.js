// document.cookie = "domain=" + window.location.hostname
// document.cookie = "path=/"

function register() {
    console.log("up straight playing with my register")
    console.log(document.getElementById('username').value)
    console.log(document.getElementById('email').value)
    console.log(document.getElementById('password').value)
    document.cookie = "user=" + document.getElementById('username').value + ";path=/"
    document.cookie = "pass=" + document.getElementById('password').value + ";path=/"
    document.cookie = "mail=" + document.getElementById('email').value + ";path=/"
    document.cookie = "bala=1000" + ";path=/"
    console.log(document.cookie) 
}