import json
import requests
import base64
from .models import Check
from django.template.loader import render_to_string
from task.settings import app as celery_app


def create_html_template(check_id, check_type, context):
    
    html = render_to_string('base/base.html', context)
    path = f'printer/templates/{check_id}_{check_type}.html'
    with open(path, 'w') as f:
        f.write(html)
    return path

@celery_app.task
def html_to_pdf(context):
    path = create_html_template(context.get('check_id'), context.get('check_type'), context)
    with open(path, 'r') as html_file:
        html_contents = html_file.read()

    encoded_html = base64.b64encode(html_contents.encode()).decode()
    

    url = 'http://localhost:8080'
    data = {
        'contents': encoded_html,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        pdf_file_name = f'{context.get("check_id")}_{context.get("check_type")}.pdf'
        with open(f'printer/media/pdf/{pdf_file_name}', 'wb') as pdf_file:
            pdf_file.write(response.content)
    else:
        print(f'Помилка під час створення PDF: {response.status_code} - {response.text}')
    
    with open(f'printer/media/pdf/{pdf_file_name}', 'rb') as f:
        file_data = f.read()
        context.get('check_obj').pdf_file.save(f'printer/media/pdf/{pdf_file_name}', f)