# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ManagerBoard.models import Document
from ManagerBoard.forms import DocumentForm
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if 'docfile' in request.FILES:
                newdoc = Document(docfile = request.FILES['docfile'], title = request.POST['title'], message = request.POST['message'], type = request.POST['type'], date = request.POST['date'], dateEnd = request.POST['dateEnd'])
                newdoc.save()
            else:
                newdoc = Document(title = request.POST['title'], message = request.POST['message'], type = request.POST['type'], date = request.POST['date'], dateEnd = request.POST['dateEnd'])
                newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('ManagerBoard.views.upload'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
def login(request):
    return render_to_response('login.html', dict(), RequestContext(request))

def document(request):
    documents = Document.objects.all().order_by('-date')
    return render_to_response('document.html', dict(documents = documents), RequestContext(request))