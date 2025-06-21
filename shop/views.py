from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Category, Product, Manufacturer, Supplier, Order, OrderItem
from .forms import CategoryForm, ProductForm, ManufacturerForm, SupplierForm, RegisterForm, ContactForm
from .cart import Cart
from django.contrib.auth import login
from django.contrib import messages

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class HomeView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_create.html'
    success_url = reverse_lazy('shop:category_list')

class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_create.html'
    success_url = reverse_lazy('shop:category_list')

class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'shop/category_confirm_delete.html'
    success_url = reverse_lazy('shop:category_list')

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_create.html'
    success_url = reverse_lazy('shop:product_list')

class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_create.html'
    success_url = reverse_lazy('shop:product_list')

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('shop:product_list')

class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'shop/manufacturer_list.html'
    context_object_name = 'manufacturers'

class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'shop/manufacturer_detail.html'
    context_object_name = 'manufacturer'

class ManufacturerCreateView(StaffRequiredMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'shop/manufacturer_create.html'
    success_url = reverse_lazy('shop:manufacturer_list')

class ManufacturerUpdateView(StaffRequiredMixin, UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'shop/manufacturer_create.html'
    success_url = reverse_lazy('shop:manufacturer_list')

class ManufacturerDeleteView(StaffRequiredMixin, DeleteView):
    model = Manufacturer
    template_name = 'shop/manufacturer_confirm_delete.html'
    success_url = reverse_lazy('shop:manufacturer_list')

class SupplierListView(ListView):
    model = Supplier
    template_name = 'shop/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'shop/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(StaffRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shop/supplier_create.html'
    success_url = reverse_lazy('shop:supplier_list')

class SupplierUpdateView(StaffRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shop/supplier_create.html'
    success_url = reverse_lazy('shop:supplier_list')

class SupplierDeleteView(StaffRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'shop/supplier_confirm_delete.html'
    success_url = reverse_lazy('shop:supplier_list')

class CartView(LoginRequiredMixin, ListView):
    template_name = 'shop/cart_detail.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart(self.request)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Товар {product.name} добавлен в корзину.')
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Товар {product.name} удален из корзины.')
    return redirect('shop:cart_detail')

def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'Корзина пуста.')
        return redirect('shop:cart_detail')
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            order_number=f'ORD-{request.user.id}-{int(cart.get_total_price())}',
            total_amount=cart.get_total_price()
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        messages.success(request, f'Заказ #{order.order_number} успешно создан.')
        return redirect('shop:order_detail', pk=order.pk)
    return render(request, 'shop/order_create.html', {'cart': cart})

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class LoginView(LoginView):
    template_name = 'shop/login.html'
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    next_page = reverse_lazy('shop:home')

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('shop:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно.')
        return redirect(self.success_url)

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Пока выводим в консоль, для реальной отправки настройте email
            print(f"Имя: {form.cleaned_data['name']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Сообщение: {form.cleaned_data['message']}")
            messages.success(request, 'Сообщение отправлено!')
            return redirect('shop:contacts')
    else:
        form = ContactForm()
    return render(request, 'shop/contacts.html', {'form': form})