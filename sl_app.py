import music21 as mu
import streamlit as st

# Define lists for describing notes
note_letters = ["C", "D", "E", "F", "G", "A", "B"]
# note_accidentals = ["", "♭", "♯"]
note_accidentals = ["", "b", "#"]
note_octaves = ["1", "2", "3", "4", "5", "6", "7"]
key_quality = ["Major", "Minor"]
# direction_options = ["b", "#"]


def key_selection(widgt_key: int) -> mu.key.Key:
    """Accepts the key prefix for a set of widgets
    retrieves values from associated widgets
    returns a mu.key.Key object
    """
    widgt_key = str(widgt_key)
    col1, col2, col3 = st.columns(3)

    with col1:
        chosen_rootnote_letter = st.selectbox(
            "Choose the root note:",
            (note_letters),
            key=widgt_key+"a"
        )
    
    with col2:
        chosen_accidental = st.selectbox(
            "Choose an accidental:",
            (note_accidentals),
            key=widgt_key+"b"
        )
        
    with col3:
        chosen_quality = st.selectbox(
            "Choose a key quality:",
            (key_quality),
            key=widgt_key+"c"
        )
        
    chosen_full_rootnote = chosen_rootnote_letter + chosen_accidental
    return mu.key.Key(chosen_full_rootnote, chosen_quality)

# This function accets int for widget diffrentiation, requests note values as str from user and retrieves a note
def note_selection(widgt_key):
    widgt_key = str(widgt_key)
    col1, col2, col3 = st.columns(3)

    with col1:
        chosen_note_letter = st.selectbox(
            "Choose a note:",
            (note_letters),
            key=widgt_key+"a"
        )
    
    with col2:
        chosen_accidental = st.selectbox(
            "Choose an accidental:",
            (note_accidentals),
            key=widgt_key+"b"
        )
        
    with col3:
        chosen_octave = st.selectbox(
            "Choose an octave:",
            (note_octaves),
            index=3,
            key=widgt_key+"c"
        )
        
    chosen_full_note = chosen_note_letter + chosen_accidental + chosen_octave
    return mu.note.Note(chosen_full_note)


st.write("Choose the lowest note in the song:")
start_bottom_note = note_selection(1)

st.write("Choose the highest note in the song:")
start_top_note = note_selection(2)

st.write("Choose the key this song is in:")
start_key = key_selection(3)

# TODO: add a friendly readable representation of start_key
st.write(
    f"\nThis song is in the key of {start_key}, the bottom note of the melody is " + \
    f"{start_bottom_note.pitch.unicodeNameWithOctave}, and the top note is " + \
    f"{start_top_note.pitch.unicodeNameWithOctave}."
)

by_halfsteps = st.slider("Transpose by how many half steps?", -11, 11, 0)
direction = "-" if by_halfsteps < 0 else "+"


new_key = start_key.transpose(by_halfsteps)
st.write(f"The new key is {new_key}")

# check for mismatch between interval specified in half steps and found interval 
# if mismatched, correct using complement interval

st.write("\nI will now make some calculations to make sure my transposition is correct!")

root_start_key = start_key.tonic
root_new_key = new_key.tonic
found_interval = mu.interval.Interval(root_start_key, root_new_key) # find interval between start key root and new key root
found_interval_in_halfsteps = found_interval.semitones # extract number of half steps in found interval

if by_halfsteps != found_interval_in_halfsteps:
    st.write("Seems the interval direction got flipped! Let me fix that real quick...")
    found_interval_complement = found_interval.complement
    st.write(f"I'm changing {found_interval.niceName} to {found_interval_complement.niceName}")
    found_interval = found_interval_complement

# checking the atributes of the interval
st.write(f"{found_interval.direction=}, {found_interval.directedName=}, {found_interval.directedNiceName=}")

# add descending direction to interval if not already

if direction == "-" and found_interval.direction == 1:
    st.write(f"the interval I have is {found_interval.directedNiceName}, but it should be descending")
    found_interval = found_interval.reverse()
    st.write(f"This interval was not set to descending, and now I changed it to {found_interval.directedNiceName}.")

# as far as we know, and interval would always be ascending unless specified otherwise. However,
# below is a test just in case
if direction == "+" and found_interval.direction == -1:
    st.write(f"the interval I have is {found_interval.directedNiceName}, but it should be ascending")
    found_interval = found_interval.reverse()
    st.write(f"This interval was not set to ascending, and now I changed it to {found_interval.directedNiceName}.")
# else:
#     found_interval.direction = 1
#     print(f"This interval is ascending, so it's {found_interval}")

st.write(f"I am transposing by {by_halfsteps} half steps, or {found_interval.directedNiceName}.")

new_bottom_note = start_bottom_note.transpose(found_interval)
new__top_note = start_top_note.transpose(found_interval)


st.write(
    f"In the key of {new_key}, the low note in the melody would be " + \
    f"{new_bottom_note.pitch.unicodeNameWithOctave}, and the high note would be " + \
    f"{new__top_note.pitch.unicodeNameWithOctave}."
)

st.write("Goodbye!")