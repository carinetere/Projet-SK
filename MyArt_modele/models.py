from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     preferred_language = models.CharField(max_length=10, choices=[('fr', 'Français'), ('en', 'English'), ('es', 'Español')], default='fr')
#     newsletter = models.BooleanField(default=True)
#     promo_emails = models.BooleanField(default=True)
#     order_updates = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username}'s profile"

#     class Meta:
#         verbose_name = "Profil"
#         verbose_name_plural = "Profils"
    

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#                 Profile.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()

class Color(models.Model):
    # id_color = models.models.CharField(, max_length=50, primary_key = True)
    name_color = models.CharField(max_length=50)
    def __str__(self):
        return self.name_color

class Categorie(models.Model):
    name_categorie = models.CharField(max_length=50)
    description_categorie = models.TextField()
    def __str__(self):
        return self.name_categorie        

class Artist(models.Model):
    name_artist = models.CharField(max_length=50)
    description_artist = models.TextField()
    contact_artist = models.CharField(max_length=50)
    def __str__(self):
        return self.name_artist

class Product(models.Model):
    id_product = models.CharField(max_length=30, primary_key = True)
    image = models.ImageField(upload_to='artworks/', null=True)
    name_product = models.CharField(max_length=30)
    descrption_product = models.TextField()
    price_product = models.DecimalField(max_digits=8, decimal_places=2)
    rate_product = models.DecimalField(max_digits=5, decimal_places=2)
    color_product = models.ForeignKey(Color, on_delete=models.CASCADE)
    state_product = models.CharField(max_length=50)
    categorie_product = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    artiste_product = models.ForeignKey(Artist, on_delete=models.CASCADE)
    reduction_product = models.DecimalField(max_digits=5, decimal_places=2, null = True)
    def __str__(self):
        return self.name_product

    
class Cart(models.Model):
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_cart = models.DecimalField(max_digits=8, decimal_places=2)
    user_cart = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "cart")
    def __str__(self):
        return self.id

class CartItem(models.Model):
    product_cartitem = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_cartitem = models.SmallIntegerField(default = 0)
    cart_cartitem = models.ForeignKey(Cart, on_delete=models.CASCADE)
    def __str__(self):
        return self.id

class Reviews(models.Model):
    # user_review = models.ForeignKey(User, on_delete=models.CASCADE)
    product_review = models.ForeignKey(Product, on_delete=models.CASCADE)
    fullname_review = models.CharField(max_length=50)
    email_review = models.CharField(max_length=50)
    message_review = models.TextField()
    rate_review = models.SmallIntegerField(default = 0)
    created_at = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return f'{self.fullname_review} {self.product_review} {self.id}'


    
    

    
    
    