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


            break_start = (
                datetime.combine(date.today(), availability.break_start)
                if availability.break_start else None
            )

            break_end = (
                datetime.combine(date.today(), availability.break_end)
                if availability.break_end else None
            )

            while start_time < end_time:
                if break_start and break_end:
                    current_start = datetime.combine(date.today(), start_time)
                    if break_start <= current_start < break_end:
                        start_time = break_end.time()
                        continue

                formatted = f'TKN0{tkn}'
                token, created = Token.objects.get_or_create(
                    doctor=availability.doctor,
                    departemnt=availability.doctor.department, 
                    appointment_date=current_date,
                    token_number=formatted,
                    defaults={
                        "start_time": start_time,
                        "end_time": (
                            (datetime.combine(date.today(), start_time) + timedelta(minutes=duration)).time()
                        ),
                        "is_booked": False,
                        "is_canceled": False,
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