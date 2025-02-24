from typing import Sequence

import pytest
from fastapi.testclient import TestClient

from lib.data import Session
from notify.model import NotificationResponse


@pytest.mark.parametrize(
    "arg_user_id, exp_status_code, exp_notification_count",
    [
        (-1, 400, None),  # negative number should not be valid
        (0, 200, 0),  # User 0 doesn't exist, should return empty list
        (1, 200, 3),  # sucess
    ],
)
def test_get_notifications_user(
    session: Session,
    client: TestClient,
    testdata,
    arg_user_id: int,
    exp_status_code: int,
    exp_notification_count: int | None,
):
    # arrange

    # act
    resp = client.get(f"notify/notifications/{arg_user_id}")

    # assert
    assert resp.status_code == exp_status_code

    if exp_status_code == 200:
        body: Sequence[NotificationResponse] = resp.json()
        assert len(body) == exp_notification_count

        # Check the content of each notification
        for item in body:
            nr: NotificationResponse = NotificationResponse.model_validate(item)
            assert nr.user_id == arg_user_id
    else:
        assert "detail" in resp.json()


@pytest.mark.parametrize(
    "arg_note, exp_status_code",
    [
        (
            {
                "user_id": 1,
                "title": "Test Notification",
                "body": "This is a test notification.",
                "category": "chat",
                "payload": {"message_id": 12345},
            },
            200,
        ),  # success
        (
            {
                "user_id": -1,
                "title": "Invalid User",
                "body": "This notification has an invalid user.",
                "category": "chat",
                "payload": {"message_id": 12345},
            },
            400,
        ),  # case user is invalid (below 0)
        (
            {
                "user_id": 98765,
                "title": "Invalid User",
                "body": "This notification has an user that does not exist.",
                "category": "chat",
                "payload": {"message_id": 12345},
            },
            400,
        ),  # case user is invalid (does not exist)
        (
            {
                "user_id": 98765,
                "body": "This notification does not have a title.",
                "category": "chat",
            },
            422,
        ),  # case empty title
        (
            {
                "user_id": 98765,
                "title": "Empty body",
                "category": "chat",
            },
            422,
        ),  # case empty body
        (
            {
                "user_id": 98765,
                "title": "Empty category",
                "body": "Who knows what sort of notification this even is?",
            },
            422,
        ),  # case empty category
    ],
)
def test_post_notification(
    session: Session,
    client: TestClient,
    testdata,
    arg_note: dict[str, any],
    exp_status_code: int,
):
    # arrange

    # act
    resp = client.post("notify/notification", json=arg_note)

    # assert
    assert resp.status_code == exp_status_code

    if exp_status_code == 200:
        nr = NotificationResponse.model_validate(resp.json())
        assert nr.title == arg_note["title"]
        assert nr.body == arg_note["body"]
    else:
        assert "detail" in resp.json()



@pytest.mark.parametrize("arg_note, exp_status_code" [
    (1, 204),
    (4, 400)
] )
def test_mark_as_red(
    session: Session,
    client: TestClient,
    testdata,
    arg_note,
    exp_status_code 
):
    resp = client.patch("notify/notification", json={"id": arg_note})

    assert resp.status_code == exp_status_code