from celery import shared_task

@shared_task(bind=True)
def test_function(self):
    #operations
    return "Donen  "