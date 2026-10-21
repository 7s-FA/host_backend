"""No ROS or hardware: exercise freshness, reboot and sensor-fault admission."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'AMR/common/navigation'))
from host_prepare import ImuHealth


class ImuReadinessTests(unittest.TestCase):
    def status(self,h,sample,now,**extra):
        fields=dict(cal='READY',attitude='1',initialized='1',hal='0',
                    result='OK',age_ms='20',samples=str(sample))
        fields.update(extra)
        h.status(' '.join(k+'='+v for k,v in fields.items()),now)

    def data(self,h,stamp,now):
        h.data(stamp,.02,(1,0,0,0),0,now)

    def healthy(self):
        h=ImuHealth()
        self.status(h,10,0);self.data(h,1,0)
        self.status(h,60,1.1);self.data(h,2,1.1)
        return h

    def test_healthy_and_stale(self):
        h=self.healthy()
        self.assertTrue(h.ready(1.1))
        self.assertFalse(h.ready(1.7))
        self.data(h,3,4)
        self.assertFalse(h.ready(4))

    def test_failure_flags(self):
        for fields in [dict(hal='2'),dict(attitude='0'),dict(result='I2C_ERROR'),
                       dict(cal='WARMUP'),dict(age_ms='1000'),dict(initialized='0')]:
            h=self.healthy();self.status(h,61,1.2,**fields)
            self.assertFalse(h.ready(1.2),fields)

    def test_stuck_counter(self):
        h=self.healthy();self.status(h,60,1.2)
        self.assertFalse(h.ready(1.2))

    def test_bad_or_repeated_data(self):
        for stamp,age,q,cov in [(3,.02,(float('nan'),0,0,0),0),
                                (3,1,(1,0,0,0),0),(2,.02,(1,0,0,0),0),
                                (3,.02,(1,0,0,0),-1),(3,.02,(0,0,0,0),0)]:
            h=self.healthy();h.data(stamp,age,q,cov,1.2)
            self.assertFalse(h.ready(1.2))

    def test_restart_requires_new_stable_evidence(self):
        h=self.healthy();self.status(h,1,1.2)
        self.assertFalse(h.ready(1.2))
        self.status(h,2,2.2);self.data(h,3,2.2)
        self.assertFalse(h.ready(2.2))
        self.status(h,52,3.3);self.data(h,4,3.3)
        self.assertTrue(h.ready(3.3))


if __name__=='__main__': unittest.main()
