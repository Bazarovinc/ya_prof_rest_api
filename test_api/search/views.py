from django.shortcuts import render
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from search.models import Notes
from search.serializer import NoteSerializer
from search.configurations import N
import sqlite3


class NotesView(APIView):

    def get(self, request, pk=0):
        if pk != 0:
            note = get_object_or_404(Notes.objects.all(), pk=pk)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        else:
            query = request.GET.get("query", "")
            if query != '':
                notes = Notes.objects.filter(Q(content__contains=str(query))
                                            | Q(content__contains=str(query)))
            else:
                notes = Notes.objects.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            note_saved = serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, pk):
        saved_user = get_object_or_404(Notes.objects.all(), pk=pk)
        serializer = NoteSerializer(instance=saved_user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            note_saved = serializer.save()
        return Response({"success": "Note was successfully updated "})

    def delete(self, request, pk):
        # Get object with this pk
        note = get_object_or_404(Notes.objects.all(), pk=pk)
        note.delete()
        return Response({"message": f"Note with id {pk} has been deleted."}, status=204)
