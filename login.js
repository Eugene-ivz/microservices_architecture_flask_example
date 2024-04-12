"use strict";

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // let data = new FormData()
    // data.append("username", `${username}`);
    // data.append("password", `${password}`);
    await fetch('http://127.0.0.1:5000/auth/login',
    {method: 'post', headers: {
        'Authorization': 'Basic ' + btoa(`${username}:${password}`)},
     credentials: "include" },);
}
  
async function logout() {
    await fetch('/logout_with_cookies', {method: 'post'});
}
  
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
  
async function makeRequestWithJWT() {
    const options = {
        method: 'post',
        credentials: 'same-origin',
        headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        },
    };
    const response = await fetch('/protected', options);
    const result = await response.json();
    return result;
}