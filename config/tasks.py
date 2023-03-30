from celery import Celery

app = Celery('social', broker='redis://0.0.0.0:6379')


@app.task
def add(x, y):
    return x + y
