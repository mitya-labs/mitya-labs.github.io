#!/usr/bin/env python3
# Генератор страниц сайта Mitya Labs: index.html (ru) и en/index.html (en) из одного набора блоков.
#   python3 tools/build.py
# Текст правится здесь, HTML руками не правится. Нужен только Python 3.
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mitya-labs.github.io/"
GH = "https://github.com/mitya-labs"
SK = GH + "/skladen"
TG = "https://t.me/dorimemmap"

MARK = ('<svg class="mark" viewBox="0 0 320 160" role="img" aria-label="{alt}">'
        '<polygon class="p1" points="0,30 80,0 80,130 0,160"/><polygon class="p2" points="80,0 160,30 160,160 80,130"/>'
        '<polygon class="p3" points="160,30 240,0 240,130 160,160"/><polygon class="p4" points="240,0 320,30 320,160 240,130"/></svg>')

PAGE = '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#E9EBEF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D0E15" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}assets/img/skladen2-photo.jpg">
<link rel="canonical" href="{site}{path}">
<link rel="alternate" hreflang="ru" href="{site}">
<link rel="alternate" hreflang="en" href="{site}en/">
<link rel="alternate" hreflang="x-default" href="{site}en/">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="preload" href="{up}assets/fonts/JetBrainsMono-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}style.css">
<script>
/* Язык по умолчанию: с корня (русская версия) уводим на /en/, если язык браузера не русский и пользователь не выбирал язык сам.
   Выбор переключателем RU/EN запоминается в localStorage. Страница /en/ при прямом заходе не перенаправляется. */
(function () {{
  if (!{isroot}) return;
  var want = null;
  try {{ want = localStorage.getItem("lang"); }} catch (e) {{}}
  if (want !== "ru" && want !== "en") {{
    var l = (navigator.languages && navigator.languages.length ? navigator.languages[0] : navigator.language) || "ru";
    want = /^ru(-|$)/i.test(l) ? "ru" : "en";
  }}
  if (want === "en") location.replace("en/" + location.search + location.hash);
}})();
</script>
</head>
<body>
<div class="wrap">
<header class="top">
  <a href="{home}" class="brand" aria-label="Mitya Labs"><img src="{up}assets/mitya-labs.svg" alt="Mitya Labs" width="209" height="99"></a>
  <nav aria-label="{navlabel}">
    <a href="#skladen">Skladen</a>
    <a href="#skladenos">skladenOS</a>
    <a href="{gh}">GitHub</a>
    <a href="{tg}">Telegram</a>
  </nav>
  <div class="lang" role="group" aria-label="{langlabel}"><a href="{ru_href}" hreflang="ru" lang="ru" data-lang="ru"{ru_cur}>RU</a><a href="{en_href}" hreflang="en" lang="en" data-lang="en"{en_cur}>EN</a></div>
</header>

<main>
<div class="hero">
  <div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <p class="status">{status}</p>
  </div>
  <figure class="shot">
    <img src="{up}assets/img/skladen2-photo.jpg" width="1100" height="729" alt="{photo_alt}">
    <figcaption>{photo_cap}</figcaption>
  </figure>
</div>

<section class="cols" id="skladen"><h2>Skladen</h2><div class="body">
{sk}
</div></section>

<section class="cols" id="skladenos"><h2>skladenOS</h2><div class="body">
{os}
</div></section>

<section class="cols"><h2>{s5h}</h2><div class="body fine">{s5}</div></section>

<section class="cols"><h2>{s6h}</h2><div class="body">{s6}</div></section>
</main>

<footer>
  <p>{foot}</p>
