import tkinter as tk
from tkinter import scrolledtext
from deep_translator import GoogleTranslator
import textwrap
from collections import Counter
import re
import unicodedata
import markdown
import pyperclip

MAX_LINE_LENGTH = 70

def get_clipboard_content_with_confirmation():
    def on_submit(output_type):
        nonlocal user_confirmed, selected_output
        user_confirmed = True
        selected_output = output_type
        root.quit()

    def on_cancel():
        nonlocal user_confirmed
        user_confirmed = False
        root.quit()

    root = tk.Tk()
    root.title("클립보드 내용 확인")

    label = tk.Label(root, text="클립보드의 내용이 다음과 같습니다. 진행하시겠습니까?")
    label.pack(padx=10, pady=10)

    text_area = scrolledtext.ScrolledText(root, width=60, height=20)
    text_area.pack(padx=10, pady=10)
    
    clipboard_content = pyperclip.paste()
    text_area.insert(tk.END, clipboard_content)
    text_area.config(state='disabled')  # 읽기 전용으로 설정

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    markdown_button = tk.Button(button_frame, text="Markdown", command=lambda: on_submit("markdown"))
    markdown_button.pack(side=tk.LEFT, padx=5)

    html_button = tk.Button(button_frame, text="HTML", command=lambda: on_submit("html"))
    html_button.pack(side=tk.LEFT, padx=5)

    both_button = tk.Button(button_frame, text="둘 다", command=lambda: on_submit("both"))
    both_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="취소", command=on_cancel)
    cancel_button.pack(side=tk.LEFT, padx=5)

    user_confirmed = None
    selected_output = None
    root.mainloop()

    root.destroy()
    return (clipboard_content, selected_output) if user_confirmed else (None, None)

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
        print("클립보드 내용을 확인하는 중...")
        english_text, output_type = get_clipboard_content_with_confirmation()
        if english_text is None or output_type is None:
            print("사용자가 작업을 취소했거나 클립보드가 비어 있습니다.")
            return

        print("번역 중...")
        korean_text = translate_text(english_text)
        
        print("Markdown 생성 중...")
        markdown_content = create_markdown(english_text, korean_text)
        
        if output_type in ["markdown", "both"]:
            with open("output.md", "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print("Markdown 파일이 생성되었습니다: output.md")
        
        if output_type in ["html", "both"]:
            print("HTML 생성 중...")
            html_content = create_html(markdown_content)
            with open("output.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML 파일이 생성되었습니다: output.html")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()