from celery import shared_task

from rentals.models import Rental


@shared_task
def calculate_rental_post(rental_id):
    rental = Rental.objects.get(id=rental_id)
    if rental.end_time is None:
        return

    duration = (rental.end_time - rental.start_time).total_seconds() / 3600
    rental.cost = duration * 5
    rental.save()