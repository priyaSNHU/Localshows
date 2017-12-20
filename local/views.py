from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import ContactForm

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string


@login_required(login_url="login/")
def index(request):
    return render(request, 'local/home.html')

#def contact(request):
 #   return render(request, 'local/basic.html',  {'content':['If you would like to contact me, please email me','xyz@hookset.com']})

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the 
            # contact information
            
            template = get_template('local/contact_template.txt')
            context = {
                        'contact_name': contact_name,
                        'contact_email': contact_email,
                        'form_content': form_content,
                    }

            content = template.render(context)
            

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

     

    
    return render(request, 'local/basic.html', {
        'form': form_class,
    })
