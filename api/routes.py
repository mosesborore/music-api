from flask import jsonify, request, url_for
from api import app
from .models import Song

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'health_check': "running", 'status': 'ok'}), 200


@app.route('/songs', methods=['POST'])
def add_song():
    try:
        data = request.get_json()

        if isinstance(data, list):  # If the request contains a list of songs
            for song_data in data:
                add_single_song(song_data)
        else:
            add_single_song(data)

        return jsonify({'message': 'Songs added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def add_single_song(song_data):
    # Create a new song instance
    new_song = Song(
        title=song_data.get('title'),
        artist=song_data.get('artist'),
        album=song_data.get('album'),
        duration=song_data.get('duration'),
        featured_artists=song_data.get('featured_artists'),
        release_year=song_data.get('release_year')
    )

    # Save the new song to the database
    new_song.save()


@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        if page < 1 or limit < 1:
            return jsonify({'error': 'Invalid page or limit parameters'}), 400

        start_index = (page - 1) * limit
        end_index = start_index + limit  

        songs = Song.objects.skip(start_index).limit(limit)
        song_list = [
            {
                'title': song.title,
                'artist': song.artist,
                'album': song.album,
                'duration': song.duration,
                'featured_artists': song.featured_artists,
                'release_year': song.release_year,
                'link': url_for('get_song', slug=song.slug, _external=True)
            }
            for song in songs
        ]

        return jsonify({'songs': song_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/songs/<string:slug>', methods=['GET'])
def get_song(slug):
    try:
        song = Song.objects.get(slug=slug)
        song_data = {
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'duration': song.duration,
            'featured_artists': song.featured_artists,
            'release_year': song.release_year
        }
        return jsonify({'song': song_data}), 200
    except Song.DoesNotExist:
        return jsonify({'error': 'Song not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@app.route('/songs/<string:slug>', methods=['PUT'])
def update_song(slug):
    try:
        song = Song.objects.get(slug=slug)

        # Update song details
        data = request.get_json()
        song.title = data.get('title', song.title)
        song.artist = data.get('artist', song.artist)
        song.album = data.get('album', song.album)
        song.duration = data.get('duration', song.duration)
        song.featured_artists = data.get('featured_artists', song.featured_artists)
        song.release_year = data.get('release_year', song.release_year)

        # Save the updated song to the database
        song.save()

        return jsonify({'message': 'Song updated successfully'}), 200
    except Song.DoesNotExist:
        return jsonify({'error': 'Song not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/songs/<string:slug>', methods=['DELETE'])
def delete_song(slug):
    try:
        song = Song.objects.get(slug=slug)
        song.delete()

        return jsonify({'message': 'Song deleted successfully'}), 200
    except Song.DoesNotExist:
        return jsonify({'error': 'Song not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        
@app.route('/songs/search', methods=['GET'])
def search_songs():
    try:
        # Get search query from request parameters
        search_query = request.args.get('query', '')

        # Perform case-insensitive search on title, artist, and album fields
        songs = Song.objects.filter(
            __raw__={
                '$or': [
                    {'title': {'$regex': f'.*{search_query}.*', '$options': 'i'}},
                    {'artist': {'$regex': f'.*{search_query}.*', '$options': 'i'}},
                    {'album': {'$regex': f'.*{search_query}.*', '$options': 'i'}}
                ]
            }
        )

        # Prepare response data
        result = []
        for song in songs:
            result.append({
                'title': song.title,
                'artist': song.artist,
                'album': song.album,
                'duration': song.duration,
                'featured_artists': song.featured_artists,
                'release_year': song.release_year
            })

        return jsonify({'songs': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500