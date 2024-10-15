const WebApp = window.Telegram.WebApp;

console.log(WebApp.initDataUnsafe);

document.getElementById("checktest").innerText = `${WebApp.initData}`;

