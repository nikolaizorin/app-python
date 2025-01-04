from api.data import ratings
from api.exceptions.notfound import NotFoundException

from api.data import goodfellas


class RatingDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver

    """
    Add a relationship between a User and Movie with a `rating` property.
    The `rating` parameter should be converted to a Neo4j Integer.
    """
    # tag::add[]
    def add(self, user_id, movie_id, rating):
        # TODO: Create function to save the rating in the database
        # TODO: Call the function within a write transaction
        # TODO: Return movie details along with a rating
        def create_rating(tx, user_id, movie_id, rating):
            return tx.run("""
                match (u:User {userId: $user_id})
                match (m:Movie{tmdbId: $movie_id})
                merge (u)-[r:RATED]->(m)
                set r.rating = $rating, r.timestamp = timestamp()
                return m { .*, rating: r.rating} as movie
            """, user_id=user_id, movie_id=movie_id, rating=rating).single()

        with self.driver.session() as session:
            record = session.execute_write(create_rating, user_id=user_id, movie_id=movie_id, rating=rating)
        
        if record is None:
            raise NotFoundException()

        return record["movie"]    

        """
        return {
            **goodfellas,
            "rating": rating
        }
        """
    # end::add[]


    """
    Return a paginated list of reviews for a Movie.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.
    """
    # tag::forMovie[]
    def for_movie(self, id, sort = 'timestamp', order = 'ASC', limit = 6, skip = 0):
        # TODO: Get ratings for a Movie
        # TODO: Remember to escape the braces in the cypher query with double braces: {{ }}

        return ratings
    # end::forMovie[]
