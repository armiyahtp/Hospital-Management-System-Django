from django.shortcuts import render
from datetime import datetime, date, timedelta

from hospital.models import DoctorAvailability, Token




def generate_token(availability):
    today = date.today()
    end_date = today + timedelta(weeks=1)
    created_tokens = []

    current_date = today + timedelta(days=1)
    while current_date <= end_date:
        if current_date.weekday() == availability.weekday:
            start_time = availability.start_time
            end_time = availability.end_time
            duration = availability.consult_duration
            tkn = 1


            lunch_start = (
                datetime.combine(date.today(), availability.lunch_start)
                if availability.lunch_start else None
            )

            lunch_end = (
                datetime.combine(date.today(), availability.lunch_end)
                if availability.lunch_end else None
            )

            while start_time < end_time:
                if lunch_start and lunch_end:
                    current_start = datetime.combine(date.today(), start_time)
                    if lunch_start <= current_start < lunch_end:
                        start_time = lunch_end.time()
                        continue

                formatted = f'TKN0{tkn}'
                token, created = Token.objects.get_or_create(
                    doctor=availability.doctor,
                    appointment_date=current_date,
                    token_number=formatted,
                    defaults={
                        "start_time": start_time,
                        "end_time": (
                            (datetime.combine(date.today(), start_time) + timedelta(minutes=duration)).time()
                        )
                    }
                )
                if created:
                    created_tokens.append(token.id)
                start_time = (
                    datetime.combine(date.today(), start_time) + timedelta(minutes=duration)
                ).time()
                tkn += 1
        current_date += timedelta(days=1)
    return created_tokens