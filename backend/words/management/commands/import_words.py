import os
import json
from django.core.management.base import BaseCommand
from words.models import Word
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports words from a JSON file into the Word model'

    def handle(self, *args, **options):
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'english_words_2000.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            words_data = json.load(file)

        for word_data in words_data:
            Word.objects.create(**word_data)

        self.stdout.write(self.style.SUCCESS('Successfully imported words'))
