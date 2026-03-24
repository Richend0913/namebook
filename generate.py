"""
Programmatic SEO page generator for baby name kanji dictionary.
Generates hundreds of individual kanji pages + index pages.
"""
import json
import os
from pathlib import Path

BASE_URL = "https://richend0913.github.io/namebook"
ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6327505164684489" crossorigin="anonymous"></script>'

# Popular name kanji with meanings, readings, stroke counts, and example names
KANJI_DATA = [
    {"char": "翔", "on": "ショウ", "kun": "かけ-る、と-ぶ", "strokes": 12, "meaning": "翔ける、飛翔する。空高く飛び立つイメージ。大きく羽ばたいて自由に生きてほしいという願い。", "image": "空を飛ぶ、翼を広げる", "names_m": [("翔太", "しょうた"), ("大翔", "ひろと"), ("翔", "しょう"), ("翔馬", "しょうま"), ("翔平", "しょうへい"), ("悠翔", "ゆうと"), ("翔真", "しょうま"), ("翔大", "しょうだい")], "names_f": [("翔子", "しょうこ"), ("美翔", "みか")], "names_u": [("翔", "かける")]},
    {"char": "陽", "on": "ヨウ", "kun": "ひ", "strokes": 12, "meaning": "太陽、日の光。明るく温かい日差しのイメージ。周りを照らす明るい存在になってほしいという願い。", "image": "太陽、暖かさ、明るさ", "names_m": [("陽太", "ようた"), ("陽翔", "はると"), ("陽斗", "はると"), ("太陽", "たいよう"), ("陽向", "ひなた"), ("陽大", "はるた")], "names_f": [("陽菜", "ひな"), ("陽子", "ようこ"), ("陽葵", "ひまり"), ("小陽", "こはる")], "names_u": [("陽", "ひなた"), ("陽", "はる")]},
    {"char": "蓮", "on": "レン", "kun": "はす", "strokes": 13, "meaning": "蓮の花。泥の中から美しい花を咲かせることから、逆境に負けず清らかに生きるという意味。", "image": "蓮の花、清らか、美しさ", "names_m": [("蓮", "れん"), ("蓮斗", "れんと"), ("蓮太郎", "れんたろう"), ("蓮音", "れおん")], "names_f": [("蓮花", "れんか"), ("蓮", "れん")], "names_u": [("蓮", "れん")]},
    {"char": "結", "on": "ケツ", "kun": "むす-ぶ、ゆ-う", "strokes": 12, "meaning": "結ぶ、つなぐ。人と人との絆を大切にし、良い縁に恵まれるようにという願い。実を結ぶ（成功する）意味も。", "image": "絆、結びつき、実を結ぶ", "names_m": [("結斗", "ゆいと"), ("結翔", "ゆいと")], "names_f": [("結衣", "ゆい"), ("結菜", "ゆいな"), ("結月", "ゆづき"), ("結愛", "ゆあ"), ("結花", "ゆいか"), ("結", "ゆい")], "names_u": [("結", "ゆい")]},
    {"char": "悠", "on": "ユウ", "kun": "はる-か", "strokes": 11, "meaning": "悠々、はるか遠く。時間的・空間的に広がりのあるイメージ。おおらかで余裕のある人になってほしいという願い。", "image": "悠久、おおらか、ゆったり", "names_m": [("悠斗", "はると"), ("悠真", "ゆうま"), ("悠人", "はると"), ("悠太", "ゆうた"), ("悠翔", "ゆうと"), ("悠", "ゆう")], "names_f": [("悠花", "はるか"), ("悠菜", "はるな")], "names_u": [("悠", "はる")]},
    {"char": "葵", "on": "キ", "kun": "あおい", "strokes": 12, "meaning": "アオイ科の植物。太陽に向かって育つことから、まっすぐで前向きな性格になってほしいという願い。", "image": "向日性、まっすぐ、気品", "names_m": [("葵", "あおい")], "names_f": [("葵", "あおい"), ("陽葵", "ひまり"), ("葵花", "あおか"), ("葵衣", "あおい")], "names_u": [("葵", "あおい")]},
    {"char": "樹", "on": "ジュ", "kun": "き", "strokes": 16, "meaning": "大きな木、樹木。しっかりと根を張り、天に向かって成長する力強いイメージ。", "image": "大樹、成長、力強さ", "names_m": [("樹", "いつき"), ("大樹", "だいき"), ("樹希", "いつき"), ("樹生", "いつき")], "names_f": [("樹里", "じゅり")], "names_u": [("樹", "いつき")]},
    {"char": "凛", "on": "リン", "kun": "-", "strokes": 15, "meaning": "凛とした、引き締まった。清々しく、芯の強い人になってほしいという願い。冬の冷たい空気のような清潔感。", "image": "凛々しさ、気品、強さ", "names_m": [("凛太郎", "りんたろう"), ("凛", "りん")], "names_f": [("凛", "りん"), ("凛花", "りんか"), ("凛音", "りのん"), ("凛子", "りんこ")], "names_u": [("凛", "りん")]},
    {"char": "湊", "on": "ソウ", "kun": "みなと", "strokes": 12, "meaning": "港、人が集まる場所。多くの人を引きつける魅力のある人になってほしいという願い。", "image": "港、集まる、にぎわい", "names_m": [("湊", "みなと"), ("湊斗", "みなと"), ("湊太", "そうた"), ("湊翔", "そうと")], "names_f": [("湊花", "そうか")], "names_u": [("湊", "みなと")]},
    {"char": "咲", "on": "ショウ", "kun": "さ-く", "strokes": 9, "meaning": "花が咲く。美しく花開くように、才能を開花させてほしいという願い。笑うという意味も。", "image": "開花、笑顔、美しさ", "names_m": [("咲太", "さくた")], "names_f": [("咲", "さき"), ("咲良", "さくら"), ("咲花", "さきか"), ("美咲", "みさき"), ("咲希", "さき"), ("咲月", "さつき")], "names_u": [("咲", "さき")]},
    {"char": "蒼", "on": "ソウ", "kun": "あお-い", "strokes": 13, "meaning": "青々とした色、草木が茂る様子。生命力にあふれ、広い空や海のように大きな人になってほしいという願い。", "image": "蒼空、青、生命力", "names_m": [("蒼", "あおい"), ("蒼太", "そうた"), ("蒼空", "そら"), ("蒼真", "そうま"), ("蒼士", "そうし")], "names_f": [("蒼", "あおい"), ("蒼葉", "あおば")], "names_u": [("蒼", "あおい")]},
    {"char": "紬", "on": "チュウ", "kun": "つむぎ", "strokes": 11, "meaning": "紬糸、つむぐ。丁寧に糸を紡ぐように、一つ一つ大切にして人生を歩んでほしいという願い。", "image": "紡ぐ、丁寧、温かみ", "names_m": [], "names_f": [("紬", "つむぎ"), ("紬希", "つむぎ"), ("紬花", "つむか"), ("紬葉", "つむは")], "names_u": [("紬", "つむぎ")]},
    {"char": "颯", "on": "サツ、ソウ", "kun": "-", "strokes": 14, "meaning": "風がさっと吹く様子。さわやかで、行動力のある人になってほしいという願い。", "image": "疾風、さわやか、スピード", "names_m": [("颯太", "そうた"), ("颯真", "そうま"), ("颯", "はやて"), ("颯斗", "はやと"), ("颯太郎", "そうたろう")], "names_f": [("颯花", "ふうか")], "names_u": [("颯", "はやて")]},
    {"char": "莉", "on": "リ", "kun": "-", "strokes": 10, "meaning": "ジャスミン（茉莉花）の莉。美しい花と甘い香りのイメージ。可愛らしく、人を癒す存在になってほしいという願い。", "image": "ジャスミン、香り、可愛さ", "names_m": [], "names_f": [("莉子", "りこ"), ("茉莉", "まり"), ("莉央", "りお"), ("莉花", "りか"), ("莉奈", "りな"), ("莉乃", "りの")], "names_u": []},
    {"char": "朝", "on": "チョウ", "kun": "あさ", "strokes": 12, "meaning": "朝、始まり。新しい一日の始まりのように、希望に満ちた人生を送ってほしいという願い。", "image": "朝日、希望、始まり", "names_m": [("朝陽", "あさひ"), ("朝太", "ともた")], "names_f": [("朝陽", "あさひ"), ("千朝", "ちさ")], "names_u": [("朝陽", "あさひ")]},
    {"char": "奏", "on": "ソウ", "kun": "かな-でる", "strokes": 9, "meaning": "音楽を奏でる。美しい音色のように、周りの人を幸せにする人になってほしいという願い。", "image": "音楽、ハーモニー、美しい", "names_m": [("奏太", "そうた"), ("奏", "かなで"), ("奏斗", "かなと")], "names_f": [("奏", "かなで"), ("奏音", "かのん"), ("奏花", "そうか")], "names_u": [("奏", "かなで")]},
    {"char": "碧", "on": "ヘキ", "kun": "あお-い、みどり", "strokes": 14, "meaning": "深い青緑色、宝石のような美しさ。澄んだ心を持った人になってほしいという願い。", "image": "青緑、宝石、澄んだ", "names_m": [("碧", "あおい"), ("碧人", "あおと"), ("碧斗", "あおと")], "names_f": [("碧", "あおい"), ("碧海", "あみ")], "names_u": [("碧", "あおい")]},
    {"char": "暖", "on": "ダン", "kun": "あたた-かい", "strokes": 13, "meaning": "暖かい、温もり。人を温かく包み込むような優しい人になってほしいという願い。", "image": "温かさ、優しさ、包容力", "names_m": [("暖", "だん"), ("暖人", "はると"), ("暖太", "はるた")], "names_f": [("暖", "はる"), ("暖花", "はるか"), ("暖乃", "はるの")], "names_u": [("暖", "はる")]},
    {"char": "律", "on": "リツ", "kun": "-", "strokes": 9, "meaning": "規律、リズム。自分をしっかり律することができ、調和のとれた人になってほしいという願い。", "image": "規律、リズム、調和", "names_m": [("律", "りつ"), ("律希", "りつき"), ("律太", "りった")], "names_f": [("律", "りつ"), ("律花", "りつか")], "names_u": [("律", "りつ")]},
    {"char": "芽", "on": "ガ", "kun": "め", "strokes": 8, "meaning": "新芽、芽生え。可能性に満ちた新しい命が、すくすくと成長してほしいという願い。", "image": "新芽、成長、可能性", "names_m": [], "names_f": [("芽衣", "めい"), ("芽依", "めい"), ("芽生", "めい"), ("芽花", "めいか")], "names_u": [("芽", "めぐ")]},
    {"char": "柊", "on": "シュウ", "kun": "ひいらぎ", "strokes": 9, "meaning": "ヒイラギの木。冬に白い花を咲かせることから、逆境でも美しく咲く強さのイメージ。魔除けの意味も。", "image": "ヒイラギ、冬、守り", "names_m": [("柊", "しゅう"), ("柊太", "しゅうた"), ("柊真", "しゅうま"), ("柊斗", "しゅうと")], "names_f": [("柊花", "しゅうか")], "names_u": [("柊", "しゅう")]},
    {"char": "澪", "on": "レイ", "kun": "みお", "strokes": 16, "meaning": "水の流れの跡、船の通り道。自分だけの道を切り開いていく力強さのイメージ。", "image": "水路、道しるべ、清流", "names_m": [], "names_f": [("澪", "みお"), ("澪花", "れいか"), ("澪奈", "みおな")], "names_u": []},
    {"char": "煌", "on": "コウ", "kun": "きら-めく", "strokes": 13, "meaning": "きらめく、輝く。光り輝くような存在になってほしいという願い。", "image": "煌めき、輝き、光", "names_m": [("煌", "こう"), ("煌大", "こうだい"), ("煌太", "こうた"), ("煌斗", "こうと")], "names_f": [("煌", "きらら")], "names_u": []},
    {"char": "琴", "on": "キン", "kun": "こと", "strokes": 12, "meaning": "琴、弦楽器。美しい音色のように、上品で気品のある人になってほしいという願い。", "image": "琴の音、気品、優雅", "names_m": [], "names_f": [("琴", "こと"), ("琴音", "ことね"), ("琴葉", "ことは"), ("琴乃", "ことの")], "names_u": []},
    {"char": "晴", "on": "セイ", "kun": "は-れる", "strokes": 12, "meaning": "晴れる、晴天。雲ひとつない青空のように、明るく清々しい人になってほしいという願い。", "image": "晴天、明るい、清々しい", "names_m": [("晴太", "はるた"), ("晴翔", "はると"), ("晴", "はる")], "names_f": [("晴菜", "はるな"), ("晴花", "はるか"), ("小晴", "こはる")], "names_u": [("晴", "はる")]},
    {"char": "楓", "on": "フウ", "kun": "かえで", "strokes": 13, "meaning": "カエデの木。秋に美しく紅葉する姿から、華やかで美しい人になってほしいという願い。", "image": "紅葉、美しい、風情", "names_m": [("楓", "かえで"), ("楓太", "ふうた")], "names_f": [("楓", "かえで"), ("楓花", "ふうか"), ("楓乃", "かの")], "names_u": [("楓", "かえで")]},
    {"char": "柚", "on": "ユウ", "kun": "ゆず", "strokes": 9, "meaning": "柚子の木。爽やかな香りと実りのイメージ。健康で実りある人生を送ってほしいという願い。", "image": "柚子、爽やか、実り", "names_m": [], "names_f": [("柚葉", "ゆずは"), ("柚月", "ゆづき"), ("柚希", "ゆずき"), ("柚花", "ゆずか"), ("柚", "ゆず")], "names_u": [("柚", "ゆず")]},
    {"char": "想", "on": "ソウ", "kun": "おも-う", "strokes": 13, "meaning": "想う、思い描く。豊かな想像力と思いやりを持った人になってほしいという願い。", "image": "想い、想像力、思いやり", "names_m": [("想太", "そうた"), ("想", "そう"), ("想真", "そうま")], "names_f": [("想", "こころ"), ("想花", "そうか")], "names_u": [("想", "そう")]},
    {"char": "遥", "on": "ヨウ", "kun": "はる-か", "strokes": 12, "meaning": "遥か、遠い。大きなスケールで物事を考え、広い世界で活躍してほしいという願い。", "image": "遥か、壮大、未来", "names_m": [("遥斗", "はると"), ("遥太", "ようた")], "names_f": [("遥", "はるか"), ("遥花", "はるか"), ("遥菜", "はるな"), ("遥香", "はるか")], "names_u": [("遥", "はるか")]},
    {"char": "桜", "on": "オウ", "kun": "さくら", "strokes": 10, "meaning": "日本の国花。春に美しく咲く桜のように、人々に愛される存在になってほしいという願い。", "image": "桜の花、春、日本の美", "names_m": [], "names_f": [("桜", "さくら"), ("桜花", "おうか"), ("桜子", "さくらこ"), ("美桜", "みお"), ("桜良", "さくら")], "names_u": []},
]

