
from music21 import note, stream

notes = [
    note.Note("C4", quarterLength=1.0),
    note.Note("D4", quarterLength=1.0),
    note.Note("E4", quarterLength=1.0),
    note.Note("F4", quarterLength=1.0)
]

stream = stream.Stream()
for n in notes:
    stream.append(n)

stream.show('midi')