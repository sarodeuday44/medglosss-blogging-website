import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from django.db import models
from django.urls import reverse
from django.conf import settings
from uuslug import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Medgloss.utils import get_current_site
from Medgloss.utils import cache_decorator, cache
from django.utils.timezone import now
from mdeditor.fields import MDTextField

logger = logging.getLogger(__name__)


class LinkShowType(models.TextChoices):
    I = ('i', 'Homepage')
    L = ('l', 'List')
    P = ('p', 'Article page')
    A = ('a', 'Full Site')
    S = ('s', 'Friendship link page')


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('Creation time', default=now)
    last_mod_time = models.DateTimeField('Modification Time', default=now)

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self,
            Article) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
        if is_update_views:
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            if 'slug' in self.__dict__:
                slug = getattr(
                    self, 'title') if 'title' in self.__dict__ else getattr(
                    self, 'name')
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class Article(BaseModel):
    """Article"""
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Publish'),
    )
    COMMENT_STATUS = (
        ('o', 'Open'),
        ('c', 'Close'),
    )
    TYPE = (
        ('a', 'Article'),
        ('p', 'Page'),
    )
    title = models.CharField('title', max_length=200, unique=True)
    body = MDTextField('text')
    pub_time = models.DateTimeField(
        'Publish Time', blank=False, null=False, default=now)
    status = models.CharField(
        'Article Status',
        max_length=1,
        choices=STATUS_CHOICES,
        default='p')
    comment_status = models.CharField(
        'Comment status',
        max_length=1,
        choices=COMMENT_STATUS,
        default='o')
    type = models.CharField('type', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('Pageviews', default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Author',
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    article_order = models.IntegerField(
        'Sort by, the larger the number the higher the ranking', blank=False, null=False, default=0)
    category = models.ForeignKey(
        'Category',
        verbose_name='classification',
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    tags = models.ManyToManyField(
        'Tag', verbose_name='Label collection', blank=True)

    def body_to_string(self):
        return self.body

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-article_order', '-pub_time']
        verbose_name = "article"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        tree = self.category.get_category_tree()
        names = list(map(lambda c: (c.name, c.get_absolute_url()), tree))

        return names

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def comment_list(self):
        cache_key = 'article_comments_{id}'.format(id=self.id)
        value = cache.get(cache_key)
        if value:
            logger.info('get article comments:{id}'.format(id=self.id))
            return value
        else:
            comments = self.comment_set.filter(is_enable=True)
            cache.set(cache_key, comments, 60 * 100)
            logger.info('set article comments:{id}'.format(id=self.id))
            return comments

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    @cache_decorator(expiration=60 * 100)
    def next_article(self):
        # Next article
        return Article.objects.filter(
            id__gt=self.id, status='p').order_by('id').first()

    @cache_decorator(expiration=60 * 100)
    def prev_article(self):
        # Previous Article
        return Article.objects.filter(id__lt=self.id, status='p').first()


class Category(BaseModel):
    """Article Categories"""
    name = models.CharField('Category name', max_length=30, unique=True)
    parent_category = models.ForeignKey(
        'self',
        verbose_name="Parent category",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "classification"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse(
            'blog:category_detail', kwargs={
                'category_name': self.slug})

    def __str__(self):
        return self.name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        """
        Recursively get the parent of a category directory
        :return:
        """
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        """
        Get all subsets of the current category
        :return:
        """
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


class Tag(BaseModel):
    """Posts Tagged"""
    name = models.CharField('tag name', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_name': self.slug})

    @cache_decorator(60 * 60 * 10)
    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "label"
        verbose_name_plural = verbose_name


class Links(models.Model):
    """links"""

    name = models.CharField('Link Name', max_length=30, unique=True)
    link = models.URLField('Link Address')
    sequence = models.IntegerField('Sort', unique=True)
    is_enable = models.BooleanField(
        'Whether to display', default=True, blank=False, null=False)
    show_type = models.CharField(
        'Display type',
        max_length=1,
        choices=LinkShowType.choices,
        default=LinkShowType.I)
    created_time = models.DateTimeField('Creation time', default=now)
    last_mod_time = models.DateTimeField('Modification time', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = 'links'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SideBar(models.Model):
    """  Sidebar to display some html content """
    name = models.CharField('Title', max_length=100)
    content = models.TextField("content")
    sequence = models.IntegerField('Sort', unique=True)
    is_enable = models.BooleanField('Enabled or not', default=True)
    created_time = models.DateTimeField('Creation time', default=now)
    last_mod_time = models.DateTimeField('Modification time', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = 'Sidebar'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogSettings(models.Model):
    '''Site settings '''
    sitename = models.CharField(
        "Website name",
        max_length=200,
        null=False,
        blank=False,
        default='')
    site_description = models.TextField(
        "Website description",
        max_length=1000,
        null=False,
        blank=False,
        default='')
    site_seo_description = models.TextField(
        "Website SEO description", max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField(
        "Website keyword",
        max_length=1000,
        null=False,
        blank=False,
        default='')
    article_sub_length = models.IntegerField(
        "Article Summary Length", default=300)
    sidebar_article_count = models.IntegerField(
        "Number of sidebar articles", default=10)
    sidebar_comment_count = models.IntegerField(
        "Number of sidebar comments", default=5)
    show_google_adsense = models.BooleanField(
        'Whether to show Google ads', default=False)
    google_adsense_codes = models.TextField(
        'google adsense codes', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField(
        'Whether to turn on the site comments', default=True)

    analyticscode = models.TextField(
        "Website analytics code ",
        null=False,
        blank=False,
        default='')

    resource_path = models.CharField(
        "Static file save address",
        max_length=300,
        null=False,
        default='/var/www/resource/')

    class Meta:
        verbose_name = 'Website configuration'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename

    def clean(self):
        if BlogSettings.objects.exclude(id=self.id).count():
            raise ValidationError(_('There can only be one configuration'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from Medgloss.utils import cache
        cache.clear()
