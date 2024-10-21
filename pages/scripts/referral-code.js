
const params = new URLSearchParams(window.Telegram.WebApp.initData);

const userData = Object.fromEntries(params);

if (userData.user) {
    userData.user = JSON.parse(userData.user);
    const refcode = `https://t.me/ClothesShopX_bot?start=${userData.user.id}`;
    document.getElementById("referralCode").innerText = refcode;
}