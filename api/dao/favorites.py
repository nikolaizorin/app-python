from api.data import popular, goodfellas
from api.exceptions.notfound import NotFoundException

class FavoriteDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver


    """
    This method should retrieve a list of movies that have an incoming :HAS_FAVORITE
    relationship from a User node with the supplied `userId`.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.

    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.
    """
    # tag::all[]
    def all(self, user_id, sort = 'title', order = 'ASC', limit = 6, skip = 0):
        # TODO: Open a new session
        # TODO: Retrieve a list of movies favorited by the user
        with self.session.driver.session() as session:
        
            movies = session.execute_read(lambda tx: tx.run("""
                match (u:User {{userId: $userId}})-[r:HAS_FAVORITE]->(m:Movie)
                return m {{ .*, favorite: true}} as movie
                order by m. '{0}' {1}
                skip $skip
                limit $limit
            """.format (sort, order), userId=userId, limit=limit, skip=skip).value("movie") 
            )

        return movies



       
        #return popular
    # end::all[]


    """
    This method should create a `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.
   *
    If either the user or movie cannot be found, a `NotFoundError` should be thrown.
    """
    # tag::add[]
    def add(self, user_id, movie_id):
        # TODO: Open a new Session
        # TODO: Define a new transaction function to create a HAS_FAVORITE relationship
        # TODO: Execute the transaction function within a Write Transaction
        # TODO: Return movie details and `favorite` property
        def add_to_favorites(tx, user_id, movie_id):
        row = tx.run("""
            MATCH (u:User {userId: $userId})
            MATCH (m:Movie {tmdbId: $movieId})
            MERGE (u)-[r:HAS_FAVORITE]->(m)
            ON CREATE SET u.createdAt = datetime()
            RETURN m {
                .*,
                favorite: true
            } AS movie
        """, userId=user_id, movieId=movie_id).single()

        # If no rows are returnedm throw a NotFoundException
        if row == None:
            raise NotFoundException()

        return row.get("movie")

    with self.driver.session() as session:
        return session.execute_write(add_to_favorites, user_id, movie_id)

        """
        return {
            **goodfellas,
            "favorite": False
        }
        """
    # end::add[]

    """
    This method should remove the `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.

    If either the user, movie or the relationship between them cannot be found,
    a `NotFoundError` should be thrown.
    """
    # tag::remove[]
    def remove(self, user_id, movie_id):
        # TODO: Open a new Session
        # TODO: Define a transaction function to delete the HAS_FAVORITE relationship within a Write Transaction
        # TODO: Execute the transaction function within a Write Transaction
        # TODO: Return movie details and `favorite` property

        def rem_from_fav(tx, user_id, movie_id):
            row = tx.run("""
               match (u:User {userId: $UserId})-[r:HAS_FAVORITE]->(m:Movie {movieId: $movieId})
               delete r
               return m { .*, favorite: false} as movie
            """,userId=user_id, movieId=movie_id).single()

            if row == None:
                raise NotFoundException()

            return row.get("movie")

        with self.driver.session() as session:
            return session.execute_write(rem_from_fav, user_id, movie_id)

        """
        return {
            **goodfellas,
            "favorite": False
        }
        """
    # end::remove[]
