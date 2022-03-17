import genanki
MODEL_ID = 1092343524
DECK_ID = 223556345

from pathlib import Path

anki_data_p = Path('anki_data')

qa_files = []
for p in anki_data_p.glob("*_question.png"):
    qa_files.append((p.name, p.name.replace('question', 'answer')))


my_model = genanki.Model(
  MODEL_ID,
  'Simple Model with Media',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Chinese City Info',
      'qfmt': '{{Question}}',
      'afmt': '{{Answer}}',
    },
  ])


my_deck = genanki.Deck(
  DECK_ID,
  'Chinese City Info')

for q, a in qa_files:
    my_note = genanki.Note(model=my_model, fields=[f'<img src="{q}">', f'<img src="{a}">'])
    my_deck.add_note(my_note)


# 这个地方其实不用模仿anki的官方文档， 一定要把媒体文件放在指定的地方
my_package = genanki.Package(my_deck)
all_meida = []
for files in qa_files:
    for f in files:
        all_meida.append(str(anki_data_p / f))
my_package.media_files = all_meida

my_package.write_to_file('ChineseCityInfo.apkg')
