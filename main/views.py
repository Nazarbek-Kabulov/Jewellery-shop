import json
import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DeleteView

from .form import ProductForm, CommentForm
from .utils import decrement_count, increment_count
from .models import Product, Shopping_cart, Picture, Comment


class HomeView(View):
    template_name = 'index.html'
    context = {}
    from_class = CommentForm

    def get(self, request):
        form = self.from_class()
        products = Product.objects.all()[:3]
        comments = Comment.objects.all()

        product_data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            product_data.append(product)
        self.context.update({'products': product_data, 'comments': comments, 'form': form})
        # protocol = 'https://' if request.is_secure() else 'http://'
        # url = protocol + request.META.get('HTTP_HOST') + reverse('product')
        # products = requests.get(url)
        # self.context.update({'products':products.json()['data']})
        return render(request, self.template_name, self.context)

    def post(self, request):
        comment_form = self.from_class(request.POST, request.FILES)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            phone = comment_form.cleaned_data['phone']
            message = comment_form.cleaned_data['message']

            comment = Comment.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            comment.save()
        return redirect('/')


class AboutView(View):
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactView(LoginRequiredMixin, View):
    template_name = 'contact.html'

    def get(self, request):
        comment = CommentForm()
        return render(request, self.template_name, {'comment': comment})

    def post(self, request):
        comment = CommentForm(request.POST)
        if comment.is_valid():
            name = comment.cleaned_data.get('name')
            email = comment.cleaned_data.get('email')
            phone = comment.cleaned_data.get('phone')
            message = comment.cleaned_data.get('message')

            msg = f'''
            
        {message}
    
    
    Full name: {name}
    email: {email}
    phone number: {phone}
    
    
                '''
            send_mail(
                'Yangi xabar',
                msg,
                name,
                ['nazarbekqobulov28@gmail.com']
            )
        return redirect('contact')


class ShoppingCartView(View):
    template_name = 'shop.html'
    context = {}

    def get(self, request):
        shopping_cart = Shopping_cart.objects.filter(user=request.user).values('product_id')
        products = Product.objects.filter(pk__in=shopping_cart)
        data = []
        for product in products:
            shop = Shopping_cart.objects.get(Q(user=request.user) & Q(product=product))
            image = Picture.objects.filter(product=product).first()
            product.count = shop.count
            product.image = image
            data.append(product)
        self.context.update({'products': data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        id = request.POST.get('id')
        user = request.user
        shopping_cart = Shopping_cart.objects.get(Q(product_id=id) & Q(user=user))
        shopping_cart.delete()
        return redirect('/shopping')


class IncrementCountView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = increment_count(id, request.user)
        return JsonResponse({'result': result})


class DecrementCountView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = decrement_count(id, request.user)
        return JsonResponse({'result': result})


class JewelleryView(View):
    template_name = 'jewellery.html'
    context = {}

    def get(self, request):
        products = Product.objects.all()
        product_data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            product_data.append(product)
        self.context.update({'products': product_data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        id = request.POST.get('id')
        user_id = request.user.id
        try:
            shopping_card, created = Shopping_cart.objects.get_or_create(
                product_id=id,
                user_id=user_id
            )
            if created:
                messages.info(request, 'Added successfully!')
            else:
                messages.warning(request, 'Already added!')
                return redirect('/shopping')
        except IntegrityError:
            messages.error(request, 'An error occurred while adding to the shopping cart.')
        return redirect('/jewellery')


class AddProductView(CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = ProductForm

    # fields = ('name', 'price', 'description')
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            author = request.user

            product = Product.objects.create(
                title=title,
                price=price,
                description=description,
                author=author
            )
            images = form.files.getlist('image')
            # print('images:', images)
            for image in images:
                picture = Picture.objects.create(
                    image=image,
                    product=product
                )
                picture.save()

            return redirect('/add-product')


class DeleteProductView(DeleteView):
    model = Product
    template_name = ''
    success_url = '/'


class ProductAPIView(View):

    def get(self, request):
        products = Product.objects.all()[:3]
        products_data = []
        for product in products:
            image = Product.objects.filter(product=product).first()
            product_dict = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'image': image.image.url,
                'author': product.author
            }
            products_data.append(product_dict)
        return JsonResponse({'data': products_data})


# class DetailView(View):
#     def get(self, request):
#         product_name = request.GET.get('title')
#         print(product_name)
#         product = get_object_or_404(Product, title=product_name)
#         return render(request, 'jewellery.html', {'product': product})
#

class ProductDetailView(View):
    template_name = 'detail.html'
    context = {}

    def get(self, request):
        products = Product.objects.all()
        product_data = []
        for product in products:
            image = Picture.objects.filter(product=product).first()
            product.image = image
            product_data.append(product)
        self.context.update({'products': product_data})

        return render(request, self.template_name, self.context)
