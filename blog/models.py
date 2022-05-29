import uuid

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from markdownx.utils import markdownify


TAG_VALIDAITON = RegexValidator(
    r"^[a-zA-Z, ]+$",
    message="Tags must be comma separated list of words",
    code="invalid_tag",
)


class Post(models.Model):
    """
    Post model to store user post in DB
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    thumbnail = models.ImageField(
        upload_to="blog/thumbnails", verbose_name=_("Thumbnail")
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug"))
    content = models.TextField(verbose_name=_("Content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    tags = models.CharField(
        max_length=255, verbose_name=_("Tags"), validators=[TAG_VALIDAITON]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def get_comma_separated_tags(self) -> list:
        """Returns post tags as a list of tag

        Returns:
            list: List of tags
        """
        return [tag.strip() for tag in self.tags.strip().split(",")]

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Post.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + "_" + str(counter)
                        counter += 1
                except Post.DoesNotExist:
                    self.slug = slug
                    break

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def get_markdown_content(self) -> str:
        return markdownify(self.content)
