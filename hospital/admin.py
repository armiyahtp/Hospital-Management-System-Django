from django.contrib import admin
from .models import *



admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Room)
admin.site.register(DoctorsInHospital)
admin.site.register(DoctorAvailability)

admin.site.register(Token)
admin.site.register(Patient)
admin.site.register(Appointment)

admin.site.register(Prescription)
admin.site.register(PrescriptionItem)

admin.site.register(AppointmentBill)
admin.site.register(BillMedicineItem)
admin.site.register(BillTestItem)
admin.site.register(BillInjectionItem)
admin.site.register(BillIntravenousItem)
admin.site.register(BillRoomItem)
admin.site.register(BillSurgeryItem)
admin.site.register(BillNursingItem)
admin.site.register(BillMiscItem)
admin.site.register(Payment)

admin.site.register(Contact)