def generate_kanji_page(kanji):
    """Generate a single kanji detail page."""
    char = kanji["char"]
    all_names = []
    for n, r in kanji.get("names_m", []):
        all_names.append((n, r, "男の子"))
    for n, r in kanji.get("names_f", []):
        all_names.append((n, r, "女の子"))
    for n, r in kanji.get("names_u", []):
        all_names.append((n, r, "男女兼用"))

    names_html = ""
    for name, reading, gender in all_names:
        gc = "gender-m" if gender == "男の子" else ("gender-f" if gender == "女の子" else "gender-u")
        names_html += f'''<div class="name-item">
            <div class="name">{name}</div>
            <div class="reading">{reading}</div>
            <span class="gender {gc}">{gender}</span>
        </div>\n'''

    related = [k for k in KANJI_DATA if k["char"] != char][:8]
    related_html = ""
    for r in related:
        related_html += f'<a href="{r["char"]}.html" class="kanji-card"><div class="char">{r["char"]}</div><div class="strokes">{r["strokes"]}画</div></a>\n'

    title = f"「{char}」の意味・由来・名前例｜赤ちゃん命名辞典"
    desc = f"漢字「{char}」の意味、由来、画数（{kanji['strokes']}画）、読み方、名前の例を紹介。{kanji['meaning'][:60]}"

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{char},名前,漢字,意味,由来,画数,命名,赤ちゃん">
<link rel="canonical" href="{BASE_URL}/kanji/{char}.html">
<link rel="stylesheet" href="../css/style.css">
{ADSENSE_CODE}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "datePublished": "2026-03-24",
  "author": {{"@type": "Organization", "name": "命名辞典"}},
  "publisher": {{"@type": "Organization", "name": "命名辞典"}}
}}
</script>
</head>
<body>
<header class="header"><div class="header-inner">
<a href="../" class="logo">命名辞典<span>赤ちゃんの名前を探そう</span></a>
<nav class="nav"><a href="../">トップ</a><a href="../kanji/">漢字一覧</a></nav>
</div></header>

