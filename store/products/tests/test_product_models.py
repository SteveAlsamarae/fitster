from django.urls import reverse
from django.db.models import QuerySet

from tests.products_factories import *  # noqa: F401
from store.products.tests.fixtures import *  # noqa: F401


def test_product_category_factory(product_category_factory):
    assert product_category_factory is not None
    assert product_category_factory is ProductCategoryFactory


def test_product_category_model(product_category):
    assert product_category is not None
    assert isinstance(product_category, ProductCategory)


def test_product_category_model_params(product_category):
    assert product_category.name == "Product Category"
    assert product_category.slug == "product-category"
    assert product_category.is_active is True


def test_product_category_str(product_category):
    assert str(product_category) == product_category.name


def test_get_all_products_exists(product_category):
    assert product_category.get_all_products().exists() is False


def test_get_products_count(product_category):
    assert product_category.get_products_count() == 0


def test_product_factories(product_factory):
    assert product_factory is not None
    assert product_factory is ProductFactory


def test_product_model(product):
    assert product is not None
    assert isinstance(product, Product)


def test_product_model_params(product):
    assert product.categories is not None
    assert product.title == "Product"
    assert product.short_description == "Product Short Description"
    assert product.description == "Product Description"
    assert product.additional_information == "Product - Additional Description"
    assert product.slug == "product"
    assert product.regular_price == 60
    assert product.discount_price == 50
    assert product.stocks == 10
    assert product.sale_tag == "SALE"
    assert product.is_active is True


def test_product_str(product):
    assert str(product) == product.title


def test_product_absolute_url(product):
    product_url = reverse("products:product_detail", kwargs={"slug": product.slug})
    assert product.get_absolute_url() == product_url


def test_product_images_exists(product):
    assert product.get_product_images().exists() is False


def test_get_product_images_type(product):
    assert isinstance(product.get_product_images(), QuerySet)


def test_extract_information_is_method(product):
    assert callable(product.extract_additional_information)


def test_product_model_has_get_review_count_property(product):
    assert callable(product.get_reviews_count) is False


def test_get_avarage_rating_is_property(product):
    assert callable(product.get_avarage_rating) is False


def test_get_blank_rating_avg_is_property(product):
    assert callable(product.get_blank_rating_avg) is False


def test_get_product_reviews_exists(product):
    assert product.get_all_reviews.exists() is False


def test_get_discount_percentage_is_property(product):
    assert callable(product.get_discount_percentage) is False


def test_get_product_price_is_property(product):
    assert callable(product.get_product_price) is False


def test_get_get_featured_img_is_property(product):
    assert callable(product.get_featured_img) is False


def test_product_image_factories(product_image_factory):
    assert product_image_factory is not None
    assert product_image_factory is ProductImageFactory


def test_product_image_model(product_image):
    assert product_image is not None
    assert isinstance(product_image, ProductImage)


def test_product_image_model_params(product_image):
    assert product_image.product is not None
    assert product_image.image is not None
    assert product_image.is_feature is False


def test_product_image_meta_class(product_image):
    assert product_image._meta.model_name == "productimage"
    assert product_image._meta.verbose_name == "Product Image"
    assert product_image._meta.verbose_name_plural == "Product Images"
