#!/usr/bin/env python3
# Генератор страниц сайта Mitya Labs: index.html (ru) и en/index.html (en) из одного набора блоков.
#   python3 tools/build.py
# Текст правится здесь, HTML руками не правится. Нужен только Python 3.
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mitya-labs.github.io/"
GH = "https://github.com/mitya-labs"
SK = GH + "/skladen"
SO = GH + "/skladenos"
APT = SITE + "apt/"
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
    <a href="#configurator">{cfg_h}</a>
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
    <img src="{up}assets/img/skladen2-photo.jpg" width="1100" height="825" alt="{photo_alt}">
    <figcaption>{photo_cap}</figcaption>
  </figure>
</div>

<section class="cols" id="skladen"><h2>Skladen</h2><div class="body">
{sk}
</div></section>

<section class="cols" id="configurator"><h2>{cfg_h}</h2><div class="body">{cfg}</div></section>

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


def configurator(text, title, cta, lang):
    url = "https://mitya-labs.github.io/skladen/"
    return ('<p>%s</p><iframe class="cfg" src="%s?embed=1&amp;lang=%s" title="%s" loading="lazy"></iframe>'
            '<p><a class="cta" href="%s?lang=%s">%s</a></p>' % (text, url, lang, title, url, lang, cta))


RU = dict(
    lang="ru", path="", up="", home="./", isroot="true", ru_href="./", en_href="en/", ru_cur=' aria-current="true"', en_cur="", langlabel="Язык", navlabel="Разделы и язык",
    title="Mitya Labs: Skladen и skladenOS",
    desc="Mitya Labs делает Skladen, напечатанный палмтоп, который превращает Xiaomi Pocophone F1 в карманный терминал, и skladenOS, систему для него.",
    h1="Палмтоп из телефона и клавиатуры",
    lede="Mitya Labs делает Skladen: напечатанный на 3D-принтере палмтоп, который превращает Xiaomi Pocophone F1 в карманный терминал в форме ноутбука, и skladenOS, систему для него.",
    status="<strong>Skladen 2.1.1 напечатан и собран.</strong> skladenOS: исходники и репозиторий пакетов открыты, готовый образ для Poco F1 скачивается из релиза v0.1.0 на GitHub.",
    photo_alt="Напечатанный Skladen 2.1.1 на столе, открытый: Pocophone F1 под рамкой на защёлках в прозрачной крышке, клавиатура Jomaa в прозрачном основании, бирюзовые рамка и логотип",
    photo_cap="Skladen 2.1.1: Pocophone F1 в прозрачной крышке из PETG с бирюзовой рамкой и логотипом, клавиатура Jomaa в прозрачном основании. На экране рабочая сборка, из которой вырастает skladenOS.",
    cfg_h="Конфигуратор", cfg=configurator("Выберите детали Skladen 2 (крышку, рамку, базу) и скачайте файл для печати: STL или 3MF.", "Skladen 2 в сборке, можно вращать и раскрывать", "Открыть конфигуратор →", "ru"),
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
        ('<a href="%s/tree/v2.1.1">2.1.1</a>' % SK, "Рёбра обжима и язычки кнопок в крышке с рамкой; напечатан", "2026-10-24"),
        ('<a href="%s/tree/v2.1.0">2.1.0</a>' % SK, "Skladen 2 с рамкой на защёлках; напечатан", "2026-10-20"),
        ('<a href="%s/tree/v2.0.0">2.0.0</a>' % SK, "Skladen 2 под Pocophone F1, телефон на ленте; напечатан", "2026-10-06"),
        ('<a href="%s/tree/v1.0.0">1.0.0</a>' % SK, "Skladen 1 под Pixel 3a XL; напечатан", "2026-10-02")]),
    '<p class="note">Размеры и масса взяты из модели, замеры напечатанных экземпляров ещё не сведены. Рёбра обжима и язычки кнопок в 2.1.1 подтверждены печатью; остальные правки рамки (отверстия для выталкивания, динамик и микрофон, закрытие челки, основание с окном под переключатель) смоделированы и проверены, на печати пока не подтверждены.</p>',
    figure("assets/img/skladen2-open.webp", 1000, 726, "Skladen 2, открытый на 112 градусов: в крышке телефон с терминалом, в основании клавиатура", "Открытый на 112°. Рендер из модели; телефон и клавиатура заменены заготовками по измеренным габаритам."),
    figure("assets/img/skladen2-closed.webp", 1000, 318, "Skladen 2 в сложенном виде, вид спереди справа", "Сложенный: 24,29 мм у петли."),
    '<p class="note">Конструкция открыта под CERN-OHL-S-2.0. Исходники, документы и список изменений: <a href="%s">репозиторий Skladen</a>.</p>' % SK,
])
RU["os"] = "\n".join([
    MARK.format(alt="Знак skladenOS: четыре сложенные грани"),
    "<p>skladenOS — система для Skladen и других складных устройств, где экран и клавиатура соединены шарниром. Это Mobian (Debian) с оконным менеджером SXMO: лёгкий интерфейс, которым управляют жестами, кнопками громкости и внешней клавиатурой. Система учитывает вырез экрана и скруглённые углы: окна и панели не заходят под челку, даже в полноэкранном режиме.</p>",
    '<p class="status">Исходники и репозиторий пакетов открыты. Готовый образ для Poco F1 (панель EBBG) — в <a href="https://github.com/mitya-labs/skladenos/releases/tag/v0.1.0">релизе v0.1.0</a>; можно и собрать из исходников одной командой (Docker).</p>',
    '<p><a class="btn" href="skladenos/">Страница skladenOS: что работает, как собрать, пакеты и эмуляторы →</a></p>',
])
RU["s5"] = "".join([
    "<p><strong>Skladen:</strong> конструкция открыта под CERN-OHL-S-2.0, исходником считается Python-модель.</p>",
    "<p><strong>skladenOS</strong> основан на <a href=\"https://mobian.org\">Mobian</a> и <a href=\"https://www.debian.org\">Debian</a>, но не является их официальным выпуском и не связан с этими проектами. Код skladenOS открыт под GPL-3.0-or-later, патчи ядра — GPL-2.0-only, свободные обои — CC BY-SA 4.0. Оконный менеджер <a href=\"https://sxmo.org\">SXMO</a> распространяется под AGPL-3.0. Прошивки Qualcomm и Xiaomi мы не распространяем: система извлекает их на самом телефоне.</p>",
    "<p><strong>Логотипы Mitya Labs и skladenOS © 2026 Dmitrii Trifonov, все права защищены.</strong> Названия и логотипы остаются отличительными знаками проектов; правила — в <a href=\"%s/blob/main/TRADEMARK.md\">TRADEMARK.md</a>.</p>" % SO,
])
RU["s6"] = "<p>Проекты ведёт организация <a href=\"%s\">mitya-labs</a> на GitHub. Репозитории <a href=\"%s\">Skladen</a> и <a href=\"%s\">skladenOS</a> открыты. Новости и заметки по ходу работы — в <a href=\"%s\">Telegram-канале</a>.</p>" % (GH, SK, SO, TG)

