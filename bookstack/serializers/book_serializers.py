from django.shortcuts import get_object_or_404
from rest_framework import serializers

from bookstack.models import (
    Book, Chapter, Activity, Shelve
)

from taggit.serializers import (
    TagListSerializerField, TaggitSerializer
)

class BookChapterSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'description')


class BookDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    chapter = BookChapterSerializer(many=True)
    
    class Meta:
        model = Book
        fields = ('creature', 'authors', 'name', 'created_at', 
                  'updated_at', 'description', 'slug', 'image', 'tags', 'chapter')


class BookActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = ('user', 'activity', 'model_type', 'name', 'slug', 'created_at')


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('name', 'authors', 'description', 'created_at', 'updated_at', 'image')


class CreateUpdateBookSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Book
        fields = ('authors', 'name', 'description', 'image', 'tags', 'published')
    
    def create(self, validated_data):
        shelve = get_object_or_404(Shelve, slug=self.context['shelve_slug'])
        validated_data['creature'] = self.context['request'].user
        validated_data['shelve'] = shelve
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        book = get_object_or_404(Book, id=instance.pk)
        if self.context['request'].user.id == book.creature.id:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {'authurize': "you don't have permission to do this."})