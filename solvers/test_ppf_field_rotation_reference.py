"""Kinematic control tests for G-770, no physical validation."""
import math
import unittest
from ppf_field_rotation_reference import (
    compose, field_angle, field_rate, laboratory_child_vector, rotate, wrap
)

class FieldRotationTests(unittest.TestCase):
    def test_zero_angles(self):
        self.assertAlmostEqual(compose(0,0,0),0)
    def test_nested_rotation_matches_composed_rotation(self):
        for f,p,q in [(0.3,-0.7,1.2),(2.1,1.3,-0.4),(-2.5,0.2,1.1)]:
            x,y=laboratory_child_vector(f,p,q)
            a,b=rotate(compose(f,p,q),1,0)
            self.assertAlmostEqual(x,a,places=12)
            self.assertAlmostEqual(y,b,places=12)
    def test_periodicity(self):
        self.assertAlmostEqual(wrap(compose(0.3,0.5,0.7)-compose(0.3+2*math.pi,0.5,0.7)),0,places=12)
    def test_rotating_field_rate(self):
        for theta in [0,0.7,2.2]:
            w=3.2
            bx,by=math.cos(theta),math.sin(theta)
            self.assertAlmostEqual(field_angle(bx,by),theta,places=12)
            self.assertAlmostEqual(field_rate(bx,by,-w*by,w*bx),w,places=12)
    def test_zero_field_is_undefined(self):
        with self.assertRaises(ValueError): field_angle(0,0)
        with self.assertRaises(ValueError): field_rate(0,0,1,0)
    def test_field_rate_scales_with_time_not_amplitude(self):
        for a in [0.1,1,20]:
            bx,by=a*0.6,a*0.8
            w=-2.0
            self.assertAlmostEqual(field_rate(bx,by,-w*by,w*bx),w,places=12)

if __name__=="__main__":
    unittest.main()
