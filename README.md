# songtronic-api
API for songs and albums using flask and mongo database

# How to run the app
1. You can run the Makefile
2. create a collection called **songs** in mongodb
    ```
    python main.py
    ```
# How to interact with app
You can use any application similar to **Postman** or **insomia** or that which allows you interact with apis
Or, since I created thi application using my phone. I created the ***client.py*** file that allows me to achieve the same purpose as using **Postman.**
## How to use client.py
1. To add new song
    ![add new song](screenshot/new_song.png)
2. get all the songs
    ![get all songs](screenshot/get_all_songs.png)
3. delete a song
    ![delete songs](screenshot/delete_song.png)
4. Get song with slug
    ![get single song](screenshot/get-song.png)
5. Search a song
    ![search a song](screenshot/search.png)

