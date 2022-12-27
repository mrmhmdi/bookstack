from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from taggit.managers import TaggableManager

from extensions.utils import convert_to_jalali, _compress_image, _create_thumbnail

# Create your models here.

User = get_user_model()


class Shelve(models.Model):
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True, verbose_name='ایجاد کننده')
    name = models.CharField(max_length=50, verbose_name='نام قفسه')
    description = models.CharField(max_length=250, blank=True, verbose_name='توضیحات')
    slug = models.SlugField(unique=True,max_length=50, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/shelves/', default='images/default_shelve.jpg', verbose_name='عکس')
    thumbnail = models.ImageField(upload_to='images/shelve/thumbnail/', default='images/default_shelve.jpg')
    tags = TaggableManager(verbose_name='بر چسب ها')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'قفسه'
        verbose_name_plural = 'قفسه ها'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        self.thumbnail = _create_thumbnail(self.image)
        self.image = _compress_image(self.image)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    def thumbnail_tag(self):
        return format_html(f'<img width=125 hiegth=100 style="border-radius: 10px" src="{self.thumbnail.url}" />')
    thumbnail_tag.short_description = 'عکس'
    
    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'


class Book(models.Model):
    shelve = models.ForeignKey(Shelve, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name='قفسه')
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True, verbose_name='ایجاد کننده')
    authors = models.ManyToManyField(User, related_name='authors', verbose_name='نویسندگان')
    name = models.CharField(max_length=25, verbose_name='نام')
    published = models.BooleanField(default=False, verbose_name='وضعیت')
    description = models.CharField(max_length=250, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='images/books/', default='images/default_book.jpg', verbose_name='عکس')
    thumbnail = models.ImageField(upload_to='images/books/thumbnail/', default='images/default_book.jpg')
    tags = TaggableManager(verbose_name='برچسب ها')
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('-name',)
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        self.thumbnail = _create_thumbnail(self.image)
        self.image = _compress_image(self.image)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
        
    def thumbnail_tag(self):
        return format_html(f'<img width=125 hiegth=100 style="border-radius: 10px" src="{self.thumbnail.url}" />')
    thumbnail_tag.short_description = 'عکس'
    
    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'



class BookViews(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self) -> str:
        return f'{self.ip_address} in {self.book.name}'


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapter', verbose_name='کتاب')
    name = models.CharField(max_length=70, verbose_name='نام')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'فصل'
        verbose_name_plural = 'فصول'
    
    def __str__(self) -> str:
        return self.name
    
    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='page', verbose_name='قفسه')
    name = models.CharField(max_length=150, null=True, verbose_name='نام') # in deployment change null to False
    text = models.TextField(verbose_name='متن')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(verbose_name='برچسب ها')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'صفحه'
        verbose_name_plural = 'صفحات'

    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'



class PageImage(models.Model):
    image = models.ImageField(upload_to='images/pages/', verbose_name='عکس')
    page = models.ManyToManyField(Page, verbose_name='صفحه')
    
    def save(self, *args, **kwargs):
        self.image = _compress_image(self.image)
        return super().save(*args, **kwargs)


class PageReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reviews', default=None, verbose_name='صفحه') # remove the default in deployment
    created_at = models.DateField(auto_now_add=True, verbose_name='زمان انتشار')
    text = models.CharField(max_length=255, verbose_name='متن')
    
    def __str__(self) -> str:
        return self.user.username

    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'



class Activity(models.Model):

    class ActivityType(models.IntegerChoices):
        CREATED = 1
        UPDATED = 2
        DELETED = 3
    
    class ModelType(models.TextChoices):
        SHELVE = 'shelve'
        BOOK = 'book'
        PAGE = 'page'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    activity = models.CharField(choices=ActivityType.choices, max_length=1, verbose_name='نوع فعالیت')
    model_type = models.CharField(choices=ModelType.choices, max_length=6, verbose_name='نوع مدل')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کتاب')
    shelve = models.ForeignKey(Shelve, on_delete=models.CASCADE, null=True, blank=True, verbose_name='قفسه')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True, verbose_name='صفحه')
    name = models.CharField(max_length=150, verbose_name='نام')
    slug = models.SlugField(blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name='زمان انتشار')
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'فعالیت'
        verbose_name_plural = 'فعالیت ها'
    
    def jcreated_at(self):
        return convert_to_jalali(self.created_at)
    jcreated_at.short_description = 'زمان انتشار'
