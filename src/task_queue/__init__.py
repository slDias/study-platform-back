from os import environ

from celery import Celery, Task

_redis_url = environ.get("REDIS_URL")
app = Celery("task_queue", backend=_redis_url, broker=_redis_url)

@app.task
def a_task():
    print("this is a task running")


if __name__ == "__main__":
    a_task.delay()
