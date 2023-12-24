from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import LoanGroup, User, GroupAdmin, Loan, LoanRepayment
from datetime import datetime, timedelta



# @receiver(post_save, sender=User)
# def create_group_for_user(sender, instance,**kwargs):
#         if instance.user_role == 'group_admin':
#             admin, created = GroupAdmin.objects.get_or_create(user=instance)
#             if not LoanGroup.objects.filter(admin_id=admin.id).exists():
#                 LoanGroup.objects.create(name=f'{instance.username} group' ,admin=admin)  




# #for each loan created,create loan repayment objects with monthly payments from the date created to the due date
# @receiver(post_save, sender=Loan)
# def create_loan_repayments(sender, instance, created, **kwargs):
#     if created:
#         loan_start_date = instance.date_assigned
#         due_date = instance.due_date

#         while loan_start_date < due_date:
#             early_repayment_date = loan_start_date
#             date = loan_start_date + timedelta(days=30)  # Assuming monthly payments
#             LoanRepayment.objects.create(
#                 loan=instance,
#                 early_repayment_date = early_repayment_date,
#                 repayment_date=date,
#                 payment_status="awaiting"  # You can set an initial payment status
#             )
#             loan_start_date = date
