from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify


from posts.models import PostModel


@receiver(pre_save, sender=PostModel)
def generate_slag_for_post(sender, instance, **kwargs):
    original_blog = slugify(instance.title)
    slug = original_blog
    count = 0
    while PostModel.objects.filter(slug=slug).exists():
        slug = f"{original_blog}-{count}"
        count += 1

    instance.slug = slug

