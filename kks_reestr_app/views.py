import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, login

from .models import KksCodeModel, KksObjectModel

from .forms import KksCodeForm


class IndexView(View):
    def get(self, request):
        # kks_form = KksCodeForm()
        objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True)
        content = {'objects': objects}
        # content = {'kks_form': kks_form}
        return render(request, 'kks_reestr_app/index.html', content)

    def post(self, request):
        kks_form = KksCodeForm(request.POST)
        print(request.POST)
        # print(kks_form)
        return redirect('index')


def get_object_view(request):
    """Функция получения списка объектов"""


