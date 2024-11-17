def movie_poster_fetcher(imdb_link):
    url_data = requests.get(imdb_link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    # Find the div containing the poster image
    poster_div = s_data.find("div", class_="ipc-media--poster-27x40")
    if poster_div:
        # Find the img tag within the div
        img_tag = poster_div.find("img")
        if img_tag and 'src' in img_tag.attrs:
            movie_poster_link = img_tag['src']
            u = urlopen(movie_poster_link)
            raw_data = u.read()
            image = PIL.Image.open(io.BytesIO(raw_data))
            image = image.resize((158, 301))
            st.image(image, use_column_width=False)
        else:
            st.warning("Movie poster link not found.")
    else:
        st.warning("Poster div not found.")

def get_movie_info(imdb_link):
    url_data = requests.get(imdb_link, headers=hdr).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    imdb_content = s_data.find("meta", property="og:description")
    if imdb_content and 'content' in imdb_content.attrs:
        movie_descr = imdb_content.attrs['content']

        # Extracting information using different separators
        separators = ['Director:', 'Directors:', 'Stars:', 'Star:', 'Writer:', 'Writers:']
        info = {}
        for sep in separators:
            if sep in movie_descr:
                index = movie_descr.index(sep)
                key = sep[:-1]
                value = movie_descr[index + len(sep):].split('|')[0].strip()
                info[key] = value

        # Constructing final strings
        movie_director = info.get('Director', '')
        movie_cast = info.get('Stars', '')
        movie_story = info.get('Writer', '')

        return movie_director, f"Cast: {movie_cast}", f"Story: {movie_story}", ""
    else:
        st.warning("Description content not found.")
        return "", "", "", ""