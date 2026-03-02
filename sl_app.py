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
            ":grey[Tonic (first note in scale)]",
            (note_letters),
            key=widgt_key+"a"
        )
    
    with col2:
        chosen_accidental = st.selectbox(
            ":grey[Accidental]",
            (note_accidentals),
            key=widgt_key+"b"
        )
        
    with col3:
        chosen_quality = st.selectbox(
            ":grey[Key Quality]",
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
            ":grey[Note]",
            (note_letters),
            key=widgt_key+"a"
        )
    
    with col2:
        chosen_accidental = st.selectbox(
            ":grey[Accidental]",
            (note_accidentals),
            key=widgt_key+"b"
        )
        
    with col3:
        chosen_octave = st.selectbox(
            ":grey[Octave]",
            (note_octaves),
            index=3,
            key=widgt_key+"c"
        )
        
    chosen_full_note = chosen_note_letter + chosen_accidental + chosen_octave
    return mu.note.Note(chosen_full_note)

st.title("Melodic Range Transposition Tool")

st.write(
    """Use this tool to input the key, bottom note and top note in the melody. Then use
    the slider below to find a new key with an appropriate melodic range.
    """
)

st.write("---")

col1, col2 = st.columns(spec=[0.7, 0.3])

with col1:
    st.write("#### Starting Key")
    start_key = key_selection(1)

st.write("")

st.write("#### Melodic Range")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.write("Lowest melody note")
    start_bottom_note = note_selection(2)

with col2:
    st.write("Highest melody note")
    start_top_note = note_selection(3)

st.write("")
st.write("")

# TODO: add a friendly readable representation of start_key
st.write(
    f"""This song is in the key of :primary[**{start_key.tonic.unicodeName} {start_key.mode}**], 
    the bottom note of the melody is :primary[**{start_bottom_note.pitch.unicodeNameWithOctave}**], 
    and the top note is :primary[**{start_top_note.pitch.unicodeNameWithOctave}**]
    """
)

st.write("---")

st.write("#### Transposition")

col1, col2 = st.columns(2)

with col1:
    by_halfsteps = st.slider(":grey[Transpose up or down by half steps]", -11, 11, 0)
    direction = "-" if by_halfsteps < 0 else "+"

new_key = start_key.transpose(by_halfsteps)

# check for mismatch between interval specified in half steps and found interval 
# if mismatched, correct using complement interval
# TODO: organize the transposition verfication in a function

root_start_key = start_key.tonic
root_new_key = new_key.tonic
found_interval = mu.interval.Interval(root_start_key, root_new_key) # find interval between start key root and new key root
found_interval_in_halfsteps = found_interval.semitones # extract number of half steps in found interval

if by_halfsteps != found_interval_in_halfsteps:
    found_interval = found_interval.complement

# add descending direction to interval if not already

if direction == "-" and found_interval.direction == 1:
    found_interval = found_interval.reverse()

# as far as we know, and interval would always be ascending unless specified otherwise. However,
# below is a test just in case

if direction == "+" and found_interval.direction == -1:
    found_interval = found_interval.reverse()


if by_halfsteps != 0:
    st.write(f"Transpose by :primary[**{by_halfsteps}**] half steps, or a :primary[**{found_interval.directedNiceName}**]")
    new_bottom_note = start_bottom_note.transpose(found_interval)
    new__top_note = start_top_note.transpose(found_interval)
    st.write("---")
    st.write(
        f"##### In the key of :primary[**{new_key.tonic.unicodeName} {new_key.mode}**], the bottom " + \
        f"note of the melody is :primary[**{new_bottom_note.pitch.unicodeNameWithOctave}**], and the " + \
        f"top note is :primary[**{new__top_note.pitch.unicodeNameWithOctave}**]"
    )

else:
    st.write("")
    st.write("---")
    st.write("##### ")
    st.write("##### ")

st.write(":grey[:small[We'd love to hear from you! Send us your [feedback](https://forms.gle/ZXTujHMSfU3j2i678).]]")