EN = dict(
    lang="en", path="en/", up="../", home="./", isroot="false", ru_href="../", en_href="./", ru_cur="", en_cur=' aria-current="true"', langlabel="Language", navlabel="Sections and language",
    title="Mitya Labs: Skladen and skladenOS",
    desc="Mitya Labs builds Skladen, a printed palmtop that turns a Xiaomi Pocophone F1 into a pocketable terminal, and skladenOS, an operating system for it.",
    h1="A palmtop made of a phone and a keyboard",
    lede="Mitya Labs builds Skladen, a 3D-printed palmtop that turns a Xiaomi Pocophone F1 into a pocketable laptop-shaped terminal, and skladenOS, the system for it.",
    status="<strong>Skladen 2.1.1 is printed and assembled.</strong> skladenOS: the source and the package repository are open; a ready-made image for the Poco F1 is in the v0.1.0 release on GitHub.",
    photo_alt="The printed Skladen 2.1.1 on a desk, open: a Pocophone F1 under the clip-on bezel in a clear lid with a teal bezel and logo, the Jomaa keyboard in a clear base",
    photo_cap="Skladen 2.1.1: a Pocophone F1 in a clear PETG lid with a teal bezel and logo, the Jomaa keyboard in a clear base. The screen runs the working build skladenOS grows out of.",
    cfg_h="Configurator", cfg=configurator("Pick the Skladen 2 parts (lid, frame, base) and download a print file: STL or 3MF.", "Skladen 2 assembled: rotate it, open and close the lid", "Open the configurator →", "en"),
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
        ('<a href="%s/tree/v2.1.1">2.1.1</a>' % SK, "Crush ribs and button tongues in the bezel lid; printed", "2026-10-24"),
        ('<a href="%s/tree/v2.1.0">2.1.0</a>' % SK, "Skladen 2 with the clip-on bezel; printed", "2026-10-20"),
        ('<a href="%s/tree/v2.0.0">2.0.0</a>' % SK, "Skladen 2 for the Pocophone F1, phone held by tape; printed", "2026-10-06"),
        ('<a href="%s/tree/v1.0.0">1.0.0</a>' % SK, "Skladen 1 for the Pixel 3a XL; printed", "2026-10-02")]),
    '<p class="note">Dimensions and mass come from the model; measurements of the printed units are not collected yet. The crush ribs and button tongues of 2.1.1 are confirmed on a print; the other bezel revisions (eject holes, speaker and microphone openings, the notch cover, the switch-window base) are modelled and checked but not yet confirmed.</p>',
    figure("../assets/img/skladen2-open.webp", 1000, 726, "Skladen 2 rendered open at 112 degrees: the phone in the lid showing a terminal, the keyboard in the base", "Open at 112°. A render from the model; the phone and keyboard are stand-ins built from their measured envelopes."),
    figure("../assets/img/skladen2-closed.webp", 1000, 318, "Skladen 2 rendered closed, seen from the front right", "Closed: 24.29 mm at the hinge."),
    '<p class="note">The design is open under CERN-OHL-S-2.0. Sources, docs and the changelog: the <a href="%s">Skladen repository</a>.</p>' % SK,
])
EN["os"] = "\n".join([
    MARK.format(alt="skladenOS mark: four folded panels"),
    "<p>skladenOS is the system for Skladen and other folding devices where the screen and the keyboard are joined by a hinge. It is Mobian (Debian) with the SXMO window manager: a light interface driven by gestures, volume keys and an external keyboard. It respects the display notch and rounded corners: windows and bars never go under the cutout, even in fullscreen.</p>",
    '<p class="status">The source and the package repository are open. A ready-made image for the Poco F1 (EBBG panel) is in the <a href="https://github.com/mitya-labs/skladenos/releases/tag/v0.1.0">v0.1.0 release</a>; you can also build it from source with one command (Docker).</p>',
    '<p><a class="btn" href="skladenos/">The skladenOS page: what works, how to build, packages and emulators →</a></p>',
])
EN["s5"] = "".join([
    "<p><strong>Skladen:</strong> the design is open under CERN-OHL-S-2.0; the Python model counts as the source.</p>",
    "<p><strong>skladenOS</strong> is based on <a href=\"https://mobian.org\">Mobian</a> and <a href=\"https://www.debian.org\">Debian</a>, but it is not an official release of either and is not affiliated with those projects. The skladenOS code is open under GPL-3.0-or-later, the kernel patches under GPL-2.0-only, the free wallpapers under CC BY-SA 4.0. The <a href=\"https://sxmo.org\">SXMO</a> window manager is distributed under the AGPL-3.0. We do not distribute Qualcomm or Xiaomi firmware: the system extracts it on the phone itself.</p>",
    "<p><strong>The Mitya Labs and skladenOS logos are © 2026 Dmitrii Trifonov, all rights reserved.</strong> The names and the logos remain distinctive marks of the projects; the rules are in <a href=\"%s/blob/main/TRADEMARK.md\">TRADEMARK.md</a>.</p>" % SO,
])
EN["s6"] = "<p>The projects are run by the <a href=\"%s\">mitya-labs</a> organization on GitHub. The <a href=\"%s\">Skladen</a> and <a href=\"%s\">skladenOS</a> repositories are open. News and notes along the way are in the <a href=\"%s\">Telegram channel</a>.</p>" % (GH, SK, SO, TG)


