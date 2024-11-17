# app.py
from flask import Flask, render_template, request
from spotify_utils import get_token, search_for_artist, get_all_tracks_by_artist, calculate_total_listening_time, get_top_tracks_by_artist

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        artist_name = request.form["artist_name"]
        token = get_token()
        artist = search_for_artist(token, artist_name)
        
        if artist is None:
            return render_template("index.html", error="Artist not found.")
        
        artist_id = artist["id"]
        all_tracks = get_all_tracks_by_artist(token, artist_id)
        top_tracks = get_top_tracks_by_artist(token, artist_id)

        number_of_songs = len(all_tracks)
        hours, minutes, seconds = calculate_total_listening_time(all_tracks)

        return render_template(
            "index.html",
            artist_name=artist["name"],
            number_of_songs=number_of_songs,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            top_tracks=top_tracks
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
