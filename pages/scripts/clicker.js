let points = 0;

document.getElementById("bird").addEventListener("click", function() {
    points += 1; // Увеличиваем очки на 10 при каждом клике
    document.getElementById("points").innerText = points + " POINTS";
});