OS_PAGE = """<!doctype html>
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
<link rel="alternate" hreflang="ru" href="{site}skladenos/">
<link rel="alternate" hreflang="en" href="{site}en/skladenos/">
<link rel="alternate" hreflang="x-default" href="{site}en/skladenos/">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="preload" href="{up}assets/fonts/JetBrainsMono-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<div class="wrap">
<header class="top">
  <a href="{home}" class="brand" aria-label="Mitya Labs"><img src="{up}assets/mitya-labs.svg" alt="Mitya Labs" width="209" height="99"></a>
  <nav aria-label="{navlabel}">
    <a href="{home}#skladen">Skladen</a>
    <a href="{home}#configurator">{cfg_h}</a>
    <a href="./" aria-current="page">skladenOS</a>
    <a href="{gh}">GitHub</a>
    <a href="{tg}">Telegram</a>
  </nav>
  <div class="lang" role="group" aria-label="{langlabel}"><a href="{ru_href}" hreflang="ru" lang="ru" data-lang="ru"{ru_cur}>RU</a><a href="{en_href}" hreflang="en" lang="en" data-lang="en"{en_cur}>EN</a></div>
</header>

<main>
<div class="hero" style="grid-template-columns:1fr">
  <div>
    {mark}
    <h1>skladenOS</h1>
    <p class="lede">{lede}</p>
    <p class="status">{status}</p>
  </div>
</div>
{sections}
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
"""


