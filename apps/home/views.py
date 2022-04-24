# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from apps.authentication.models import CustomUser, Company, Role
from apps.home import filters
# from apps.home.filters import ZakazFilter
from apps.home.forms import ZakazForm, ZakazUpdateForm, CompanyForm
from apps.home.models import Sklad, Tovar


@login_required(login_url="/login/")
def index(request):
    item = Sklad.objects.all()[:5]
    # print(item)
    context = {'segment': 'index', 'item': item}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@csrf_exempt
# @login_required(login_url="/login/")
def zakaz_create(request):
    list_zakaz = Sklad.objects.filter(accept=request.user, status='Ожидается')
    tovar = Tovar.objects.all()
    if request.method == 'POST':
        zakaz = ZakazForm(request.POST, request.FILES)
        if zakaz.is_valid():
            # print(zakaz.cleaned_data)
            # zakaz.cleaned_data["company"] = request.user.company
            zakaz.cleaned_data['accept'] = request.user
            zakaz.cleaned_data["status"] = 'Ожидается'
            zakaz.cleaned_data["user"] = request.user

            Sklad.objects.create(**zakaz.cleaned_data)
            # zakaz.save()
            return redirect('create-zakaz')
    else:
        zakaz = ZakazForm()
    return render(request, "home/page-blank.html",
                  {'zakaz': zakaz, 'list_zakaz': list_zakaz, 'tovar': tovar})


# @login_required(login_url="/login/")
class StudentListView(ListView):
    model = Sklad
    template_name = 'home/zakaz.html'
    context_object_name = 'list_zakaz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        print(context['user'])
        context['filter'] = filters.TeachersFilter(self.request.GET,
                                                   queryset=self.get_queryset())
        return context

    def get_queryset(self):

        if self.request.user.role == None or self.request.user.role == 'client':
            return Sklad.objects.filter(
                user=self.request.user
            )
                    # (
                # accept=self.request.user
            # )

        elif self.request.user.role == 'company':
            return Sklad.objects.filter(
                company=self.request.user.company
            )
        elif self.request.user.role == 'logist':
            return Sklad.objects.all()


class StudentDetailView(DetailView):
    template_name = 'home/check.html'
    model = Sklad
    context_object_name = 'check'

    def get_queryset(self):
        return Sklad.objects.filter(
            status='Доставлено'
        )


def clients(request):
    user = CustomUser.objects.all()
    clients = Company.objects.all()
    pos_zakaz = Sklad.objects.filter(accept=request.user)
    print(pos_zakaz)

    comp = Sklad.objects.values('company').annotate(com=Count('obiem'))
    compa = Sklad.objects.filter(company=request.user.company).values(
        'company').annotate(com=Count('obiem'))
    ml = zip(clients, comp)
    return render(request, 'home/admin-panel-clients.html',
                  {'ml': ml,
                   "pos_zakaz": pos_zakaz,
                   "compa": compa
                   })


def zakaz_admin(request):
    zakaz_all = Sklad.objects.all()
    zakaz_on = Sklad.objects.filter(status='Принято')
    zakaz_off = Sklad.objects.filter(status='Ожидается')

    return render(request, 'home/zakaz.html',
                  {"zakaz_all": zakaz_all, "zakaz_on": zakaz_on,
                   "zakaz_off": zakaz_off})


class TeacherListView(ListView):
    model = Sklad
    template_name = 'home/zakaz.html'
    context_object_name = 'adm_z'

    # def get(self, request, *args, **kwargs):
    #     if request.user.role == None:
    #         return Sklad.objects.filter(
    #             company=request.user.company
    #         )
    #     elif request.user.role == 'admin':
    #         return Sklad.objects.all()
    #     elif request.user.role == 'logist':
    #         return Sklad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['filter'] = filters.TeachersFilter(self.request.GET,
                                                   queryset=self.get_queryset())
        return context


