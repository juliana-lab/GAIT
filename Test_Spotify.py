import magenta
import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music import DEFAULT_QUARTERS_PER_MINUTE
from magenta.music.protobuf import generator_pb2, music_pb2

# Initialize the model.
bundle = sequence_generator_bundle.read_bundle_file('path/to/downloaded/bundle')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# Model parameters.
num_steps = 128  # Length of the melody.
temperature = 1.0  # The randomness of the generated melodies.

# Create a seed melody.
seed = music_pb2.NoteSequence()
seed.ticks_per_quarter = 220
note_seq.note_sequence_io.note_sequence_to_midi_file(seed, 'seed.mid')

# Generate a melody from the seed.
generator_options = generator_pb2.GeneratorOptions()
generator_options.args['temperature'].float_value = temperature
generate_section = generator_options.generate_sections.add(start_time=0, end_time=num_steps)
sequence = melody_rnn.generate(seed, generator_options)

# Play the generated melody.
note_seq.plot_sequence(sequence)
note_seq.play_sequence(sequence, synth=note_seq.fluidsynth)




"""
def get_token():
    auth_string = client_id+ ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result =json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=(artist_name)&type=artist&limit=1"

    query_url = url + query
    result =get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) ==0:
        print("No artist with this name exists...")
        return None

    return json_result[0]


token = get_token()
result = search_for_artist(token,"ACDC")
artist_id = result["id"]
"""