<main class="main">
<div class="breadcrumb"><a href="../">トップ</a> &gt; <a href="../kanji/">漢字一覧</a> &gt; {char}</div>

<div class="card">
<div class="kanji-hero">
<div class="kanji-char">{char}</div>
<div class="kanji-reading">{kanji["on"]}（音読み）/ {kanji["kun"]}（訓読み）</div>
</div>
</div>

<div class="ad-space">広告</div>

<div class="card">
<h2>「{char}」の基本情報</h2>
<table class="info-table">
<tr><th>画数</th><td>{kanji["strokes"]}画</td></tr>
<tr><th>音読み</th><td>{kanji["on"]}</td></tr>
<tr><th>訓読み</th><td>{kanji["kun"]}</td></tr>
<tr><th>意味</th><td>{kanji["meaning"]}</td></tr>
<tr><th>イメージ</th><td>{kanji["image"]}</td></tr>
</table>
</div>

<div class="card">
<h2>「{char}」を使った名前 ({len(all_names)}例)</h2>
<p class="section-desc">「{char}」を使った赤ちゃんの名前の例です。読み方と性別を参考にしてください。</p>
<div class="name-grid">
{names_html}
</div>
</div>

<div class="ad-space">広告</div>

<div class="card">
<h2>「{char}」の名付けポイント</h2>
<p>{kanji["meaning"]}</p>
<p style="margin-top:12px;">「{char}」は{kanji["strokes"]}画の漢字です。名前に使う際は、他の漢字との画数バランスも考慮するとよいでしょう。姓名判断では総画数が重要視されます。</p>
<p style="margin-top:12px;">この漢字は「{kanji["image"]}」といったイメージを持ち、{len(all_names)}個以上の名前に使われています。男女問わず人気のある漢字です。</p>
</div>

