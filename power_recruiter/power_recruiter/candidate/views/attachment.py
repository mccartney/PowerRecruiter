from power_recruiter.candidate.models import Attachment
from django.shortcuts import redirect

def attachment(request, id):
    att = Attachment.objects.get(pk=id)
    return redirect(att.file.url)