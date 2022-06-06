import factory
from store.products.models import ProductCategory, Product, ProductImage


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = "Product Category"
    slug = "product-category"
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    categories = factory.SubFactory(ProductCategoryFactory)
    title = "Product"
    short_description = "Product Short Description"
    description = "Product Description"
    additional_information = "Product - Additional Description"
    slug = "product"
    regular_price = 60
    discount_price = 50
    stocks = 10
    sale_tag = "SALE"
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(color="green")
