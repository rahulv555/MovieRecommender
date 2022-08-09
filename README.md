# MOVIE RECOMMENDATION APP

This is a movie recommending application, using TMDB data on the movies and their user ratings, that has been scraped using BeautifulSoup4 and requests libraries, as well as some data from the internet
The recommendation is done based on the Content-based and Collaborative-filter algorithms

#Technologies used 
PyQt5, QTdesigner for the GUI <br/>
pandas, numpy <br/>
sciKit learn - for the recommendation algorithms <br/>
BeautfilSoup4, requests - for webscrapping <br/>



#RUNNING THE PROGRAM
Run the main.py file to launch the program

The application will be launched as follows
![Base](https://user-images.githubusercontent.com/75095822/183623915-a5c9caa5-95b5-422b-abb8-2433764da0fe.jpg)

At the top left, is the entire list of movies, and the user can select the desired movie and click add to add it to their favourite movies list, which is the list below it.
![select](https://user-images.githubusercontent.com/75095822/183624191-ffe0c398-be3a-41b3-9d06-b221273d5e69.jpg)

The user can add multiple movies, and adjust their ratings for the movie as desired

Now, there are two options, to recommend movie based on either of the two algorithms
Recommend based on selected movie - CONTENT BASED, recommends based on the single selected movie <br/> 
![Content Based](https://user-images.githubusercontent.com/75095822/183624623-5593fb2c-5e37-45cd-a5b0-0472de6334c7.jpg)

Recomment based on collaborative filter - COLLAB FILTER, recommends based on the entire list of favourite movies and their ratings by the user
![Collab filter](https://user-images.githubusercontent.com/75095822/183624637-8c3fa392-5bd5-4d7b-9ea0-bb72aa08f51e.jpg)

In the recommended movies list, the user can select any movie, and its title and descriptions are displayed.

NOTE :
Upon clicking recommend, it may take some to load. I aim to implement loading states as well as improve the overall styling in the future.