def sec(title, body, cls="body", sid=""):
    return '<section class="cols"%s><h2>%s</h2><div class="%s">%s</div></section>' % (' id="%s"' % sid if sid else "", title, cls, body)


APT_CMD = ('<pre><code>curl -fsS %sskladenos-archive-keyring.gpg | sudo tee /usr/share/keyrings/skladenos-archive-keyring.gpg &gt;/dev/null\n'
           'sudo tee /etc/apt/sources.list.d/skladenos.sources &gt;/dev/null &lt;&lt;\'EOF\'\n'
           'Types: deb\nURIs: %s\nSuites: garmon\nComponents: main non-free\n'
           'Signed-By: /usr/share/keyrings/skladenos-archive-keyring.gpg\nEOF\nsudo apt update</code></pre>') % (APT, APT)
BUILD_CMD = ('<pre><code>git clone %s.git &amp;&amp; cd skladenos\n'
             'packages/build.sh skladenos-config        # и так для каждого пакета skladenos-*\n'
             'build/image/build.sh build                # образ в out/image/&lt;метка&gt;/ , около 5 минут\n'
             'scripts/snapshot-flash out/image/&lt;метка&gt;   # стирает весь телефон!</code></pre>') % SO
BUILD_CMD_EN = BUILD_CMD.replace("# и так для каждого пакета skladenos-*", "# repeat for each skladenos-* package").replace("# образ в out/image/&lt;метка&gt;/ , около 5 минут", "# image in out/image/&lt;label&gt;/, about 5 minutes").replace("out/image/&lt;метка&gt;   # стирает весь телефон!", "out/image/&lt;label&gt;   # erases the whole phone!")

