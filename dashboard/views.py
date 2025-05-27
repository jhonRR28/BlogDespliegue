from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, UpdateView, DeleteView
from newsletter.models import Newsletter, NewsletterUser
from newsletter.forms import NewsletterCreationForm
from django.conf import settings
from django.core.mail import send_mail

# VIEWS FOR NEWSLETTER.
class DashboardHomeView(TemplateView):
    template_name = 'dashboard/index.html'

class NewslettersDashboardHomeView(View):
    def get(self, request, *args, **kwargs):
        newsletters = Newsletter.objects.all()
        context = {
            'newsletters':newsletters
        }
        return render(request, 'dashboard/list.html', context)
    
class NewsletterCreateView(View):
    def get(self, request, *args, **kwargs):
        form = NewsletterCreationForm()
        context = {
            'form':form
        }
        return render(request, 'dashboard/create.html', context)
    
    def post(self, request, *args, **kwargs):

        if request.method=="POST":
            form = NewsletterCreationForm(request.POST or None)
            if form.is_valid():
                instance = form.save()
                newsletter = Newsletter.objects.get(id=instance.id)
                if newsletter.status=="Publish":
                    subject = newsletter.subject
                    body = newsletter.body
                    from_email = settings.EMAIL_HOST_USER
                    for email in newsletter.email.all():
                        send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
                return redirect('dashboard:list')
        context = {
            'form':form
        }
        return render(request, 'dashboard/create.html', context)
    
class NewsletterDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        newsletter = get_object_or_404(Newsletter, pk=pk)
        context = {
            'newsletter' : newsletter
        }
        return render(request, 'dashboard/detail.html', context)
    
class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterCreationForm
    template_name = 'dashboard/update.html'
    success_url = 'dashboard/detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        newsletter = get_object_or_404(Newsletter, pk=pk)

        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            instance = form.save()
            if instance.status == "Published":
                subject = instance.subject
                body = instance.body
                from_email = settings.EMAIL_HOST_USER
                for email in instance.email.all():
                    send_mail(
                        subject=subject,
                        from_email=from_email,
                        recipient_list=[email],
                        message=body,
                        fail_silently=True
                    )
            return redirect('dashboard:detail', pk=instance.id)
        
        context = {
            'form': form
        }
        return render(request, 'dashboard/update.html', context)

    
class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'dashboard/delete.html'
    success_url = '/dashboard/list/'


# VIEWS FOR NEWSLETTERUSER.
class NewsletterUserListView(View):
    def get(self, request, *args, **kwargs):
        users = NewsletterUser.objects.all()
        context = {
            'users':users
        }
        return render(request, 'dashboard/list-user.html', context)
    