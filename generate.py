# generate.py — версия с категорией "ИИ"
import feedparser
from datetime import datetime
import html

# Общие источники
GENERAL_FEEDS = [
    ("Лента.ру", "https://lenta.ru/rss"),
    ("РИА Новости", "https://ria.ru/export/rss2/news/index.xml"),
]

# Специализированные источники по ИИ
AI_FEEDS = [
    ("Хабр — ИИ", "https://habr.com/ru/rss/articles/?tag=10047"),  # тег "Искусственный интеллект"
    ("VC.ru — ИИ", "https://vc.ru/feed/tag/345"),                  # тег "Искусственный интеллект"
]

def clean(text):
    return html.escape(text).replace("\n", " ")[:250] + "..."

def fetch_articles(feeds, limit=8):
    articles = []
    for source_name, url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                pub_date = entry.get("published", "")
                try:
                    parsed_date = datetime.strptime(pub_date[:-6], "%a, %d %b %Y %H:%M:%S")
                    pub_date = parsed_date.strftime("%d.%m.%Y %H:%M")
                except:
                    pass
                articles.append({
                    "title": clean(entry.get("title", "Без заголовка")),
                    "link": entry.get("link", "#"),
                    "summary": clean(entry.get("summary", entry.get("description", ""))),
                    "source": source_name,
                    "date": pub_date,
                })
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")
    return articles

def generate_html(general_news, ai_news):
    html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Новостной Агрегатор с ИИ</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 900px; margin: 20px auto; padding: 0 15px; background: #fafafa; color: #222; }
        header { text-align: center; margin-bottom: 30px; }
        h1 { color: #1a73e8; }
        section { margin-bottom: 40px; }
        h2 { border-left: 4px solid #1a73e8; padding-left: 12px; color: #1a1a1a; }
        article { margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
        h3 { margin: 0; font-size: 1.25em; }
        h3 a { text-decoration: none; color: #1a0dab; }
        h3 a:hover { text-decoration: underline; }
        .meta { font-size: 0.85em; color: #666; margin: 6px 0; }
        .summary { color: #333; line-height: 1.5; }
        footer { text-align: center; margin-top: 40px; color: #888; font-size: 0.9em; }
    </style>
</head>
<body>
    <header>
        <h1>🗞️ Новостной Агрегатор</h1>
        <p>Общие новости и специальный раздел — Искусственный Интеллект</p>
    </header>

    <section>
        <h2>🧠 Новости об ИИ</h2>
"""
    if ai_news:
        for art in ai_news:
            html_content += f"""
        <article>
            <h3><a href="{art['link']}" target="_blank">{art['title']}</a></h3>
            <div class="meta">{art['date']} | {art['source']}</div>
            <div class="summary">{art['summary']}</div>
        </article>
"""
    else:
        html_content += "        <p>Новости об ИИ временно недоступны.</p>\n"

    html_content += """
    </section>

    <section>
        <h2>📰 Общие новости</h2>
"""

    if general_news:
        for art in general_news:
            html_content += f"""
        <article>
            <h3><a href="{art['link']}" target="_blank">{art['title']}</a></h3>
            <div class="meta">{art['date']} | {art['source']}</div>
            <div class="summary">{art['summary']}</div>
        </article>
"""
    else:
        html_content += "        <p>Общие новости временно недоступны.</p>\n"

    html_content += """
    </section>

    <footer>
        Обновляется вручную. Проект для обучения.
    </footer>
</body>
</html>
"""
    return html_content

if __name__ == "__main__":
    print("Сбор общих новостей...")
    general = fetch_articles(GENERAL_FEEDS, limit=6)
    print("Сбор новостей об ИИ...")
    ai = fetch_articles(AI_FEEDS, limit=6)

    html_output = generate_html(general, ai)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ Готово! Найдено: {len(general)} общих, {len(ai)} по ИИ.")
    print("Открой index.html в браузере или загрузи на GitHub Pages.")
