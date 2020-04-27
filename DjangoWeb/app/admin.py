from django.contrib import admin
from app.models import Product, ProductGrade, ProductInstance,Result,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.template.loader import get_template
from datetime import datetime
from multiprocessing import Pool,Process

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    actions = [ 'send_email' ]
    
    def send_email (self, request, queryset):
        letters_number = 0
        for i in queryset:
            if i.profile.verified == True:
                continue
            html_message = get_template('app/email.html')
            html_message = html_message.render({
                    'name':i.username,
                    'email':i.email,
                    'time':datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
                    'url':request.build_absolute_uri('/confirmation/' + str(i.id) + '/')
                })
            letters_number += send_mail('Django mail', html_message, 'i.surikov@outlook.com',[ str(i.email) ],fail_silently=False, html_message = html_message)
        self.message_user(request, "количество успешно отправленных писем: {0}".format(letters_number))
            
    send_email.short_description = "Отправить письмо для подтверждения"



admin.site.register(Product)
admin.site.register(ProductGrade)
admin.site.register(ProductInstance)
admin.site.register(Result)
admin.site.register(Profile)