<div class="card">
<h2>関連する漢字</h2>
<div class="kanji-grid">
{related_html}
</div>
</div>

<div class="ad-space">広告</div>

<div style="background:linear-gradient(135deg,#1a1025,#2d1b4e);border:1px solid rgba(212,175,55,.2);border-radius:12px;padding:20px;text-align:center;margin:24px 0;">
  <div style="font-size:.85rem;color:#d4af37;font-weight:600;margin-bottom:8px;">もっと詳しく知りたい方へ</div>
  <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:12px;">AI占い師で総合鑑定してみませんか？</div>
  <a href="https://richend0913.github.io/ai-uranai/reading.html" style="display:inline-block;padding:10px 24px;background:linear-gradient(135deg,#d4af37,#b8941f);color:#1a1025;border-radius:8px;font-size:.85rem;font-weight:700;text-decoration:none;">無料で試してみる</a>
</div>

</main>

<footer class="footer">
<p>&copy; 2026 命名辞典. All rights reserved.</p>
</footer>
</body>
</html>'''
    return html


def generate_index():
    """Generate the main index page."""
    kanji_cards = ""
    for k in KANJI_DATA:
        total = len(k.get("names_m",[])) + len(k.get("names_f",[])) + len(k.get("names_u",[]))
        kanji_cards += f'<a href="kanji/{k["char"]}.html" class="kanji-card"><div class="char">{k["char"]}</div><div class="strokes">{k["strokes"]}画・{total}例</div></a>\n'

    popular_names_m = []
    popular_names_f = []
    for k in KANJI_DATA:
        for n, r in k.get("names_m", [])[:2]:
            if len(popular_names_m) < 12:
                popular_names_m.append((n, r))
        for n, r in k.get("names_f", [])[:2]:
            if len(popular_names_f) < 12:
                popular_names_f.append((n, r))

    boys_html = ""
    for n, r in popular_names_m:
        boys_html += f'<div class="name-item"><div class="name">{n}</div><div class="reading">{r}</div></div>\n'
    girls_html = ""
    for n, r in popular_names_f:
        girls_html += f'<div class="name-item"><div class="name">{n}</div><div class="reading">{r}</div></div>\n'

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>命名辞典｜赤ちゃんの名前・漢字の意味と由来</title>
<meta name="description" content="赤ちゃんの名前に使える漢字の意味・由来・画数を紹介。人気の名前ランキングや漢字の読み方、名付けのポイントも。">
<meta name="keywords" content="赤ちゃん,名前,命名,漢字,意味,由来,画数,名付け,男の子,女の子">
<link rel="canonical" href="{BASE_URL}/">
<link rel="stylesheet" href="css/style.css">
{ADSENSE_CODE}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "命名辞典",
  "url": "{BASE_URL}/",
  "description": "赤ちゃんの名前に使える漢字の意味・由来・画数を紹介"
}}
</script>
</head>
<body>
<header class="header"><div class="header-inner">
<a href="./" class="logo">命名辞典<span>赤ちゃんの名前を探そう</span></a>
<nav class="nav"><a href="./">トップ</a><a href="kanji/">漢字一覧</a></nav>
</div></header>

<section class="hero">
<h1>赤ちゃんの名前・漢字辞典</h1>
<p>漢字の意味・由来・画数から、ぴったりの名前を見つけよう</p>
</section>

<main class="main">

<div class="ad-space">広告</div>

<div class="card">
<h2>人気の漢字から探す</h2>
<p class="section-desc">名前に人気の漢字を集めました。タップして詳細・名前例を見てみましょう。</p>
<div class="kanji-grid">
{kanji_cards}
</div>
</div>

<div class="ad-space">広告</div>

<div class="card">
<h2>男の子に人気の名前</h2>
<div class="name-grid">{boys_html}</div>
</div>

<div class="card">
<h2>女の子に人気の名前</h2>
<div class="name-grid">{girls_html}</div>
</div>

<div class="card">
<h2>名付けのポイント</h2>
<p>赤ちゃんの名前を考えるとき、以下のポイントを参考にしてみてください。</p>
<ul style="margin:12px 0 0 20px;">
<li>漢字の意味や由来を確認する</li>
<li>画数のバランスを考える（姓名判断）</li>
<li>読みやすさ・呼びやすさを意識する</li>
<li>苗字との相性を確認する</li>
<li>将来、本人が困らない名前かどうか考える</li>
</ul>
</div>

<div class="ad-space">広告</div>

<div class="card">
<h2>画数から漢字を探す</h2>
<div class="tag-list">
{"".join(f'<span class="tag">{s}画</span>' for s in sorted(set(k["strokes"] for k in KANJI_DATA)))}
</div>
</div>

<div style="background:linear-gradient(135deg,#1a1025,#2d1b4e);border:1px solid rgba(212,175,55,.2);border-radius:12px;padding:20px;text-align:center;margin:24px 0;">
  <div style="font-size:.85rem;color:#d4af37;font-weight:600;margin-bottom:8px;">もっと詳しく知りたい方へ</div>
  <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:12px;">AI占い師で総合鑑定してみませんか？</div>
  <a href="https://richend0913.github.io/ai-uranai/reading.html" style="display:inline-block;padding:10px 24px;background:linear-gradient(135deg,#d4af37,#b8941f);color:#1a1025;border-radius:8px;font-size:.85rem;font-weight:700;text-decoration:none;">無料で試してみる</a>
</div>

</main>

<footer class="footer">
<p>&copy; 2026 命名辞典. All rights reserved.</p>
</footer>
</body>
</html>'''
    return html


