import subprocess
from celery import Celery
from django.shortcuts import render
from django.conf import settings
import pandas as pd
import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app = Celery('tasks', broker=settings.RABBITMQ_URL)


def home(request):

    if request.method == "POST":
        read_data.delay()

    return render(request, "home.html")


@app.task
def read_data():
    nrows = 10000
    chunks = []
    i_chunk = 0
    skiprows = 1
    total_items = 0

    file = 'bancapp_1.xlsx'
    print(timezone.now())

    df_header = pd.read_excel(file, nrows=1)

    while True:
        df_chunk = pd.read_excel(file, nrows=nrows, skiprows=skiprows, header=None)
        skiprows += nrows

        if not df_chunk.shape[0]:
            break
        else:
            total_items += df_chunk.shape[0]
            print(f"  - chunk {i_chunk} ({df_chunk.shape[0]} rows)")
            chunks.append(df_chunk)
        i_chunk += 1

    df_chunks = pd.concat(chunks)

    columns = {i: col for i, col in enumerate(df_header.columns.tolist())}
    df_chunks.rename(columns=columns, inplace=True)
    df = pd.concat([df_header, df_chunks])

    total_amount = df.get('Amount in Local Currency').sum()

    with open('puppeteer.html', 'w') as f:
        f.write(f"<b>Total Items:</b>{total_items}<br>")
        f.write(f"<b>Total Amount:</b>{total_amount}")
    f.close()

    execute(
        settings.NODE_PATH,
        settings.PUPPETEER_PDF_JS,
        settings.PUPPETEER_TEMPLATE,
        settings.OUTPUT_PUPPETEER_PDF
    )

    print(timezone.now())


def execute(*args):
    subprocess.run(list(args), timeout=180)