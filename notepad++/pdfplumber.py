import random
import os
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# Define paths
COMPUTER_DESK = os.path.join('C:\\', 'Users', 'admin', 'Desktop')
NOTEBOOK_DESK = os.path.join('C:\\', 'Users', 'jerry', 'OneDrive', '桌面')
EXERCISE = os.path.join('structure', 'Server', 'non_cust', 'exercise')

COMPUTER_EXERCISE_PATH = os.path.join(COMPUTER_DESK, EXERCISE)
NOTEBOOK_EXERCISE_PATH = os.path.join(NOTEBOOK_DESK, EXERCISE)

def total_images_from_pdf(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        return sum(len(page.images) for page in pdf.pages)

def select_questions_from_pool(subject, one_button=True):
    easy_path = os.path.join(subject, 'pool', 'easy.pdf')
    medium_path = os.path.join(subject, 'pool', 'medium.pdf')
    med_up_path = os.path.join(subject, 'pool', 'med_up.pdf')
    hard_path = os.path.join(subject, 'pool', 'hard.pdf')

    pool_files = {
        'easy': os.path.join(NOTEBOOK_EXERCISE_PATH, easy_path),
        'medium': os.path.join(NOTEBOOK_EXERCISE_PATH, medium_path),
        'med_up': os.path.join(NOTEBOOK_EXERCISE_PATH, med_up_path),
        'hard': os.path.join(NOTEBOOK_EXERCISE_PATH, hard_path)
    }

    total_images = {}
    for difficulty, file_path in pool_files.items():
        total_images[difficulty] = total_images_from_pdf(file_path)

    selected_pages = {}
    if one_button:
        for difficulty, count in [('easy', 3), ('medium', 4), ('med_up', 2), ('hard', 1)]:
            selected_pages[difficulty] = random.sample(range(1, total_images[difficulty] + 1), count)
    else:
        for difficulty, count in [('easy', 4), ('medium', 4), ('med_up', 2), ('hard', 2)]:
            selected_pages[difficulty] = random.sample(range(1, total_images[difficulty] + 1), count)

    extracted_images = {}
    for difficulty, file_path in pool_files.items():
        images = []
        with pdfplumber.open(file_path) as pdf:
            for page_num in selected_pages[difficulty]:
                page = pdf.pages[page_num - 1]
                for img in page.images:
                    images.append(img['stream'].get('data'))
        extracted_images[difficulty] = images

    return extracted_images

def create_pdf(images, output_file_path):
    c = canvas.Canvas(output_file_path, pagesize=letter)
    y_position = 9.5 * inch
    for data in images:
        image_path = os.path.join(NOTEBOOK_DESK, 'temp_image.png')
        with open(image_path, 'wb') as f:
            f.write(data)
        c.drawImage(image_path, 1 * inch, y_position,)
        os.remove(image_path)
        y_position -= 5 * inch
        if y_position < 1 * inch:
            c.showPage()
            y_position = 9.5 * inch
    c.save()

# Create the 'exam' PDF file
extracted_images = select_questions_from_pool('calculus', one_button=True)
create_pdf([img for img_list in extracted_images.values() for img in img_list], 'exam1.pdf')
print('一鍵生成試題創建成功')
