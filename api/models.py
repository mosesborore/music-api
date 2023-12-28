from mongoengine import Document, StringField, FloatField, ListField, IntField
import re

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = re.sub(r"[^a-z0-9]+", "-", instance.title.lower())

    Klass = instance.__class__
    qs_exists = Klass.objects(slug=slug).first()
    if qs_exists:
        new_slug = "{slug}-{extra}".format(slug=slug, extra=instance.artist[0])

        return unique_slug_generator(instance, new_slug=new_slug)

    return slug

class Song(Document):
    title = StringField(required=True, max_length=100)
    artist = StringField(required=True, max_length=100)
    slug = StringField(required=True, max_length=100, unique=True)
    album = StringField(max_length=100)
    duration = StringField(max_length=6)
    featured_artists = ListField(StringField(max_length=100))
    release_year = IntField()
    
    def clean(self):
        """called as part of .save(), so it adds unique slug before saving the model"""
        slug = unique_slug_generator(self)
        # remove trailing '-'
        self.slug = slug.rstrip("-")