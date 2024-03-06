import fitz
import random
import os

COMPUTER_DESK = os.path.join('C:\\', 'Users', 'admin', 'Desktop')
NOTEBOOK_DESK = os.path.join('C:\\', 'Users', 'jerry', 'OneDrive', '桌面')
EXERCISE = os.path.join('structure', 'Server', 'non_cust', 'exercise')

COMPUTER_EXERCISE_PATH = os.path.join(COMPUTER_DESK, EXERCISE)
NOTEBOOK_EXERCISE_PATH = os.path.join(NOTEBOOK_DESK, EXERCISE)
easy_path = os.path.join('calculus', 'pool', 'easy.pdf')
medium_path = os.path.join('calculus', 'pool', 'medium.pdf')
med_up_path = os.path.join('calculus', 'pool', 'med_up.pdf')
hard_path = os.path.join('calculus', 'pool', 'hard.pdf')

# Define the file paths for the PDF files
pdf_files = {
    'easy': os.path.join(NOTEBOOK_EXERCISE_PATH, easy_path),
    'medium': os.path.join(NOTEBOOK_EXERCISE_PATH, medium_path),
    'med_up': os.path.join(NOTEBOOK_EXERCISE_PATH, med_up_path),
    'hard': os.path.join(NOTEBOOK_EXERCISE_PATH, hard_path)
}

# Initialize a new PDF document for the exam
exam_doc = fitz.open()

# Loop through the selection criteria and randomly select pages from each file
selection_criteria = {
    'easy': 3,
    'medium': 4,
    'med_up': 2,
    'hard': 1
}

for difficulty, num_pages in selection_criteria.items():
    pdf_path = pdf_files[difficulty]
    doc = fitz.open(pdf_path)
    for _ in range(num_pages):
        page_num = random.randint(0, doc.page_count - 1)
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        exam_page = exam_doc.new_page(width=pix.width, height=pix.height)
        exam_page.insert_image((0, 0, pix.width, pix.height), pixmap=pix)
    doc.close()

# Save the exam document to a new PDF file
exam_doc_path = r'C:\Users\jerry\OneDrive\桌面\structure\Server\non_cust\exercise\calculus\one_button\exam.pdf'
exam_doc.save(exam_doc_path)
exam_doc.close()