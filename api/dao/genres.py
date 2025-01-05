from api.data import genres
from api.exceptions.notfound import NotFoundException

class GenreDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver

    """
    This method should return a list of genres from the database with a
    `name` property, `movies` which is the count of the incoming `IN_GENRE`
    relationships and a `poster` property to be used as a background.

    [
       {
        name: 'Action',
        movies: 1545,
        poster: 'https://image.tmdb.org/t/p/w440_and_h660_face/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
       }, ...

    ]
    """
    # tag::all[]
    def all(self):
        # TODO: Open a new session
        with self.driver.session() as session:
            
            # TODO: Define a unit of work to Get a list of Genres
            genres = session.execute_read(lambda tx: tx.run("""
                match (g:Genre) where g.name <> '(no genres listed)'

                call {
                    with g
                    match (g)<-[:IN_GENRE]-(m:Movie)
                    where m.imdbRating is not Null and m.poster is not Null
                    return m.poster as poster
                    order by m.imdbRating desc limit 1
                }    

                return g { .*, movies: count{(g)<-[:in_GENRE]-(:Movie)}, poster: poster}
                order by g.name desc
                """).value(0))
        # TODO: Execute within a Read Transaction

        return genres
    # end::all[]


    """
    This method should find a Genre node by its name and return a set of properties
    along with a `poster` image and `movies` count.

    If the genre is not found, a NotFoundError should be thrown.
    """
    # tag::find[]
    def find(self, name):
        # TODO: Open a new session
        # TODO: Define a unit of work to find the genre by it's name
        # TODO: Execute within a Read Transaction

        return [g for g in genres if g["name"] == name][0]
    # end::find[]