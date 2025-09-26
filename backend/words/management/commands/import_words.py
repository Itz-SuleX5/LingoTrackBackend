import json
from django.core.management.base import BaseCommand
from words.models import Word

class Command(BaseCommand):
    help = 'Imports words from a JSON file into the Word model'

    def handle(self, *args, **options):
        json_file_path = 'C:/Users/User/Downloads/LingoTrack/english_words_2000.json'
        with open(json_file_path, 'r', encoding='utf-8') as file:
            words_data = json.load(file)

        for word_data in words_data:
            Word.objects.create(
                base=word_data['base'],
                s_form=word_data['s_form'],
                past=word_data['past'],
                past_participle=word_data['past_participle'],
                ing=word_data['ing'],
                meaning=word_data['meaning'],
                example=word_data['example'],
                translation=word_data['translation']
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported words'))