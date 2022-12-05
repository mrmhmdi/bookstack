from rest_framework import serializers

from bookstack.models import (
    Activity, Book, Shelve
)

from taggit.serializers import (
    TagListSerializerField, TaggitSerializer
)

from bookstack.serializers.main_serializers import RecentBookSerializer


class ShelveSerializer(serializers.ModelSerializer):
    books = RecentBookSerializer(many=True)

    class Meta:
        model = Shelve
        fields = ('name', 'description', 'slug', 'created_at', 
                  'updated_at', 'image', 'books')


class NewShelveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shelve
        fields = ('name', 'slug')


class CreateUpdateShelveSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Shelve
        fields = ('name', 'description', 'image', 'tags')

    def create(self, validated_data):
        validated_data['creature'] = self.context['request'].user
        return super().create(validated_data)


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('name', 'slug', 'description', 'created_at', 'updated_at',)


class ShelveDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    
    class Meta:
        model = Shelve
        fields = ('name', 'description', 'created_at', 'updated_at', 'books')


class ShelveActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = ('user', 'activity', 'created_at', 'name', 'slug')