</footer>
</div>
<script>
document.querySelectorAll("a[data-lang]").forEach(function (a) {{
  a.addEventListener("click", function () {{ try {{ localStorage.setItem("lang", a.getAttribute("data-lang")); }} catch (e) {{}} }});
}});
</script>
</body>
</html>
'''


def dl(rows, cls="feat"):
    return '<dl class="%s">%s</dl>' % (cls, "".join("<dt>%s</dt><dd>%s</dd>" % r for r in rows))


def steps(rows):
    return '<ol class="steps">%s</ol>' % "".join("<li><b>%s</b>%s</li>" % r for r in rows)


def road(items, done):
    return '<ul class="road">%s</ul>' % "".join('<li%s>%s</li>' % (' class="done"' if i < done else "", t) for i, t in enumerate(items))


def table(head, rows):
    th = "".join("<th scope=\"col\">%s</th>" % h for h in head)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="table-wrap"><table class="ver"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)


def figure(img, w, h, alt, cap):
    return '<figure class="render"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (img, w, h, alt, cap)


RU = dict(
    lang="ru", path="", up="", home="./", isroot="true", ru_href="./", en_href="en/", ru_cur=' aria-current="true"', en_cur="", langlabel="Язык", navlabel="Разделы и язык",
    title="Mitya Labs: Skladen и skladenOS",
    desc="Mitya Labs делает Skladen, напечатанный палмтоп, который превращает Xiaomi Pocophone F1 в карманный терминал, и skladenOS, систему для него.",
    h1="Палмтоп из телефона и клавиатуры",
    lede="Mitya Labs делает Skladen: напечатанный на 3D-принтере палмтоп, который превращает Xiaomi Pocophone F1 в карманный терминал в форме ноутбука, и skladenOS, систему для него.",
    status="<strong>Skladen 2.1 напечатан и собран.</strong> skladenOS в разработке: готовых образов пока нет.",
    photo_alt="Напечатанный Skladen 2.1 на столе, открытый: Pocophone F1 под рамкой на защёлках в прозрачной крышке, клавиатура Jomaa в основании",
    photo_cap="Skladen 2.1.0: Pocophone F1 в прозрачной крышке из PETG, клавиатура Jomaa в основании. На экране рабочая сборка, из которой вырастает skladenOS.",
    s5h="Основа и права", s6h="Где следить",
    foot="© 2026 Mitya Labs. Страница обновляется по мере продвижения проектов.",
)
RU["sk"] = "\n".join([
    "<p>Skladen — палмтоп, который превращает Xiaomi Pocophone F1 в карманный терминал в форме ноутбука. Название — <i>складень</i>: дорожная икона на петлях, две створки, которые смыкаются над тем, что в них лежит.</p>",
    "<p>Крышка держит телефон под рамкой на защёлках, в основании клавиатура Jomaa KEYBOARD098RU из чехла-книжки. Всё напечатано, петли держатся на двух болтах M3. Конструкция описана кодом (build123d): размеры и проверки считаются при сборке модели.</p>",
    dl([("Телефон", "Xiaomi Pocophone F1, 155,5 × 75,3 × 9,25 мм, 182 г"),
        ("Клавиатура", "Jomaa KEYBOARD098RU"),
        ("В сложенном виде", "24,29 мм у петли, 20,31 мм спереди"),
        ("Масса", "около 403 г по модели")], "feat"),
    "<h3>Версии</h3>",
    table(("Версия", "Что это", "Дата"), [
        ('<a href="%s/tree/v2.1.0">2.1.0</a>' % SK, "Skladen 2 с рамкой на защёлках; напечатан", "2026-10-20"),
        ('<a href="%s/tree/v2.0.0">2.0.0</a>' % SK, "Skladen 2 под Pocophone F1, телефон на ленте; напечатан", "2026-10-06"),
        ('<a href="%s/tree/v1.0.0">1.0.0</a>' % SK, "Skladen 1 под Pixel 3a XL; напечатан", "2026-10-02")]),
    '<p class="note">Размеры и масса взяты из модели, замеры напечатанных экземпляров ещё не сведены. Последние правки рамки смоделированы и проверены, на печати не подтверждены.</p>',
    figure("assets/img/skladen2-open.webp", 1000, 726, "Skladen 2, открытый на 112 градусов: в крышке телефон с терминалом, в основании клавиатура", "Открытый на 112°. Рендер из модели; телефон и клавиатура заменены заготовками по измеренным габаритам."),
    figure("assets/img/skladen2-closed.webp", 1000, 318, "Skladen 2 в сложенном виде, вид спереди справа", "Сложенный: 24,29 мм у петли."),
    '<p class="note">Конструкция открыта под CERN-OHL-S-2.0. Исходники, документы и список изменений: <a href="%s">репозиторий Skladen</a>.</p>' % SK,
])
RU["os"] = "\n".join([
    MARK.format(alt="Знак skladenOS: четыре сложенные грани"),
    "<p>skladenOS — система для Skladen и других складных устройств, где экран и клавиатура соединены шарниром. Это Mobian (Debian) с оконным менеджером SXMO: лёгкий интерфейс, которым управляют жестами, кнопками громкости и внешней клавиатурой. Система учитывает вырез экрана и скруглённые углы: окна и панели не заходят под челку, даже в полноэкранном режиме.</p>",
    '<p class="status">Готовых образов для скачивания пока нет: сборка из исходников и проверка на устройстве ещё идут.</p>',
    "<h3>Что уже работает</h3>",
    dl([("Вырез и углы", "Панель и окна отступают от выреза и перестраиваются при повороте экрана."),
        ("Кнопки и жесты", "Питание, громкость, жесты по краям экрана; с внешней клавиатуры работает <kbd>Super</kbd>+<kbd>Esc</kbd>."),
        ("USB", "Роль хоста или устройства выбирается сама: хаб, флешка и клавиатура работают, с компьютером поднимается USB-сеть."),
        ("Питание", "Режимы «Баланс», «Экономия», «Ночь» и «Производительность» из меню, режим «экран не гаснет»."),
        ("Раскладки", "Английская и русская по CapsLock, экранная клавиатура с кириллицей."),
        ("Звук и датчики", "Оба динамика, датчики через SLPI на ядре 7.x.")]),
    '<p class="note">Проверено на рабочей сборке с Pocophone F1 и ядром 7.2. Новая сборка из исходников ещё проходит проверку на устройстве.</p>',
    "<h3>Как собирается</h3>",
    steps([("Ядро", "Ядро Mobian для SDM845 из исходников и наши патчи: Type-C и зарядка PD."),
           ("Пакеты", "Настройки устройства и SXMO оформлены как deb-пакеты."),
           ("Образ", "Рецепты Mobian (debos) собирают образ из ядра и пакетов."),
           ("Прошивка", "Образ прошивается на телефон через fastboot.")]),
    "<p>Версии ядра и рецептов зафиксированы, сборку планируется вести в CI на GitHub: образ можно будет воспроизвести из исходников.</p>",
    "<h3>Что дальше</h3>",
    road(["Имя, организация и чистый репозиторий", "Каркас сборки ядра с патчами, пакеты настроек, логотип", "Полная сборка ядра и образа в CI", "Обновления по воздуху (OTA) через собственный репозиторий пакетов", "Проверка с обоими вариантами панели Poco F1 (ebbg и tianma)", "Иконки статус-бара, лицензия и описание репозитория", "Публичный репозиторий и первый образ"], 2),
])
RU["s5"] = "".join([
    "<p><strong>Skladen:</strong> конструкция открыта под CERN-OHL-S-2.0, исходником считается Python-модель.</p>",
    "<p><strong>skladenOS</strong> основан на <a href=\"https://mobian.org\">Mobian</a> и <a href=\"https://www.debian.org\">Debian</a>, но не является их официальным выпуском и не связан с этими проектами. Оконный менеджер <a href=\"https://sxmo.org\">SXMO</a> распространяется под AGPL-3.0. Прошивки Qualcomm и Xiaomi мы не распространяем: система извлекает их на самом телефоне. Лицензия кода skladenOS будет объявлена при открытии репозитория.</p>",
    "<p><strong>Логотипы Mitya Labs и skladenOS © 2026 Dmitrii Trifonov, все права защищены.</strong> Названия и логотипы остаются отличительными знаками проектов.</p>",
])
RU["s6"] = "<p>Проекты ведёт организация <a href=\"%s\">mitya-labs</a> на GitHub. Репозиторий <a href=\"%s\">Skladen</a> открыт. Репозиторий skladenOS откроется, когда будут готовы лицензия и описание; до тех пор можно подписаться на организацию. Новости и заметки по ходу работы — в <a href=\"%s\">Telegram-канале</a>.</p>" % (GH, SK, TG)

EN = dict(
    lang="en", path="en/", up="../", home="./", isroot="false", ru_href="../", en_href="./", ru_cur="", en_cur=' aria-current="true"', langlabel="Language", navlabel="Sections and language",
    title="Mitya Labs: Skladen and skladenOS",
    desc="Mitya Labs builds Skladen, a printed palmtop that turns a Xiaomi Pocophone F1 into a pocketable terminal, and skladenOS, an operating system for it.",
    h1="A palmtop made of a phone and a keyboard",
    lede="Mitya Labs builds Skladen, a 3D-printed palmtop that turns a Xiaomi Pocophone F1 into a pocketable laptop-shaped terminal, and skladenOS, the system for it.",
    status="<strong>Skladen 2.1 is printed and assembled.</strong> skladenOS is in development: there are no images yet.",
    photo_alt="The printed Skladen 2.1 on a desk, open: a Pocophone F1 under the clip-on bezel in a transparent lid, the Jomaa keyboard in the base",
    photo_cap="Skladen 2.1.0: a Pocophone F1 in a transparent PETG lid, the Jomaa keyboard in the base. The screen runs the working build skladenOS grows out of.",
    s5h="Basis and rights", s6h="Follow along",
    foot="© 2026 Mitya Labs. This page is updated as the projects move along.",
)
EN["sk"] = "\n".join([
    "<p>Skladen is a palmtop that turns a Xiaomi Pocophone F1 into a pocketable laptop-shaped terminal. The name is <i>skladen</i> (складень), a hinged Russian travel icon: two panels that fold shut over what they carry.</p>",
    "<p>The lid holds the phone under a clip-on bezel, the base carries a Jomaa KEYBOARD098RU salvaged from a folio case. Everything is printed, and the hinge sits on two M3 bolts. The design is written as code (build123d): dimensions and checks are computed when the model is built.</p>",
    dl([("Phone", "Xiaomi Pocophone F1, 155.5 × 75.3 × 9.25 mm, 182 g"),
        ("Keyboard", "Jomaa KEYBOARD098RU"),
        ("Closed", "24.29 mm at the hinge, 20.31 mm at the front"),
        ("Mass", "about 403 g by the model")], "feat"),
    "<h3>Versions</h3>",
    table(("Version", "What", "Date"), [
        ('<a href="%s/tree/v2.1.0">2.1.0</a>' % SK, "Skladen 2 with the clip-on bezel; printed", "2026-10-20"),
        ('<a href="%s/tree/v2.0.0">2.0.0</a>' % SK, "Skladen 2 for the Pocophone F1, phone held by tape; printed", "2026-10-06"),
        ('<a href="%s/tree/v1.0.0">1.0.0</a>' % SK, "Skladen 1 for the Pixel 3a XL; printed", "2026-10-02")]),
    '<p class="note">Dimensions and mass come from the model; measurements of the printed units are not collected yet. The latest bezel revisions are modelled and checked but not confirmed on a print.</p>',
    figure("../assets/img/skladen2-open.webp", 1000, 726, "Skladen 2 rendered open at 112 degrees: the phone in the lid showing a terminal, the keyboard in the base", "Open at 112°. A render from the model; the phone and keyboard are stand-ins built from their measured envelopes."),
    figure("../assets/img/skladen2-closed.webp", 1000, 318, "Skladen 2 rendered closed, seen from the front right", "Closed: 24.29 mm at the hinge."),
    '<p class="note">The design is open under CERN-OHL-S-2.0. Sources, docs and the changelog: the <a href="%s">Skladen repository</a>.</p>' % SK,
])
EN["os"] = "\n".join([
    MARK.format(alt="skladenOS mark: four folded panels"),
    "<p>skladenOS is the system for Skladen and other folding devices where the screen and the keyboard are joined by a hinge. It is Mobian (Debian) with the SXMO window manager: a light interface driven by gestures, volume keys and an external keyboard. It respects the display notch and rounded corners: windows and bars never go under the cutout, even in fullscreen.</p>",
    '<p class="status">There are no images to download yet: building from source and testing on the device are still under way.</p>',
    "<h3>What works today</h3>",
    dl([("Notch and corners", "The bar and windows keep clear of the cutout and adjust when the screen rotates."),
        ("Buttons and gestures", "Power, volume, edge gestures; <kbd>Super</kbd>+<kbd>Esc</kbd> works from an external keyboard."),
        ("USB", "Host or device role is picked automatically: a hub, a flash drive and a keyboard work; USB networking comes up with a computer."),
        ("Power", "“Balanced”, “Eco”, “Night” and “Performance” profiles from the menu, plus a “keep screen awake” mode."),
        ("Layouts", "English and Russian switched with CapsLock, on-screen keyboard with Cyrillic."),
        ("Audio and sensors", "Both speakers, sensors through the SLPI on kernel 7.x.")]),
    '<p class="note">Verified on a working build with a Pocophone F1 and kernel 7.2. The new from-source build is still being tested on the device.</p>',
    "<h3>How it is built</h3>",
    steps([("Kernel", "The Mobian SDM845 kernel from source plus our patches: Type-C and PD charging."),
           ("Packages", "Device and SXMO settings are shipped as deb packages."),
           ("Image", "Mobian recipes (debos) assemble an image from the kernel and the packages."),
           ("Flashing", "The image is flashed to the phone with fastboot.")]),
    "<p>Kernel and recipe versions are pinned, and the build is planned to run in CI on GitHub, so the image can be reproduced from source.</p>",
    "<h3>What is next</h3>",
    road(["Name, organization and a clean repository", "Kernel build scaffolding with patches, settings packages, logo", "Full kernel and image build in CI", "Over-the-air (OTA) updates through our own package repository", "Testing with both Poco F1 panel variants (ebbg and tianma)", "Status bar icons, license and repository description", "Public repository and the first image"], 2),
])
EN["s5"] = "".join([
    "<p><strong>Skladen:</strong> the design is open under CERN-OHL-S-2.0; the Python model counts as the source.</p>",
    "<p><strong>skladenOS</strong> is based on <a href=\"https://mobian.org\">Mobian</a> and <a href=\"https://www.debian.org\">Debian</a>, but it is not an official release of either and is not affiliated with those projects. The <a href=\"https://sxmo.org\">SXMO</a> window manager is distributed under the AGPL-3.0. We do not distribute Qualcomm or Xiaomi firmware: the system extracts it on the phone itself. The license of the skladenOS code will be announced when the repository opens.</p>",
    "<p><strong>The Mitya Labs and skladenOS logos are © 2026 Dmitrii Trifonov, all rights reserved.</strong> The names and the logos remain distinctive marks of the projects.</p>",
])
EN["s6"] = "<p>The projects are run by the <a href=\"%s\">mitya-labs</a> organization on GitHub. The <a href=\"%s\">Skladen</a> repository is open. The skladenOS repository will open once the license and the description are ready; until then, follow the organization. News and notes along the way are in the <a href=\"%s\">Telegram channel</a>.</p>" % (GH, SK, TG)


def build():
    for d, out in ((RU, "index.html"), (EN, "en/index.html")):
        html = PAGE.format(site=SITE, gh=GH, tg=TG, **d)
        os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
        open(os.path.join(ROOT, out), "w", encoding="utf-8").write(html)
        print("ok", out, len(html))


if __name__ == "__main__":
    build()
