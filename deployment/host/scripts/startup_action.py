"""Bounded startup action calls; never retry a goal after a lost response."""
import time


def await_reply(node, ros, future, seconds, label):
    deadline = time.monotonic() + seconds
    while not future.done() and time.monotonic() < deadline:
        ros.spin_once(node, timeout_sec=min(.1, max(0., deadline-time.monotonic())))
    if not future.done():
        raise TimeoutError(label + ': 응답 시간 초과')
    return future.result()


def confirmed_result(reply, label):
    if reply.status != 4 or not reply.result.success or reply.result.message != 'IDLE':
        raise RuntimeError(label + ': 완료 확인 실패 · status=' + str(reply.status) +
                           ' · ' + str(reply.result.message))
    return reply


def release_once(client, goal, goal_id, wait, query_result, timeout, label, report=print):
    """Only for CLEAR_ERROR/AMR RESTART; correlate recovery with the same UUID."""
    if goal.command not in ('CLEAR_ERROR', 'RESTART'):
        raise ValueError('잠금 해제 전용입니다.')
    accepted = client.send_goal_async(goal, goal_uuid=goal_id)
    try:
        handle = wait(accepted, 8, label + ' 접수')
    except TimeoutError:
        # Do not resend. The server can complete even if send_goal response
        # failed. Query exactly this request, never infer success from gate.json.
        report(label + ': 접수 응답 누락 · 같은 요청 ID의 최종 결과 조회')
        return confirmed_result(query_result(goal_id, timeout), label)
    if not handle.accepted:
        raise RuntimeError(label + ': 거절 · 실행 중 작업/서버 상태 확인')
    try:
        result = wait(handle.get_result_async(), timeout, label + ' 완료')
    except TimeoutError:
        report(label + ': 완료 응답 누락 · 같은 요청 ID의 최종 결과 조회')
        result = query_result(goal_id, timeout)
    return confirmed_result(result, label)