RU_OS_PAGE = dict(
    lang="ru", path="skladenos/", up="../", home="../", ru_href="./", en_href="../en/skladenos/", ru_cur=' aria-current="true"', en_cur="",
    langlabel="Язык", navlabel="Разделы и язык", cfg_h=RU["cfg_h"], foot=RU["foot"],
    title="skladenOS: система для Skladen и Poco F1 — Mitya Labs",
    desc="skladenOS: Mobian и SXMO для Xiaomi Poco F1 — что работает, как собрать образ, пакеты, эмуляторы и apt-репозиторий.",
    mark=MARK.format(alt="Знак skladenOS: четыре сложенные грани"),
    lede="Система для Skladen и других складных устройств: Mobian (Debian) с оконным менеджером SXMO, ядро 7.2 с нашими патчами зарядки и USB-PD, мастер первой загрузки и набор пакетов.",
    status="<strong>Исходники и репозиторий пакетов открыты.</strong> Готовый образ для Poco F1 (панель EBBG) — в релизе v0.1.0 на GitHub; можно собрать и из исходников одной командой.",
)
RU_OS_PAGE["sections"] = "\n".join([
    sec("Что это", "<p>skladenOS — система для Xiaomi Poco F1 (SDM845), в первую очередь в составе палмтопа <a href=\"../#skladen\">Skladen</a>, где экран и клавиатура соединены шарниром. Основа — <a href=\"https://mobian.org\">Mobian</a> (Debian forky) с лёгким интерфейсом <a href=\"https://sxmo.org\">SXMO</a> (sway): жесты, кнопки громкости, внешняя клавиатура. Окна и панели не заходят под вырез и скруглённые углы экрана, даже в полноэкранном режиме.</p>"),
    sec("Что работает", dl([
        ("Вырез и углы", "Панель и окна отступают от выреза и перестраиваются при повороте экрана."),
        ("Кнопки и жесты", "Питание, громкость, жесты по краям экрана; с внешней клавиатуры работает <kbd>Super</kbd>+<kbd>Esc</kbd>."),
        ("Первая загрузка", "Мастер на 12 языках (английский по умолчанию): Bluetooth-клавиатура, Wi-Fi, имя пользователя и обязательная смена пароля."),
        ("USB и зарядка", "Роль хоста или устройства выбирается сама; хаб, флешка и клавиатура работают; зарядка по USB-PD."),
        ("Питание", "Режимы «Баланс», «Экономия», «Ночь» и «Производительность» из меню, режим «экран не гаснет»."),
        ("Раскладки", "Английская и русская по CapsLock, экранная клавиатура с кириллицей."),
        ("Звук, датчики, сеть", "Оба динамика, микрофон, датчики через SLPI на ядре 7.x, Wi-Fi и Bluetooth."),
        ("Защита тача", "Сторож перезапускает драйвер тачскрина, если касание «зависло»."),
        ("fastfetch", "Показывает логотип skladenOS и название системы.")]) +
        '<p class="note">Проверено на Pocophone F1 (панель EBBG) с ядром 7.2: образ, собранный из исходников, прошит и работает. Вариант панели Tianma собирается, но на железе не проверен. SIM не проверялась.</p>'),
    sec("Первая загрузка", "<p>Сразу после прошивки вход: пользователь <code>skladen</code>, пароль <code>1234</code>. На экране запускается мастер: выбор языка, поиск Bluetooth-клавиатуры, Wi-Fi, затем имя пользователя и новый пароль. Пока пароль по умолчанию не сменён, вход по SSH разрешён только из локальных сетей. Имя пользователя применяется после перезагрузки.</p>"),
    sec("Как собрать и прошить", "<p>Нужны Mac или Linux, Docker, <code>fastboot</code> и разблокированный загрузчик. Образ собирается в Docker из официального rootfs Mobian, наших пакетов и ядра (около пяти минут). Прошивка <strong>стирает весь телефон</strong>.</p>" + BUILD_CMD + "<p>Подробности, предварительные условия и «подводные камни»: <a href=\"%s#быстрый-старт\">README в репозитории</a>.</p>" % SO),
    sec("Пакеты из репозитория", "<p>Пакеты лежат в подписанном apt-репозитории, релиз <b>garmon</b> (arm64). В образе источник уже включён; на другой системе на Poco F1:</p>" + APT_CMD + "<p>Отпечаток ключа подписи: <code>B27E 8856 988A 9019 BB9A 23F2 BBBD 1474 A352 F720</code>.</p>" +
        dl([("skladenos-config", "Системные настройки устройства и SXMO, сторож тача, fastfetch."),
            ("skladenos-firstboot", "Мастер первой загрузки (12 языков)."),
            ("skladenos-fonts, -wallpapers", "Шрифт значков и свободные обои (CC BY-SA 4.0)."),
            ("skladenos-artwork", "Логотип и фирменные обои (компонент <code>non-free</code>, права защищены)."),
            ("skladenos-archive-keyring", "Ключ репозитория и источник apt."),
            ("skladenos-emu-jornada720, -emu-psion", "Эмуляторы (см. ниже)."),
            ("skladenos-tools, -dev, -containers", "Метапакеты: htop, git, fastfetch…; сборка программ; podman.")], cls="feat")),
    sec("Эмуляторы", "<p>HP Jornada 720 (Windows CE, QEMU) и Psion 5mx (EPOC, WindEmu) ставятся пакетами <code>skladenos-emu-jornada720</code> и <code>skladenos-emu-psion</code> и запускаются из меню Scripts в SXMO. ROM в пакеты не входят, нужен свой: <code>~/roms/jornada720.bin</code> и <code>~/roms/5mx_eng.bin</code>. Сборка эмуляторов воспроизводится в Docker из наших форков (<a href=\"%s/qemu-jornada720\">qemu-jornada720</a>, <a href=\"%s/WindEmu\">WindEmu</a>).</p>" % ("https://github.com/DmitriiTrifonov", "https://github.com/DmitriiTrifonov")),
    sec("Основа и права", "<p><strong>skladenOS</strong> основан на <a href=\"https://mobian.org\">Mobian</a> и <a href=\"https://www.debian.org\">Debian</a>, но не является их официальным выпуском и не связан с этими проектами. Код открыт под GPL-3.0-or-later, патчи ядра — GPL-2.0-only, свободные обои — CC BY-SA 4.0; оконный менеджер SXMO распространяется под AGPL-3.0. Лицензия каждого файла описана по стандарту REUSE. Прошивки Qualcomm и Xiaomi мы не распространяем: система извлекает их на самом телефоне.</p><p><strong>Логотипы Mitya Labs и skladenOS © 2026 Dmitrii Trifonov, все права защищены.</strong> Правила использования названий и логотипа — в <a href=\"%s/blob/main/TRADEMARK.md\">TRADEMARK.md</a>.</p>" % SO, cls="body fine"),
    sec("Что дальше", road(["Образ собирается и прошивается из исходников", "Мастер первой загрузки на 12 языках", "Свой подписанный репозиторий пакетов, эмуляторы пакетами", "Публичный репозиторий, лицензии по REUSE", "Сборка ядра и образа в CI на GitHub", "Образ для скачивания (релиз v0.1.0, панель EBBG)", "Проверка с обоими вариантами панели Poco F1 (ebbg и tianma)"], 6)),
    sec("Ссылки", "<p>Репозиторий: <a href=\"%s\">github.com/mitya-labs/skladenos</a>. Образ и релизы: <a href=\"%s/releases\">releases</a>. Пакеты: <a href=\"%s\">mitya-labs.github.io/apt</a>. Вопросы и ошибки — <a href=\"%s/issues\">issues</a>. Новости — <a href=\"%s\">Telegram-канал</a>. Проекты ведёт организация <a href=\"%s\">mitya-labs</a>.</p>" % (SO, SO, APT, SO, TG, GH)),
])

