from django.urls import reverse
from django.views.generic import CreateView

from contacts.forms import ContactModelForm


class ContactCreateView(CreateView):
    template_name = 'contact.html'
    form_class = ContactModelForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("contacts:contact")
