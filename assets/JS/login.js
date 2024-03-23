let loginBtn = document.getElementById("loginBtn");
let registerBtn = document.getElementById("registerBtn");
let nameField = document.getElementById("nameField");
let title = document.getElementById("title");

loginBtn.onclick = function(){
    nameField.style.maxHeight = "0";
    title.innerHTML = "Login"
    registerBtn.classList.add("disable");
    loginBtn.classList.remove("disable");
}
registerBtn.onclick = function(){
    nameField.style.maxHeight = "60px";
    title.innerHTML = "Register"
    loginBtn.classList.add("disable");
    registerBtn.classList.remove("disable");
}