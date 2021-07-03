from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pytils.translit import slugify

from .validators import validate_date

CustomUser = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=200,
        blank=False,
        null=False,
        help_text='Укажите назване категории'
    )
    slug = models.SlugField(
        'Адрес страницы категории',
        max_length=200,
        unique=True,
        help_text=(
            'Укажите адрес для страницы группы. Используйте только'
            ' латиницу, цифры, дефисы и знаки подчёркивания.'
        ),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Напишите название жанра'
    )
    slug = models.SlugField(
        'Адрес страницы жанра',
        max_length=200,
        unique=True,
        help_text=(
            'Укажите адрес для страницы группы. Используйте только'
            ' латиницу, цифры, дефисы и знаки подчёркивания.'
        ),
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200,
        blank=False,
        help_text='Напишите название произведения',
    )
    year = models.PositiveSmallIntegerField(
        db_index=True,
        validators=[validate_date]
    )
    description = models.TextField(
        help_text='описание произведения',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='categores',
        db_index=False,
    )

    class Meta:
        verbose_name = 'Названиe'
        verbose_name_plural = 'Названия'
        ordering = ['id', ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        CustomUser, blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='rev'
    )
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MaxValueValidator(10, 'Больше 10 поставить нельзя'),
            MinValueValidator(1, 'Меньше 1 поставить нельзя')
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['id', ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_object_user',
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date', ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.review} прокоментировал {self.author}'
