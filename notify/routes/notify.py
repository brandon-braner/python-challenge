from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response

from lib.data import DB
from notify.handler import Notify
from notify.model import NotificationRequest, NotificationReadRequest, NotificationResponse


def notify(db: DB) -> APIRouter:

    router = APIRouter(
        prefix="/notify",
        tags=["notify"],
    )

    def get_handler() -> Notify:
        return Notify(db)

    # set healthcheck endpoint
    @router.get("/health")
    async def health() -> Response:
        return Response(status_code=200)

    @router.get("/notifications/{user_id}")
    async def get_notifications_user(
        handler: Annotated[Notify, Depends(get_handler)],
        user_id: int,
    ) -> Sequence[NotificationResponse]:
        return handler.get_notifications(user_id)

    @router.post("/notification")
    async def post_notification(
        handler: Annotated[Notify, Depends(get_handler)], req: NotificationRequest
    ) -> NotificationResponse:
        return handler.post_notification(req)



    @router.patch("/notification")
    async def patch_notification(
        handler: Annotated[Notify, Depends(get_handler)], req: NotificationReadRequest
    ) -> Response:
        handler.mark_notification_read(req)
        # As we talked about need to add checking for authed user
        return Response(status_code=204)
    return router
