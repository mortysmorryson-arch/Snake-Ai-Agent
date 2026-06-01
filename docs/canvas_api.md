# Canvas 2D Context API
## Методы отрисовки
- `ctx.fillRect(x, y, width, height)` — рисует залитый прямоугольник
- `ctx.clearRect(x, y, width, height)` — очищает область
- `ctx.beginPath()` — начинает новый путь
- `ctx.arc(x, y, radius, startAngle, endAngle, counterclockwise)` — дуга/круг
## Цикл анимации
Используй `requestAnimationFrame(callback)`. Callback получает timestamp в миллисекундах.
