from flaskr.db import get_db
from ..error_handling.logger import logger

from ..error_handling.exceptions import INTERNAL_ERROR_EXCEPTION

def update_users_refresh_secret_key(new_refresh_secret_key: str, users_id: int) -> None:
    """updates users refresh secret key

    Args:
        new_refresh_secret_key (str): new refresh secret key
        users_id (int): users id

    Raises:
        INTERNAL_ERROR_EXCEPTION: is raised when operation on db failes
    """
    
    db = get_db()
    try:
        db.execute(
            "UPDATE user SET refresh_secret_key = ? WHERE id = ?",
            (new_refresh_secret_key, users_id)
        )
        db.commit()
    except Exception as e:
        logger.error(e)
        raise INTERNAL_ERROR_EXCEPTION(error='Error while updating user.')