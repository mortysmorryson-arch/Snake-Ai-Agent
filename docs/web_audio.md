# Web Audio API
## Инициализация
`const audioCtx = new (window.AudioContext || window.webkitAudioContext)();`
Требует жеста пользователя для `audioCtx.resume()`.
## Генерация звука
- `audioCtx.createOscillator()` → `osc.type = 'sine' | 'square' | 'triangle'`
- `audioCtx.createGain()` → управление громкостью
- Подключение: `osc.connect(gain); gain.connect(audioCtx.destination);`
- Запуск: `osc.start(); osc.stop(audioCtx.currentTime + duration);`
