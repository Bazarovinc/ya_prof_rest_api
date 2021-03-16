from rest_framework import serializers
from .models import Notes


class NoteSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source='make_not_blank', read_only=True)

    class Meta:
        model = Notes
        fields = ('id', 'title', 'content')