EN_OS_PAGE = dict(
    lang="en", path="en/skladenos/", up="../../", home="../", ru_href="../../skladenos/", en_href="./", ru_cur="", en_cur=' aria-current="true"',
    langlabel="Language", navlabel="Sections and language", cfg_h=EN["cfg_h"], foot=EN["foot"],
    title="skladenOS: the system for Skladen and the Poco F1 — Mitya Labs",
    desc="skladenOS: Mobian and SXMO for the Xiaomi Poco F1 — what works, how to build the image, packages, emulators and the apt repository.",
    mark=MARK.format(alt="skladenOS mark: four folded panels"),
    lede="The system for Skladen and other folding devices: Mobian (Debian) with the SXMO window manager, a 7.2 kernel with our charging and USB-PD patches, a first-boot wizard and a set of packages.",
    status="<strong>The source and the package repository are open.</strong> A ready-made image for the Poco F1 (EBBG panel) is in the v0.1.0 release on GitHub; you can also build it from source with one command.",
)
EN_OS_PAGE["sections"] = "\n".join([
    sec("What it is", "<p>skladenOS is the system for the Xiaomi Poco F1 (SDM845), first of all as part of the <a href=\"../#skladen\">Skladen</a> palmtop, where the screen and the keyboard are joined by a hinge. It is built on <a href=\"https://mobian.org\">Mobian</a> (Debian forky) with the light <a href=\"https://sxmo.org\">SXMO</a> (sway) interface: gestures, volume keys, an external keyboard. Windows and bars keep clear of the notch and the rounded corners, even in fullscreen.</p>"),
    sec("What works", dl([
        ("Notch and corners", "The bar and windows keep clear of the cutout and adjust when the screen rotates."),
        ("Buttons and gestures", "Power, volume, edge gestures; <kbd>Super</kbd>+<kbd>Esc</kbd> works from an external keyboard."),
        ("First boot", "A wizard in 12 languages (English by default): Bluetooth keyboard, Wi-Fi, user name and a required password change."),
        ("USB and charging", "Host or device role is picked automatically; a hub, a flash drive and a keyboard work; USB-PD charging."),
        ("Power", "“Balanced”, “Eco”, “Night” and “Performance” profiles from the menu, plus a “keep screen awake” mode."),
        ("Layouts", "English and Russian switched with CapsLock, on-screen keyboard with Cyrillic."),
        ("Audio, sensors, network", "Both speakers, microphone, sensors through the SLPI on kernel 7.x, Wi-Fi and Bluetooth."),
        ("Touch watchdog", "A service resets the touchscreen driver when a touch gets stuck."),
        ("fastfetch", "Shows the skladenOS logo and the system name.")]) +
        '<p class="note">Verified on a Pocophone F1 (EBBG panel) with kernel 7.2: an image built from source is flashed and runs. The Tianma panel variant builds but is not verified on hardware. The SIM has not been tested.</p>'),
    sec("First boot", "<p>Right after flashing, log in as <code>skladen</code> with the password <code>1234</code>. A wizard starts on screen: language, a Bluetooth keyboard search, Wi-Fi, then a user name and a new password. Until the default password is changed, SSH password login is allowed only from local networks. The new user name takes effect after a reboot.</p>"),
    sec("How to build and flash", "<p>You need a Mac or Linux, Docker, <code>fastboot</code> and an unlocked bootloader. The image is assembled in Docker from the official Mobian rootfs, our packages and the kernel (about five minutes). Flashing <strong>erases the whole phone</strong>.</p>" + BUILD_CMD_EN + "<p>Details, prerequisites and pitfalls: the <a href=\"%s\">README in the repository</a>.</p>" % SO),
    sec("Packages from the repository", "<p>The packages live in a signed apt repository, release <b>garmon</b> (arm64). The image already has the source enabled; on another system on a Poco F1:</p>" + APT_CMD + "<p>Signing key fingerprint: <code>B27E 8856 988A 9019 BB9A 23F2 BBBD 1474 A352 F720</code>.</p>" +
        dl([("skladenos-config", "Device and SXMO system settings, the touch watchdog, fastfetch."),
            ("skladenos-firstboot", "The first-boot wizard (12 languages)."),
            ("skladenos-fonts, -wallpapers", "The icon font and the free wallpapers (CC BY-SA 4.0)."),
            ("skladenos-artwork", "The logo and the branded wallpapers (<code>non-free</code> component, all rights reserved)."),
            ("skladenos-archive-keyring", "The repository key and the apt source."),
            ("skladenos-emu-jornada720, -emu-psion", "Emulators (see below)."),
            ("skladenos-tools, -dev, -containers", "Metapackages: htop, git, fastfetch…; build tools; podman.")], cls="feat")),
    sec("Emulators", "<p>HP Jornada 720 (Windows CE, QEMU) and Psion 5mx (EPOC, WindEmu) install as the packages <code>skladenos-emu-jornada720</code> and <code>skladenos-emu-psion</code> and start from the Scripts menu in SXMO. ROMs are not included; bring your own: <code>~/roms/jornada720.bin</code> and <code>~/roms/5mx_eng.bin</code>. The emulators are built reproducibly in Docker from our forks (<a href=\"%s/qemu-jornada720\">qemu-jornada720</a>, <a href=\"%s/WindEmu\">WindEmu</a>).</p>" % ("https://github.com/DmitriiTrifonov", "https://github.com/DmitriiTrifonov")),
    sec("Basis and rights", "<p><strong>skladenOS</strong> is based on <a href=\"https://mobian.org\">Mobian</a> and <a href=\"https://www.debian.org\">Debian</a>, but it is not an official release of either and is not affiliated with those projects. The code is open under GPL-3.0-or-later, the kernel patches under GPL-2.0-only, the free wallpapers under CC BY-SA 4.0; the SXMO window manager is distributed under the AGPL-3.0. The license of every file is described to the REUSE standard. We do not distribute Qualcomm or Xiaomi firmware: the system extracts it on the phone itself.</p><p><strong>The Mitya Labs and skladenOS logos are © 2026 Dmitrii Trifonov, all rights reserved.</strong> The rules for using the names and the logo are in <a href=\"%s/blob/main/TRADEMARK.md\">TRADEMARK.md</a>.</p>" % SO, cls="body fine"),
    sec("What is next", road(["The image builds and flashes from source", "First-boot wizard in 12 languages", "Our own signed package repository, emulators as packages", "Public repository, licenses to the REUSE standard", "Kernel and image build in CI on GitHub", "A downloadable image (release v0.1.0, EBBG panel)", "Testing with both Poco F1 panel variants (ebbg and tianma)"], 6)),
    sec("Links", "<p>Repository: <a href=\"%s\">github.com/mitya-labs/skladenos</a>. Image and releases: <a href=\"%s/releases\">releases</a>. Packages: <a href=\"%s\">mitya-labs.github.io/apt</a>. Questions and bugs: <a href=\"%s/issues\">issues</a>. News: the <a href=\"%s\">Telegram channel</a>. The projects are run by the <a href=\"%s\">mitya-labs</a> organization.</p>" % (SO, SO, APT, SO, TG, GH)),
])


def build():
    for d, out in ((RU, "index.html"), (EN, "en/index.html")):
        html = PAGE.format(site=SITE, gh=GH, tg=TG, **d)
        os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
        open(os.path.join(ROOT, out), "w", encoding="utf-8").write(html)
        print("ok", out, len(html))
    for d, out in ((RU_OS_PAGE, "skladenos/index.html"), (EN_OS_PAGE, "en/skladenos/index.html")):
        html = OS_PAGE.format(site=SITE, gh=GH, tg=TG, **d)
        os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
        open(os.path.join(ROOT, out), "w", encoding="utf-8").write(html)
        print("ok", out, len(html))


if __name__ == "__main__":
    build()
