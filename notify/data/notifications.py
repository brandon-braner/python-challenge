from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from notify.model import Notification
from user.model import User


# @capture_stderr()
def read_all(
    session: Session,
    user_id: int,
) -> Sequence[Notification]:

    query = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created.desc())
    )

    rslt = session.scalars(query).all()
    return rslt


def create(
    session: Session,
    note: Notification,
) -> Notification:

    # raise an exception if the user does not exist
    session.query(User).filter(User.id == note.user_id).one()

    session.add(note)
    session.commit()
    session.refresh(note)

    return note

def set_as_read(session: Session, id: int) -> int:

    session.execute(
        update(Notification).where(Notification.id == id).values(is_read=True)
    )
    
    session.commit()
    return id

