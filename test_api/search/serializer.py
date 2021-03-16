from rest_framework import serializers
from .models import Notes
from search.configurations import N


class NoteSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source='make_not_blank', read_only=True)

    def make_not_blank(self):
        if self.fields.title == '':
            return self.fields.content[:N]
        return self.fields.title


    class Meta:
        model = Notes
        fields = ('id', 'title', 'content')
