let WebApp = window.Telegram.WebApp;

const params = new URLSearchParams(window.Telegram.WebApp.initData);

const userData = Object.fromEntries(params);

if (userData.user) {
    userData.user = JSON.parse(userData.user);
    document.getElementById("user_id").value = userData.user.id;
}