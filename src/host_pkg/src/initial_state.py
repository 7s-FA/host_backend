"""Shared initial-state sequence. Every step requires a terminal success result."""
RELEASE_STEPS = (
    ('arm1', 'CLEAR_ERROR', '자재창고 중단 작업 정리', 30),
    ('arm2', 'CLEAR_ERROR', '조립대 중단 작업·리니어 정지 확인', 30),
    ('M1', 'RESTART', 'M1 정지 잠금 해제', 30),
    ('M2', 'RESTART', 'M2 정지 잠금 해제', 30),
)
HOME_STEPS = (
    ('arm1', 'HOME_A', '팔1 초기 자세 복귀', 180),
    # RESET returns both arms without the PREPARE_HOME retraction to 1.5mm.
    ('arm2', 'RESET', '팔2·3 저장 자세 복귀', 360),
    ('arm2', 'BUILD_SLIDE', '리니어 바깥쪽 초기 위치', 60),
    ('M1', 'GO_TO_PARK', 'M1 지정 주차 복귀', 300),
    ('M2', 'GO_TO_PARK', 'M2 지정 주차 복귀', 300),
)
INITIAL_STEPS = RELEASE_STEPS + HOME_STEPS

# Only use when the operator confirms both physical parking poses. Do not drive
# from a stale AMCL pose; recover localization before returning the arms.
PARKED_INITIAL_STEPS = RELEASE_STEPS[:2] + (
    ('M1', 'PREPARE_PARKED', 'M1 주차 위치·Nav2 준비', 610),
    ('M2', 'PREPARE_PARKED', 'M2 주차 위치·Nav2 준비', 610),
) + HOME_STEPS[:3]


def initial_steps(amrs_parked=False):
    return PARKED_INITIAL_STEPS if amrs_parked else INITIAL_STEPS


class StartupJournal:
    """Share the runtime's interrupted-motion journal with pre-web hostrun."""
    def __init__(self, path, saved):
        from pathlib import Path
        self.path, self.saved = Path(path), saved
        self.job = None

    def write(self):
        import json
        import os
        self.saved['full_reset'] = self.job
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.startup.tmp')
        with temporary.open('w') as stream:
            json.dump(self.saved, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(self.path)

    def begin(self, device, command):
        import time
        import uuid
        index = next(i for i, step in enumerate(INITIAL_STEPS) if step[:2] == (device, command))
        _, _, label, timeout = INITIAL_STEPS[index]
        self.job = dict(id=(self.job or {}).get('id', uuid.uuid4().hex), status='running', step=index,
                        uncertain=False, error='', stop_id=None,
                        task=dict(id=uuid.uuid4().hex, device=device, command=command, label=label,
                                  submitted=time.monotonic(), accepted=False, timeout=timeout))
        self.write()
        return self.job['task']['id']

    def accepted(self):
        self.job['task']['accepted'] = True
        self.write()

    def result(self, success, *, uncertain=False, error=''):
        if success:
            self.job.update(step=self.job['step']+1, task=None, uncertain=False)
            if self.job['step'] == len(INITIAL_STEPS):
                self.job['status'] = 'done'
        else:
            self.job.update(status='failed', uncertain=uncertain, error=error)
            if not uncertain:
                self.job['task'] = None
        self.write()
