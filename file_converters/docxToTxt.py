from docx import Document

def docx_to_txt(docxFile, txtFile):
    # Открываем документ .docx
    doc = Document(docxFile)
    
    # Собираем текст из всех параграфов в одну переменную
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    
    # Записываем текст в файл .txt
    with open(txtFile, 'w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(fullText))

docxFile = 'test.docx'  # Здесь укажем путь к файлу .docx
txtFile = 'output.txt'  # Здесь укажем путь к файлу .docx

docx_to_txt(docxFile, txtFile)
