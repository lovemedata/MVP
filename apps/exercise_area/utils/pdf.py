import random
import os
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

COMPUTER_DESK = os.path.join('C:\\', 'Users', 'admin', 'Desktop')
NOTEBOOK_DESK = os.path.join('C:\\', 'Users', 'jerry', 'OneDrive', '桌面')
EXERCISE = os.path.join('structure', 'Server', 'non_cust', 'exercise')

COMPUTER_EXERCISE_PATH = os.path.join(COMPUTER_DESK, EXERCISE)
NOTEBOOK_EXERCISE_PATH = os.path.join(NOTEBOOK_DESK, EXERCISE)

def total_images_from_pdf(pdf_file_path):
    pdf = PdfReader(pdf_file_path)
    images_count = 0
    '''for page_num in range(len(pdf.pages)):
        print(pdf.pages[page_num]['/Resources']['/XObject'].get_object()) # 在這種一頁只包含一張圖的pdf結構之下, 這一行指令不管在哪一頁都會獲取到pdf檔所有的內容, 而不是只獲取到那一頁的而已(即page_num不影響獲取的內容), 但感覺有用到頁碼的index來選取, 所以理論上要相關才對, 為避免以後改版修正這個問題, 所以原始的code也先保留在這註解起來, 下面的是修改成現在(2024/3/4)這個時間點會得到想要的結果的.
        for obj in pdf.pages[page_num]['/Resources']['/XObject'].get_object():
            if pdf.pages[page_num]['/Resources']['/XObject'].get_object()[obj]['/Subtype'] == '/Image':
                # 現在每一頁都只有放一張圖片, 而這個判斷式"感覺"是只要pdf檔只有圖片就可以不用判斷, 但不是很確定所以就先保留.
                images_count += 1
    print(images_count) # 答案是平方, 也就是代表每一張圖片都循環了頁碼的次數, 但一張圖片只需要循環一次'''
       
    # print(pdf.pages[1]['/Resources']['/XObject'].get_object())
    for obj in pdf.pages[1]['/Resources']['/XObject'].get_object():
        if pdf.pages[1]['/Resources']['/XObject'].get_object()[obj]['/Subtype'] == '/Image':
            # 現在每一頁都只有放一張圖片, 而這個判斷式"感覺"是只要pdf檔只有圖片就可以不用判斷, 但不是很確定所以就先保留.
            images_count += 1
    # print(images_count)
    return images_count


def select_questions_from_pool(subject, one_button=True):
    ''' subject: 不同科目不同路徑
        one_button: 一鍵生成的題數與定期產生的題目數量不一樣, 預設是一鍵生成
    '''
    
    easy_path = os.path.join(subject, 'pool', 'easy.pdf')
    medium_path = os.path.join(subject, 'pool', 'medium.pdf')
    med_up_path = os.path.join(subject, 'pool', 'med_up.pdf')
    hard_path = os.path.join(subject, 'pool', 'hard.pdf')
    
    # Paths to the pool PDF files
    pool_files = {
        'easy': os.path.join(NOTEBOOK_EXERCISE_PATH, easy_path),
        'medium': os.path.join(NOTEBOOK_EXERCISE_PATH, medium_path),
        'med_up': os.path.join(NOTEBOOK_EXERCISE_PATH, med_up_path),
        'hard': os.path.join(NOTEBOOK_EXERCISE_PATH, hard_path)
    }

    # Get the total number of images in each PDF file
    total_images = {}
    for difficulty, file_path in pool_files.items():
        pdf = PdfReader(file_path)
        total_images[difficulty] = total_images_from_pdf(file_path)

    # Select pages(images) randomly based on the total number of pages(images) in each file
    selected_pages = {} # 現在一頁只放一張圖片, 而一張圖片也只放一道題, 所以頁碼與題目與圖片數量目前是等價的
    if one_button:
        for difficulty, count in [('easy', 3), ('medium', 4), ('med_up', 2), ('hard', 1)]:
            selected_pages[difficulty] = random.sample(range(1, total_images[difficulty] + 1), count)
            # print(selected_pages)
    else:
        for difficulty, count in [('easy', 4), ('medium', 4), ('med_up', 2), ('hard', 2)]:
            selected_pages[difficulty] = random.sample(range(1, total_images[difficulty] + 1), count)
    
    # Load only the selected pages(images)
    extracted_images = {}
    for difficulty, file_path in pool_files.items():
        pdf = PdfReader(file_path)
        images = []
        for page_num in selected_pages[difficulty]:
            # print(page_num-1)
            page = pdf.pages[page_num-1]
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj]._data
                    images.append((size, data))
        extracted_images[difficulty] = images

    return extracted_images

# Function to create the 'exam' PDF file
def create_pdf(images, output_file_path):
    c = canvas.Canvas(output_file_path, pagesize=letter)
    y_position = 10.5 * inch
    for image in images:
        c.drawImage(image, 1 * inch, y_position, width=6*inch, height=4*inch)
        y_position -= 5 * inch
        if y_position < 1 * inch:
            c.showPage()
            y_position = 10.5 * inch
    c.save()

# Create the 'exam' PDF file
extracted_images = select_questions_from_pool('calculus', one_button=True)
print(extracted_images['easy'][0])
    # 一鍵生成的試題
one_button_path = os.path.join(NOTEBOOK_EXERCISE_PATH, 'calculus', 'one_button', 'exam.pdf')
create_pdf([img for img_list in extracted_images.values() for img in img_list], one_button_path)
print('一鍵生成試題創建成功')
'''elif total_images == 12:
    # 定期生成的試題
    create_pdf([img for img_list in extracted_images.values() for img in img_list], 'present/此期日期/exam.pdf')
    print('定期生成試題創建成功')
else:
    print('發生錯誤')'''