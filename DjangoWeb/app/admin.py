from django.contrib import admin
from app.models import Product, ProductGrade, ProductInstance,Result,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.template.loader import get_template
from datetime import datetime
from multiprocessing import Pool

admin.site.unregister(User)

def send_email (request, user):
    print(user.username)
    html_message = get_template('app/email.html')
    html_message = html_message.render({
            'name':user.username,
            'email':user.email,
            'time':datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
            'url':request.build_absolute_uri('/confirmation/' + str(user.id) + '/')
        })
    send_mail('Подтверждение почты', html_message, 'i.surikov@outlook.com',[ str(user.email) ],fail_silently=False, html_message = html_message)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    actions = [ 'send_emails_async' ]

    def send_emails_async(self, request, queryset):
        letters_counter = 0
        args = []
        for user in queryset:
            if user.profile.verified == True:
                continue
            letters_counter += 1
            args.append((user,request))
        with Pool(processes=letters_counter) as pool:
            pool.starmap(send_email, args)
        self.message_user(request, "количество успешно отправленных писем: {0}".format(letters_number))

    send_emails_async.short_description = "Отправить письмо для подтверждения"
    

    #def send_email (self, request, queryset):
    #    letters_number = 0
    #    for i in queryset:
    #        if i.profile.verified == True:
    #            continue
    #        html_message = get_template('app/email.html')
    #        html_message = html_message.render({
    #                'name':i.username,
    #                'email':i.email,
    #                'time':datetime.today().strftime("%Y-%m-%d-%H.%M.%S"),
    #                'url':request.build_absolute_uri('/confirmation/' + str(i.id) + '/')
    #            })
    #        letters_number += send_mail('Django mail', html_message, 'i.surikov@outlook.com',[ str(i.email) ],fail_silently=False, html_message = html_message)
    #    self.message_user(request, "количество успешно отправленных писем: {0}".format(letters_number))
            


admin.site.register(Product)
admin.site.register(ProductGrade)
admin.site.register(ProductInstance)
admin.site.register(Result)
admin.site.register(Profile)





