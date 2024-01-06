import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from google import google_translate

def generate_pdf_from_web_content(url):
    # 设置请求头部，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 使用Session对象发送HTTP请求获取网页内容，并设置连接超时时间为10秒
    with requests.Session() as session:
        try:
            response = session.get(url, headers=headers, timeout=(10, 10))
            response.raise_for_status()  # 检查是否有错误发生

            # 检查请求是否成功
            if response.status_code == 200:
                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # 获取文章标题
                title = soup.find('h1').text.strip()

                # 创建 PDF 文件以标题命名
                pdf_filename = f"{title.replace(' ', '_')}.pdf"
                doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

                # 添加中文支持的字体
                chinese_font_path = "C:\Windows\Fonts\msyh.ttc"
                pdfmetrics.registerFont(TTFont('SimSun', chinese_font_path))

                # 定义样式
                styles = getSampleStyleSheet()
                title_style = styles['Title']
                body_style = ParagraphStyle(
                    'BodyText',
                    parent=styles['BodyText'],
                    fontName='SimSun',  # Use SimSun for Chinese content
                )

                # 添加文章标题
                title_paragraph = Paragraph(title, title_style)
                doc.build([title_paragraph])

                # 添加文章内容
                paragraphs = soup.find_all('p')
                body_content = []
                for paragraph in paragraphs:
                    orig_content = paragraph.text
                    translate_content = google_translate(orig_content)
                    print(translate_content)
                    body_content.append(
                        Paragraph(f"Original: {orig_content}<br/><br/>Translated: {translate_content}", body_style))
                doc.build(body_content)

                print(f"文章已保存为 {pdf_filename}")

            else:
                print(f"无法获取网页内容，状态码: {response.status_code}")

        except requests.exceptions.Timeout:
            print('连接超时，请检查网络或增加超时时间。')
        except requests.exceptions.RequestException as e:
            print(f'发生其他请求异常: {e}')

# 使用函数获取并保存文章内容为 PDF
# url = "https://towardsdatascience.com/5-hard-truths-about-generative-ai-for-technology-leaders-4b119336bc85"
# generate_pdf_from_web_content(url)
