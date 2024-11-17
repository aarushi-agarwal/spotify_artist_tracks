import streamlit as st
from spotify_utils import get_token, search_for_artist, get_all_tracks_by_artist, calculate_total_listening_time, get_top_tracks_by_artist

# Streamlit App
def main():
    # Title of the app
    st.title("Spotify Artist Track Info")

    # Use a form to handle both Enter and Button click
    with st.form(key="artist_search_form"):
        artist_name = st.text_input("Enter the artist name:", "")
        submit_button = st.form_submit_button("Search")  # Triggers on both Enter and Button click

    # Check if form was submitted
    if submit_button:
        # Validate user input
        if not artist_name.strip():
            st.error("Please enter a valid artist name.")
            return

        # Fetch Spotify token
        token = get_token()

        # Search for the artist
        artist = search_for_artist(token, artist_name)

        # Handle case where the artist is not found
        if artist is None:
            st.error("Artist not found.")
            return

        # Display artist information
        st.subheader(f"Artist: {artist['name']}")

        # Fetch all tracks and top tracks
        artist_id = artist["id"]
        all_tracks = get_all_tracks_by_artist(token, artist_id)
        top_tracks = get_top_tracks_by_artist(token, artist_id)

        # Calculate total songs and listening time
        number_of_songs = len(all_tracks)
        hours, minutes, seconds = calculate_total_listening_time(all_tracks)

        # Output the total number of songs and listening time
        st.write(f"**Total Number of Songs:** {number_of_songs}")
        st.write(f"**Total Listening Time:** {hours} hours, {minutes} minutes, and {seconds} seconds")

        # Display the top tracks
        st.subheader("Top Tracks")
        if top_tracks:
            for idx, track in enumerate(top_tracks, start=1):
                st.write(f"{idx}. {track['name']}")
        else:
            st.write("No top tracks available.")

if __name__ == "__main__":
    main()