@login_required(login_url="/login/")
def profile(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    # if user.company:
    #     company = Company.objects.get(pk=request.user.company.pk)
    #     context = {'profile': 'profile', "company": company}
    context = {'profile': 'profile'}

    if request.method == "POST":
        # print(request.POST)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        # if not company:
        #     company.name = request.POST.get('name')
        #     company.address = request.POST.get('address')
        #     company.save()
        # Company.objects.create(name=request.POST.get('name'),
        #                        address=request.POST.get('address'))

        user.save()
        request.user = user
        context["success"] = 'Данные успешно обновлены!!'

    html_template = loader.get_template('home/ui-badges.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def userAdd(request):
    if "logist" not in request.user.role.name:
        return redirect('home')
    context = {
        'segment': 'user-add',
        'form': {
            'username': {
                'input': '',
                'error': False,
                'text': ''
            },
            'first_name': {
                'input': '',
                'error': False,
                'text': ''
            },
            'last_name': {
                'input': '',
                'error': False,
                'text': ''
            },
            'email': {
                'input': '',
                'error': False,
                'text': ''
            },
            'company': {
                'input': '',
                'error': False,
                'text': ''
            },
            'password': {
                'error': False,
                'text': ''
            },
            'password1': {
                'error': False,
                'text': ''
            },
        }
    }
    html_template = loader.get_template('home/ui-button.html')
    user = request.user
    if request.method == "POST":
        # print(request.POST)
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        company = request.POST['company']
        role = Role.objects.filter(name='company').first()
        print()
        error = False
        if password == '':
            error = True
            context['form']['password']['error'] = True
            context['form']['password']['text'] = 'Пароль не могут быть пустым'
        elif len(str(password)) < 8:
            error = True
            context['form']['password']['error'] = True
            context['form']['password'][
                'text'] = 'Пароль должен быть не менее 8 символов'
        if request.POST['password'] != password1:
            error = True
            context['form']['password1']['error'] = True
            context['form']['password1'][
                'text'] = 'Пароли должны быть одинаковыми'
        if error:
            context['form']['username']['input'] = username
            context['form']['first_name']['input'] = first_name
            context['form']['last_name']['input'] = last_name
            context['form']['password']['input'] = password
        else:
            company = Company.objects.create(name=company, staff=True)
            user_new = CustomUser.objects.create(username=username,
                                                 email=email,
                                                 first_name=first_name,
                                                 last_name=last_name,
                                                 role=role, company=company,
                                                 )
            user_new.set_password(password)
            user_new.save()
            return redirect('home')
        return HttpResponse(html_template.render(context, request))

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def zakazDelete(request, pk):
    Sklad.objects.get(pk=pk).delete()
    return redirect('create-zakaz')


@login_required(login_url="/login/")
def companyDelete(request, pk):
    Company.objects.get(pk=pk).delete()
    return redirect('admin-clients')


@login_required(login_url="/login/")
def accept_zakaz(request, pk):
    sklad = Sklad.objects.get(pk=pk)
    sklad.status = 'Принято'
    sklad.save()

    return redirect('list-zakaz')


def verify_zakaz(request, pk):
    sklad = Sklad.objects.get(pk=pk)
    sklad.status = 'Доставлено'
    sklad.save()

    return redirect('list-zakaz')


@login_required(login_url="/login/")
def send_zakaz(request, pk):
    sklad = Sklad.objects.get(pk=pk)
    sklad.status = 'В_пути'
    sklad.save()
    return redirect('list-zakaz')


def create_Company(request):
    if request.method == 'POST':
        company = CompanyForm(request.POST, request.FILES)
        if company.is_valid():
            Company.objects.create(**company.cleaned_data)
            # zakaz.save()
            return redirect('admin-clients')
    else:
        company = ZakazForm()
    return render(request, "home/ui-forms.html",
                  {'company': company})


def list_tovar(request):
    tovar = Tovar.objects.all()

    return render(request, 'home/ui-collapse.html', {"tovar": tovar})
