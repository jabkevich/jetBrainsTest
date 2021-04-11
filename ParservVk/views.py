from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
# Create your views here.
from io import StringIO

from .Parser import get_wal, get_post

# 118445684
context = {
    'pars': '',
    'idwall': '',
    'value': '',
    'nameGroup': '',
    'comments': ''
}

idwall = 0


def home(request):
    global idwall
    if request.GET.get('print_btn'):
        context = {
            'pars': get_wal(int(request.GET.get('idwall'))),
            'idwall': int(request.GET.get('idwall')),
            'value': 'Button clicked',
            'nameGroup': str(request.GET.get('namewall'))
        }
        idwall = context['idwall']

    return render(request, 'parserVk/home.html', context)


def GraphicComments(plt):
    fig = plt
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    return imgdata.getvalue()




def postDetail(request, pk):
    context['comments'] = get_post(pk, idwall, plt)
    context['graph'] = GraphicComments(plt)
    return render(request, 'parserVk/post.html', context)
