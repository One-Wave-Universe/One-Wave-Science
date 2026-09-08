import unittest
from fractions import Fraction
from translator_variants import FAMILIES, top, recover, packets

class Variants(unittest.TestCase):
    def test_known_packets(self):
        p = packets(26, 'original')
        self.assertEqual([(r['x'], r['top'], r['wrapper']) for r in p if r['n']==1],
                         [(-1,'-2','-1'),(-1,'-2','-3'),(1,'2','1'),(1,'2','3')])
        self.assertEqual(top(1,'odd_up'), 3)
        self.assertEqual(top(2,'odd_up'), 5)

    def test_roundtrip_every_family(self):
        for family, (_, steps, _) in FAMILIES.items():
            for k in steps:
                for n in range(1, 27):
                    self.assertEqual(recover(top(n,family,k),family,k),n)

    def test_order_remains_distinct(self):
        self.assertNotEqual(top(5,'subtract_then_half',1),top(5,'half_then_subtract',1))
        self.assertEqual(top(3,'ascending_after',2),top(3,'ascending_before',1))

    def test_wrapper_parity_and_rational_domain(self):
        for family, (_, steps, _) in FAMILIES.items():
            for k in steps:
                for r in packets(26,family,k):
                    t,w = Fraction(r['top']), Fraction(r['wrapper'])
                    self.assertEqual(abs(w-t),1)
                    if t.denominator == 1:
                        self.assertNotEqual(int(t)%2,int(w)%2)
                    else:
                        self.assertIsNone(r['top_parity'])

    def test_inversion_couples_side_not_sign(self):
        normal = packets(26,'original')
        inverse = packets(26,'original',inverted=True)
        self.assertEqual(normal[0]['label'],'A')
        self.assertEqual(inverse[0]['label'],'Z')
        for a,b in zip(normal,inverse):
            self.assertEqual(a['top'],b['top'])
            self.assertEqual(Fraction(a['wrapper'])+Fraction(b['wrapper']),2*Fraction(a['top']))

    def test_opposing_reverses_order_only(self):
        forward=packets(12,'odd_up')
        reverse=packets(12,'odd_up',opposing=True)
        self.assertEqual(reverse[0]['n'],12)
        self.assertEqual({(r['x'],r['top'],r['wrapper']) for r in forward},
                         {(r['x'],r['top'],r['wrapper']) for r in reverse})

    def test_input_validation(self):
        for value in (True,0,-1,1.5):
            with self.assertRaises(ValueError): top(value,'original')
        with self.assertRaises(ValueError): top(1,'ascending_after',0)
        with self.assertRaises(ValueError): top(1,'original',1)

    def test_recover_from_signed_oriented_wrapper(self):
        for family, (_,steps,_) in FAMILIES.items():
            for k in steps:
                for inverted in (False,True):
                    for opposing in (False,True):
                        for r in packets(26,family,k,inverted,opposing):
                            t = r['sign']*Fraction(r['wrapper']) - (-1 if inverted else 1)*r['logical_side']
                            self.assertEqual(recover(t,family,k),r['n'])

    def test_corrected_odd_b(self):
        b=[r for r in packets(26,'odd_up') if r['n']==2 and r['sign']==1]
        self.assertEqual([(r['x'],r['top'],r['wrapper']) for r in b],[(2,'5','4'),(2,'5','6')])

    def test_unbounded_ladder_examples(self):
        for n in range(1,27):
            for k in (1,2,3,26,100,1000):
                self.assertEqual(top(n,'ascending_after',2*k),top(n,'ascending_before',k))
                self.assertEqual(top(n,'subtract_then_half',2*k),top(n,'half_then_subtract',k))
                for family in ('ascending_before','ascending_after','subtract_then_half','half_then_subtract'):
                    self.assertEqual(recover(top(n,family,k),family,k),n)

if __name__=='__main__': unittest.main()
