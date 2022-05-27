import uuid

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    """
    Product category model to categorize products.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Slug for url"), max_length=250, unique=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)

        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_all_products(self) -> list[object]:
        products = self.products.all()

        return products

    def get_products_count(self) -> int:
        products_count = self.products.count()

        if products_count > 0 and products_count < 10:
            return f"0{products_count}"
        elif products_count > 10:
            return products_count
        return 0


class Product(models.Model):
    """
    Product model with product necessary fields.
    """

    SALE_TAGS = (("SALE", "SALE"), ("NEW", "NEW"), ("HOT", "HOT"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categories = models.ForeignKey(
        ProductCategory,
        verbose_name=_("Product Categories"),
        on_delete=models.RESTRICT,
        related_name="products",
    )
    title = models.CharField(
        verbose_name=_("Product Title"),
        help_text=_("Required"),
        max_length=200,
        db_index=True,
    )
    short_description = models.TextField(
        verbose_name=_("Short Description"), max_length=500, blank=True
    )
    description = models.TextField(
        verbose_name=_("Product Description"), help_text=_("Optional"), blank=True
    )
    additional_information = models.TextField(
        verbose_name=_("Additional Product Information"), blank=True
    )
    slug = models.SlugField(max_length=300, unique=True)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        max_digits=6,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        max_digits=6,
        decimal_places=2,
        blank=True,
    )
    stocks = models.IntegerField(verbose_name=_("Stocks"), default=0)
    sale_tag = models.CharField(
        verbose_name=_("Sale Tag"), max_length=10, choices=SALE_TAGS, blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def get_product_images(self):
        return self.product_images.all()

    def extract_additional_information(self) -> list[dict]:
        for line in self.additional_information.split("\n"):
            if line:
                name_value_tuples = line.strip().split("-")
                if len(name_value_tuples) == 2:
                    name, value = (
                        name_value_tuples[0].strip(),
                        name_value_tuples[1].strip(),
                    )
                    yield {"name": name, "value": value}
        return

    @property
    def get_first_product_img(self):
        return self.product_images.first().image

    @property
    def get_featured_img(self):
        for img in self.product_images.all():
            if img.is_feature:
                return img.image

    @property
    def get_product_price(self):
        if self.discount_price:
            return self.discount_price
        return self.regular_price

    @property
    def get_discount_percentage(self):
        if self.discount_price:
            return f"{int(round((1 - (self.discount_price / self.regular_price)) * 100, 0))}%"
        else:
            return _("No discount")

    @property
    def get_all_reviews(self) -> list[object]:
        return self.reviews.all().order_by("-created_at")

    @property
    def get_reviews_count(self) -> str:
        count = self.reviews.count()
        if count > 0 and count < 10:
            return f"0{count}"
        return f"{count}"

    @property
    def get_avarage_rating(self) -> range:
        reviews = self.reviews.all()
        if reviews:
            avg = round(sum(review.rating for review in reviews) / len(reviews))
            return range(avg)
        return range(0)

    @property
    def get_blank_rating_avg(self) -> range:
        reviews = self.reviews.all()
        if reviews:
            avg = round(sum(review.rating for review in reviews) / len(reviews))
            return range(5 - avg)
        return range(5)


class ProductImage(models.Model):
    """
    Images for a specific product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="products/",
        default="images/product_default.png",
    )

    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
