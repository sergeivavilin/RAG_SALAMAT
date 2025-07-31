import logging
import time
from typing import Callable, Awaitable

from fastapi import Request, Response

from src.common.logger import logger


async def log_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:

    if logger.isEnabledFor(logging.DEBUG):

        start_time = time.perf_counter()
        body = await request.json()
        if request.client:
            logger.debug(
                f"--> Incoming request: {request.method} {request.url} "
                f"- User input: {body.get('user_input')} "
                f"- User id: {body.get('thread_id')} "
                f"- Request from: {request.client.host}:{request.client.port} "
            )
        else:
            logger.warning(
                f"--> Incoming request: {request.method} {request.url} "
                f"- User input: {body.get('user_input')} "
                f"- User id: {body.get('thread_id')} "
                f"- Request from: CLIENT ip:port NOT FOUND "
            )
        # Перехватим ответ
        response = await call_next(request)

        # Считаем тело (нужно прочитать и пересобрать)
        resp_body = b""

        async for chunk in response.body_iterator:  # type: ignore
            resp_body += chunk

        response_body = resp_body.decode("utf-8", errors="ignore")
        process_time = time.perf_counter() - start_time

        # Логируем
        logger.debug(
            f"<-- Outgoing response: {request.method} {request.url} "
            f"- Status: {response.status_code} "
            f"- ResponseBody: {response_body} "
            f"- Process time: {process_time}"
        )

        # Возвращаем новый response с тем же телом
        return Response(
            content=resp_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    if logger.isEnabledFor(logging.INFO):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # Логируем
        method = request.method if request.method else "GET"
        url = request.url if request.url else ""
        host = request.client.host if request.client else ""
        port = request.client.port if request.client else ""
        log_dict = {
            "Method": method,
            "Url": url,
            "Request from": f"{host}:{port}",
            "Response status code": response.status_code,
            "Process time": process_time,
        }
        logger.info(
            log_dict,
            extra=log_dict,
        )
        return response
    # Если логирование выключено, просто вызываем следующую функцию
    return await call_next(request)
