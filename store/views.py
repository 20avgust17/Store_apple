from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .forms import UserProfileForm, ContactForm
from .models import Product, Category, Basket, Contact
from django.views.generic.edit import CreateView, UpdateView
from .tasks import send_spam_email


class ProductByCategory(ListView):
    paginate_by = 1
    models = Category
    template_name = 'store/product_by_category.html'
    context_object_name = 'product_by_category'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductByCategory, self).get_context_data(**kwargs)
        context['title'] = 'Товар по категориям'
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class ProductDetail(DetailView):
    models = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'item_product'

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробности о товаре'
        context['new_products'] = Product.objects.all().order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['new_products'] = Product.objects.all().order_by('-created_at')[:3]
        return context


class GetIndex(ListView):
    models = Product
    template_name = 'store/index.html'
    success_url = '/'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()[:3]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Apple Store'
        context['new_products'] = Product.objects.all().order_by('-created_at')[:5]
        context['top_rating_products'] = Product.objects.all()[:5]  # дописать order_by, когда будет сделан рейтинг
        context['top_like_products'] = Product.objects.all()[:3]
        context['top_price_products'] = Product.objects.all().order_by('-price')[:3]
        context['top_presence_product'] = Product.objects.filter(presence=True)[:3]
        context['categories'] = Category.objects.all()
        return context


class Search(ListView):
    paginate_by = 9
    template_name = 'store/product_by_category.html'
    context_object_name = 'product_by_category'

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f'{self.request.GET.get("q")}&'
        context['all_category'] = Category.objects.all()
        context['categories'] = Category.objects.all()
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'store/profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_superuser:
            qs = qs.filter(pk=self.request.user.pk)
        return qs


class SendSpam(CreateView):
    models = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'store/send_spam.html'

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