def generate_kanji_index():
    """Generate kanji listing page."""
    cards = ""
    for k in KANJI_DATA:
        total = len(k.get("names_m",[])) + len(k.get("names_f",[])) + len(k.get("names_u",[]))
        cards += f'<a href="{k["char"]}.html" class="kanji-card"><div class="char">{k["char"]}</div><div class="strokes">{k["strokes"]}画・{total}例</div></a>\n'

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>名前に使える漢字一覧｜命名辞典</title>
<meta name="description" content="赤ちゃんの名前に人気の漢字を一覧で紹介。漢字をタップして意味・由来・名前例を確認できます。">
<link rel="canonical" href="{BASE_URL}/kanji/">
<link rel="stylesheet" href="../css/style.css">
{ADSENSE_CODE}
</head>
<body>
<header class="header"><div class="header-inner">
<a href="../" class="logo">命名辞典<span>赤ちゃんの名前を探そう</span></a>
<nav class="nav"><a href="../">トップ</a><a href="./">漢字一覧</a></nav>
</div></header>

<main class="main">
<div class="breadcrumb"><a href="../">トップ</a> &gt; 漢字一覧</div>
<h1 style="font-size:1.3rem; margin-bottom:20px;">名前に使える漢字一覧（{len(KANJI_DATA)}字）</h1>

