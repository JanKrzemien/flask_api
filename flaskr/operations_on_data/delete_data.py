from flaskr.db import get_db
from ..error_handling.logger import logger

from ..error_handling.exceptions import INTERNAL_ERROR_EXCEPTION

def delete_user_by_id(id: int) -> None:
    """deletes user with id given as a param from table user

    Args:
        id (int): users id

    Raises:
        INTERNAL_ERROR_EXCEPTION: someting bad happened while handling database operation
    """
    db = get_db()
    try:
        db.execute(
            "DELETE FROM user WHERE id = ?",
            (id, )
        )
        db.commit()
    except Exception as e:
        logger.error(e)
        raise INTERNAL_ERROR_EXCEPTION(error='Internal error while deleting user.')