from SheepFish_test_task.celery import app


@app.task
def render_pdj_kitchen(data):
    pass


@app.task
def render_pdf_client(data):
    pass
