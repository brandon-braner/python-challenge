from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from lib.data import DB
from notify.data import notifications
from notify.model import Notification, NotificationRequest, NotificationReadRequest, NotificationResponse


class Notify:
    def __init__(self, db: DB) -> None:
        self.db: DB = db

    def get_notifications(self, user_id: int) -> Sequence[NotificationResponse]:
        if user_id < 0:
            raise HTTPException(400, "User ID must be a positive integer")

        with self.db.get_session() as session:
            try:
                notes = notifications.read_all(session, user_id)
            except NoResultFound:
                return []

        return [n.to_JSON() for n in notes]

    def post_notification(self, nr: NotificationRequest) -> NotificationResponse:

        if nr.user_id < 0:
            raise HTTPException(400, "User ID must be a positive integer")

        note = Notification.from_JSON(nr)

        with self.db.get_session() as session:
            try:
                note = notifications.create(session, note)
            except NoResultFound:
                raise HTTPException(400, "No user found for this notification")

        return note.to_JSON()

    def mark_notification_read(self, req: NotificationReadRequest) -> bool:
        if req.id <= 0:
            raise ValueError("Notification id must be greater then 0")
        
        with self.db.get_session() as session:
            try:
                notifications.set_as_read(session, req.id)
                return True
            except NoResultFound:
                raise HTTPException(400, "Notification Not Found")
            
        return False
            