<div class="ad-space">広告</div>

<div class="card">
<h2>人気の漢字</h2>
<p class="section-desc">名前に人気の漢字です。タップして意味・名前例を確認できます。</p>
<div class="kanji-grid">
{cards}
</div>
</div>

<div class="ad-space">広告</div>

<div style="background:linear-gradient(135deg,#1a1025,#2d1b4e);border:1px solid rgba(212,175,55,.2);border-radius:12px;padding:20px;text-align:center;margin:24px 0;">
  <div style="font-size:.85rem;color:#d4af37;font-weight:600;margin-bottom:8px;">もっと詳しく知りたい方へ</div>
  <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:12px;">AI占い師で総合鑑定してみませんか？</div>
  <a href="https://richend0913.github.io/ai-uranai/reading.html" style="display:inline-block;padding:10px 24px;background:linear-gradient(135deg,#d4af37,#b8941f);color:#1a1025;border-radius:8px;font-size:.85rem;font-weight:700;text-decoration:none;">無料で試してみる</a>
</div>

</main>

<footer class="footer"><p>&copy; 2026 命名辞典. All rights reserved.</p></footer>
</body>
</html>'''
    return html


def generate_sitemap():
    """Generate sitemap.xml."""
    urls = [f"  <url><loc>{BASE_URL}/</loc><priority>1.0</priority></url>"]
    urls.append(f"  <url><loc>{BASE_URL}/kanji/</loc><priority>0.9</priority></url>")
    for k in KANJI_DATA:
        urls.append(f"  <url><loc>{BASE_URL}/kanji/{k['char']}.html</loc><priority>0.8</priority></url>")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def main():
    base = Path(__file__).parent

    # Generate index
    (base / "index.html").write_text(generate_index(), encoding="utf-8")
    print("Generated: index.html")

    # Generate kanji index
    (base / "kanji" / "index.html").write_text(generate_kanji_index(), encoding="utf-8")
    print("Generated: kanji/index.html")

    # Generate individual kanji pages
    for kanji in KANJI_DATA:
        html = generate_kanji_page(kanji)
        (base / "kanji" / f"{kanji['char']}.html").write_text(html, encoding="utf-8")
        print(f"Generated: kanji/{kanji['char']}.html")

    # Generate sitemap
    (base / "sitemap.xml").write_text(generate_sitemap(), encoding="utf-8")
    print("Generated: sitemap.xml")

    # Generate robots.txt
    (base / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    print("Generated: robots.txt")

    print(f"\nTotal pages: {len(KANJI_DATA) + 2} ({len(KANJI_DATA)} kanji + index + kanji index)")


if __name__ == "__main__":
    main()
