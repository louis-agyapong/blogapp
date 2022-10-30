from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import PublishedManager


class Category(models.Model):
    """
    Blog category model
    """

    name: str = models.CharField(_("Name"), max_length=100)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT: str = "draft", _("DRAFT")
        PUBLISHED: str = "published", _("PUBLISHED")

    category = models.ForeignKey("Category", verbose_name=_("Category"), on_delete=models.PROTECT)
    title: str = models.CharField(_("Title"), max_length=250)
    slug: str = models.SlugField(_("Slug"), unique_for_date="publish")
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField(_("Body"))
    publish = models.DateTimeField(_("Published"), default=timezone.now)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Publish"), auto_now=True)
    status = models.CharField(_("Status"), max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self) -> str:
        return self.title
