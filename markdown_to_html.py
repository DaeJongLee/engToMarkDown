import tkinter as tk
from tkinter import scrolledtext
from deep_translator import GoogleTranslator
import textwrap
from collections import Counter
import re
import unicodedata
import markdown

MAX_LINE_LENGTH = 70

def get_user_input():
    def on_submit():
        nonlocal user_input
        user_input = text_area.get("1.0", tk.END).strip()
        root.quit()

    root = tk.Tk()
    root.title("영어 텍스트 입력")
    
    text_area = scrolledtext.ScrolledText(root, width=60, height=20)
    text_area.pack(padx=10, pady=10)
    
    submit_button = tk.Button(root, text="제출", command=on_submit)
    submit_button.pack(pady=10)
    
    user_input = None
    root.mainloop()
    
    root.destroy()
    return user_input

def translate_text(text):
    translator = GoogleTranslator(source='en', target='ko')
    chunks = textwrap.wrap(text, 5000)
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return ' '.join(translated_chunks)

def get_string_width(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'FW' else 1 for c in s)

def wrap_text(text, is_korean=False):
    wrapped_lines = []
    for line in text.split('\n'):
        if is_korean:
            current_line = ''
            for word in line.split():
                if get_string_width(current_line + word) <= MAX_LINE_LENGTH:
                    current_line += word + ' '
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + ' '
            if current_line:
                wrapped_lines.append(current_line.strip())
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=MAX_LINE_LENGTH))
    return '\n'.join(wrapped_lines)

def extract_key_words(text, num_words=20):
    words = re.findall(r'\b[A-Za-z][A-Za-z-]+\b', text.lower())
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    words = [word for word in words if word not in stop_words]
    return [word for word, _ in Counter(words).most_common(num_words)]

def translate_words(words):
    translator = GoogleTranslator(source='en', target='ko')
    return [translator.translate(word) for word in words]

def create_word_list(english_text):
    key_words = extract_key_words(english_text, num_words=20)
    translated_words = translate_words(key_words)
    return list(zip(key_words, translated_words))

def get_title(text):
    first_sentence = text.split('.')[0].strip()
    return first_sentence if len(first_sentence) <= 50 else first_sentence[:47] + "..."

def create_markdown(english_text, korean_text):
    title = get_title(english_text)
    word_pairs = create_word_list(english_text)
    
    # HTML 테이블로 단어 목록 생성
    word_list_html = """<table border="1">
    <tr>
        <th>영어</th>
        <th>한국어</th>
        <th>영어</th>
        <th>한국어</th>
    </tr>
"""
    for i in range(0, len(word_pairs), 2):
        word_list_html += "<tr>"
        word_list_html += f"<td>{word_pairs[i][0]}</td><td>{word_pairs[i][1]}</td>"
        if i + 1 < len(word_pairs):
            word_list_html += f"<td>{word_pairs[i+1][0]}</td><td>{word_pairs[i+1][1]}</td>"
        else:
            word_list_html += "<td></td><td></td>"
        word_list_html += "</tr>\n"
    word_list_html += "</table>"

    markdown_template = """# {title}

## English (Original)

{english_text}

## 한국어 (번역)

{korean_text}

## 주요 단어 목록

{word_list_html}
"""

    return markdown_template.format(
        title=title,
        english_text=wrap_text(english_text),
        korean_text=wrap_text(korean_text, is_korean=True),
        word_list_html=word_list_html
    )
def create_html(markdown_content):
    html_content = markdown.markdown(markdown_content)

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        {content}
    </body>
    </html>
    """

    title = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    title = title.group(1) if title else "Markdown Document"

    return html_template.format(title=title, content=html_content)

def main():
    try:
        print("영어 텍스트를 입력하세요.")
        english_text = get_user_input()
        if english_text is None:
            print("사용자가 입력을 취소했습니다.")
            return

        print("번역 중...")
        korean_text = translate_text(english_text)
        
        print("Markdown 생성 중...")
        markdown_content = create_markdown(english_text, korean_text)
        
        print("HTML 생성 중...")
        html_content = create_html(markdown_content)
        
        with open("data_science_article.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        with open("data_science_article.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("Markdown 파일이 생성되었습니다: data_science_article.md")
        print("HTML 파일이 생성되었습니다: data_science_article.html")
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()