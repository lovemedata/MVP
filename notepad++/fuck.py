import random
import os
import fitz  # PyMuPDF

COMPUTER_DESK = os.path.join('C:\\', 'Users', 'admin', 'Desktop')
NOTEBOOK_DESK = os.path.join('C:\\', 'Users', 'jerry', 'OneDrive', '桌面')
EXERCISE = os.path.join('structure', 'Server', 'non_cust', 'exercise')

COMPUTER_EXERCISE_PATH = os.path.join(COMPUTER_DESK, EXERCISE)
NOTEBOOK_EXERCISE_PATH = os.path.join(NOTEBOOK_DESK, EXERCISE)


def total_images_from_pdf(pdf_file_path):
    pdf_document = fitz.open(pdf_file_path)
    image_number = len(pdf_document.get_page_images(0))
        
    pdf_document.close()
    return image_number

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
            print(selected_pages)
    else:
        for difficulty, count in [('easy', 4), ('medium', 4), ('med_up', 2), ('hard', 2)]:
            selected_pages[difficulty] = random.sample(range(1, total_images[difficulty] + 1), count)
    
    extracted_images = {}
    for difficulty, file_path in pool_files.items():
        pdf_document = fitz.open(file_path)
        images = []
        for page_num in selected_pages[difficulty]:
            print(page_num-1)
            page = pdf_document[page_num - 1]
            '''for img in page.get_images(full=True):                        就是
                xref = img[0]                                                這裡                
                base_image = pdf_document.extract_image(xref)               出問題 
                images.append(base_image['image'])'''
        extracted_images[difficulty] = images
        pdf_document.close()

    return extracted_images

# Function to create the 'exam' PDF file
def create_pdf(images, output_file_path):
    c = fitz.open()
    for image in images:
        c.new_page(width=image.width, height=image.height)
        c.insert_image((0, 0), image)
    c.save(output_file_path)

# Create the 'exam' PDF file
extracted_images = select_questions_from_pool('calculus', one_button=True)
one_button_path = os.path.join(NOTEBOOK_EXERCISE_PATH, 'calculus', 'one_button', 'exam.pdf')
create_pdf([fitz.'''ImageStream'''(img) for img_list in extracted_images.values() for img in img_list], one_button_path)
print('一鍵生成試題創建成功')
