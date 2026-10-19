import json
import allure


class AllureApiLogger:

    @staticmethod
    def attach_request(
        endpoint: str,
        method: str,
        payload: dict = None
    ):

        allure.attach(
            endpoint,
            name="Endpoint",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            method,
            name="HTTP Method",
            attachment_type=allure.attachment_type.TEXT
        )

        if payload:

            allure.attach(
                json.dumps(
                    payload,
                    indent=4
                ),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

    @staticmethod
    def attach_response(
        response
    ):

        allure.attach(
            str(response.status_code),
            name="Status Code",
            attachment_type=allure.attachment_type.TEXT
        )

        try:

            allure.attach(
                json.dumps(
                    response.json(),
                    indent=4
                ),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        except Exception:

            allure.attach(
                str(response.text),
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT
            )

    @staticmethod
    def attach_json(
        title: str,
        content: dict
    ):

        allure.attach(
            json.dumps(
                content,
                indent=4
            ),
            name=title,
            attachment_type=allure.attachment_type.JSON
        )

    @staticmethod
    def attach_text(
        title: str,
        content: str
    ):

        allure.attach(
            content,
            name=title,
            attachment_type=allure.attachment_type.TEXT
        )