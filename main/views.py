from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterUserForm, CategoryForm, RequestStatusAcceptWork
from .models import AdvUser, Applic, Category
from django.views.generic import TemplateView
from .forms import ApplicForm, AIFormSet
from django.shortcuts import redirect

def index(request):
    count = Applic.objects.filter(status='Принято в работу').count()
    bbs = Applic.objects.filter(status='Выполнено').order_by('-data')[:4]
    return render(request, 'main/index.html', {'bbs': bbs, 'count': count})



def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
   template_name = 'main/login.html'


@login_required
def profile(request):
    status = request.GET.get('status', '')
    current_user = request.user
    bbs = Applic.objects.filter(user=current_user)
    context = {'status': status, 'bbs': bbs}
    return render(request, 'main/profile.html', context)

@login_required
def profile_applic_add(request):
    if request.method == 'POST':
        form = ApplicForm(request.POST, request.FILES)
        if form.is_valid():
            Applic = form.save(commit=False)
            Applic.user=request.user
            Applic.save()
            messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
            return redirect('main:profile')
    else:
       form = ApplicForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'main/profile_applic_add.html', context)



class DeleteAppliView(LoginRequiredMixin, DeleteView):
   model = Applic
   template_name = 'main/profile_applic_delete.html'
   success_url = reverse_lazy('main:index')

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/profile.html'


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Create User object
            AdvUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                sur_name=form.cleaned_data['sur_name'],
                n_name=form.cleaned_data['n_name'],
                pat_mic=form.cleaned_data['pat_mic'],
            )
            messages.success(request, 'Registration successful.')
            return render(request, 'main/profile.html')
    else:
        form = RegisterUserForm()
    return render(request, 'main/register_user.html', {'form': form})

# def profile_applic_delete(request, pk):
#    bb = get_object_or_404(Applic, pk=pk)
#    if not request.user.is_author(bb):
#        return redirect('main:profile')
#    if request.method == 'POST':
#        bb.delete()
#        messages.add_message(request, messages.SUCCESS,
#                             'Объявление удалено')
#        return redirect('main:profile')
#    else:
#        context = {'bb': bb}
#        return render(request, 'main/profile_applic_delete.html', context)


class BBLogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'main/logout.html'

def my_requests(request):
    requests = Applic.objects.filter(username=request.user)
    return render(request, 'main/profile_applic_add.html', {'requests': requests})

def admin_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Категория добавлена')
            return redirect('main:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form': form})

def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'admin/category_list.html', {'category_list': category_list})


class AdminCategoryDelete(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'id'
    model = Category
    template_name = 'admin/admin_category_delete.html'
    success_url = reverse_lazy('main:category_list')

# def change_status(request):

def request_all(request):
    reque = Applic.objects.all()
    return render(request, 'admin/request_all.html', {'reque': reque})


class ChangeStatusAcceptWork(View):
    def get(self, request, id):
        design_request = Applic.objects.get(id=id)
        form = RequestStatusAcceptWork(instance=design_request)
        return render(request, 'admin/change_status_accept_work.html', {'form': form})

    def post(self, request, id):
        design_request = Applic.objects.get(id=id)
        form = RequestStatusAcceptWork(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            design_request.status = 'Принято в работу'
            design_request.comment = form.cleaned_data['comment']
            form.save()
            return redirect('main:request_all')
        return render(request, 'admin/change_status_accept_work.html', {'form': form})



class ChangeStatusCompleted(View):
    def get(self, request, id):
        design_request = Applic.objects.get(id=id)
        form = ChangeStatusCompleted(instance=design_request)
        return render(request, 'admin/change_status_completed.html', {'form': form})

    def post(self, request, id):
        design_request = Applic.objects.get(id=id)
        form = ChangeStatusCompleted(request.POST, instance=design_request)
        if form.is_valid():
            design_request.status = 'Выполнено'
            design_request.design_image = form.cleaned_data['image_design']
            form.save()
            return redirect('App:request_all')
        return render(request, 'admin/change_status_completed.html', {'form': form})