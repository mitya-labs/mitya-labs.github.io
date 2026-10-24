# mitya-labs.github.io

Сайт проекта [skladenOS](https://mitya-labs.github.io/) (организация mitya-labs): статические страницы для GitHub Pages, без сборки.

- `index.html` — русская версия, `en/index.html` — английская, `skladenos/index.html` и `en/skladenos/index.html` — отдельная страница skladenOS (ru/en), `404.html` — страница ошибки. Страницы генерирует `python3 tools/build.py`, HTML руками не правится.
- `apt/` — apt-репозиторий skladenOS (релиз garmon), его выкладывает `repo/publish.sh` из репозитория skladenos.
- `style.css` — единый стиль, светлая и тёмная тема по настройке системы.
- `assets/` — логотип, значок и шрифт JetBrains Mono (подмножество Latin + Cyrillic, лицензия SIL OFL 1.1, `assets/fonts/OFL.txt`).

Локальный просмотр: `python3 -m http.server 8000` и открыть http://127.0.0.1:8000/.

Логотип skladenOS © 2026 Dmitrii Trifonov, все права защищены. Остальное содержимое: лицензия пока не выбрана.
