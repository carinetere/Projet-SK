from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MyArt_modele.models import Product, Categorie, Color, Reviews, Cart, CartItem, Product
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Avg

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def products(request):
    categorie_id = request.GET.get('categorie')
    list_categorie = Categorie.objects.all()
    
    if categorie_id:
        list_product = Product.objects.filter(categorie_product_id=categorie_id)
    else:
        list_product = Product.objects.all()

    list_color = Color.objects.all()
    paginator = Paginator(list_product, 6)  # 6 produits par page (tu peux changer)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    datas = {'page_obj': page_obj, 'list_categorie': list_categorie, 'list_color': list_color}
    return render(request, 'products.html', datas)

def product_detail(request, id_product):
    product = Product.objects.get(id_product = id_product)
    avg_rating = Reviews.objects.filter(product_review=product).aggregate(Avg('rate_review'))['rate_review__avg']
    if avg_rating is None:
        avg_rating = 0
    list_avis = Reviews.objects.filter(product_review = product)
    datas = {'product': product, 'avg_rating': avg_rating, 'list_avis': list_avis}
    return render(request, 'product-detail.html', datas)

def add_review(request, id_product):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        rate = request.POST.get('rate')  # On récupère le nombre d'étoiles

        product = Product.objects.get(id_product=id_product)
        Reviews.objects.create(
            product_review=product,
            fullname_review=fullname,
            email_review=email,
            message_review=message,
            rate_review=rate  # Enregistrement de la note
        )
        return redirect('product-detail', id_product=id_product)



def product_list(request):
    categorie_id = request.GET.get('categorie')
    list_categorie = Categorie.objects.all()
    
    if categorie_id:
        list_product = Product.objects.filter(categorie_product_id=categorie_id)
    else:
        list_product = Product.objects.all()
    list_color = Color.objects.all()
    paginator = Paginator(list_product, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    datas = {'page_obj': page_obj, 'list_categorie': list_categorie, 'list_color': list_color, }
    return render(request, 'product-list.html', datas)


@login_required
def cart(request):
    try:
        # Récupérer le panier de l'utilisateur connecté
        cart = Cart.objects.get(user_cart=request.user)
    except Cart.DoesNotExist:
        # Si le panier n'existe pas encore, on le crée
        cart = Cart.objects.create(
            total_price=Decimal('0.00'),
            discount_cart=Decimal('0.00'),
            user_cart=request.user
        )

    # Récupérer les éléments du panier
    cart_items = CartItem.objects.filter(cart_cartitem=cart)

    # Calculer le total du panier et la réduction
    total_price = sum(item.product_cartitem.price_product * item.quantity_cartitem for item in cart_items)
    discount_price = total_price * Decimal('0.10')  # Exemple de réduction de 10%

    # Passer les données dans le contexte
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_price': discount_price,
        'final_price': total_price - discount_price,
    }

    return render(request, 'cart.html', context)

def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart_cartitem__user_cart=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')  # Redirige vers la page du panier après la suppression

def checkout(request):
    return render(request, 'checkout.html')

def services(request):
    return render(request, 'services.html')

def work_detail(request):
    return render(request, 'work-detail.html')

def work(request):
    return render(request, 'work.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement l'utilisateur après l'inscription
            return redirect('index')  # Redirige vers la page d'accueil
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirige après connexion
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après déconnexion

@login_required
def add_to_cart(request, id_product):
    product = Product.objects.get(id_product=id_product)
    
    # Vérifier si l'utilisateur a déjà un panier
    cart, created = Cart.objects.get_or_create(user_cart=request.user)
    
    # Récupérer la quantité du produit
    quantity = int(request.POST.get('quantity', 1))  # Par défaut 1 si non spécifié
    
    # Vérifier si le produit est déjà dans le panier
    cart_item, created = CartItem.objects.get_or_create(cart_cartitem=cart, product_cartitem=product)
    
    # Si l'item est déjà dans le panier, on met à jour la quantité
    if not created:
        cart_item.quantity_cartitem += quantity
        cart_item.save()
    else:
        cart_item.quantity_cartitem = quantity
        cart_item.save()
    
    return redirect('cart')  # Rediriger vers la page du panier