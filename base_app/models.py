from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    # The is another separate table for clients.

    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    first_name = models.CharField("Nombre(s)", max_length=200)
    last_name = models.CharField("Apellidos", max_length=200)
    phone_number = models.CharField(
        "Teléfono", max_length=15, unique=True, null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    pass

    class meta:
        pass

    objects = UserManager()

    def _str_(self):
        return self.email, self.first_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.total = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)
        self.order.total = sum(item.product.price * item.quantity for item in self.order.orderitem_set.all())
        self.order.save()
    
    def delete(self, *args, **kwargs):
        super(OrderItem, self).delete(*args, **kwargs)
        self.order.total = sum(item.product.price * item.quantity for item in self.order.orderitem_set.all())
        self.order.save()