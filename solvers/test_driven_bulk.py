import unittest
import json
from dataclasses import replace
import numpy as np
from bulk_excitation import BulkExcitation, BulkCoefficients
from driven_bulk import (DrivenBulk, potential, driven_step, external_energy,
                         applied_force, centroid_chart, prepare_linear_packet)
from joint_boundary_response import OFFSETS

class DriveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=BulkExcitation(12);cls.f=cls.m.seed().astype(complex)

    def test_valid_centroid_receipt_serializes(self):
        d=DrivenBulk(self.m,self.f)
        self.assertTrue(d.chart['valid'])
        json.dumps(d.measurements(self.f),allow_nan=False)
        self.assertIs(type(d.measurements(self.f)['centroid']['geometrically_resolved']),bool)

    def test_zero_force_matches_original_law(self):
        np.testing.assert_array_equal(driven_step(self.m,self.f,.02,[0,0,0]),self.m.step(self.f,.02))
        q=driven_step(self.m,self.f,.02,[.01,-.02,0])
        np.testing.assert_allclose(driven_step(self.m,q,-.02,[.01,-.02,0]),self.f,atol=1e-12)

    def test_switch_work_and_translation_work(self):
        m=self.m;field=self.f.copy();d=DrivenBulk(m,field)
        field=driven_step(m,field,.02,[0,0,0])
        for force in ([.01,0,0],[0,-.01,.02],[0,0,0]):
            old=d.total_energy(field);work=d.set_force(field,force)
            self.assertAlmostEqual(d.total_energy(field)-old,work,places=13)
            event=d.events[-1]
            independent=m.volume*np.dot(potential(m,event['new_force'])-potential(m,event['old_force']),event['density'])
            self.assertAlmostEqual(independent,work,places=13)
        after=np.roll(m.full(field),(1,1,0),axis=(0,1,2))[m.mask]
        old=d.total_energy(field);d.intervention(field,after,[1,1,0])
        self.assertAlmostEqual(d.events[-1]['work'],d.total_energy(after)-old,places=13)
        event=d.events[-1]
        independent=m.volume*np.dot(potential(m,event['force']),np.array(event['after_density'])-event['before_density'])+event['internal_energy_change']
        self.assertAlmostEqual(independent,event['work'],places=13)
        self.assertEqual(event['shift_in_lattice_indices'],[1,1,0])

    def test_force_is_potential_gradient(self):
        m=self.m;force=np.array([.01,-.01,.005]);n=np.sum(abs(self.f)**2,axis=1)
        h=1e-5;original=m.xyz.copy();numerical=[]
        try:
            for j in range(3):
                m.xyz=original.copy();m.xyz[:,j]+=h;plus=external_energy(m,self.f,force)
                m.xyz=original.copy();m.xyz[:,j]-=h;minus=external_energy(m,self.f,force)
                numerical.append(-(plus-minus)/(2*h))
        finally:m.xyz=original
        np.testing.assert_allclose(applied_force(m,self.f,force),numerical,atol=1e-10)

    def test_static_nonlinear_energy_norm_refinement(self):
        errors=[]
        for dt in [.04,.02,.01]:
            d=DrivenBulk(self.m,self.f);f=self.f.copy();d.set_force(f,[.01,0,0])
            for _ in range(round(1/dt)):f=d.advance(f,dt)
            r=d.measurements(f);self.assertLess(r['max_norm_relative_error'],1e-10)
            errors.append(r['max_balance_error'])
        self.assertLess(errors[0],1e-4)
        self.assertLess(errors[1],errors[0]/3.5);self.assertLess(errors[2],errors[1]/3.5)

    def test_periodic_centroid_crossing_and_ambiguity(self):
        m=self.m;field=m.seed(width=.6).astype(complex);previous=None;start=None
        for k in range(18):
            chart=centroid_chart(m,field,previous);self.assertTrue(chart['valid'])
            current=np.array(chart['position']);start=current.copy() if start is None else start
            np.testing.assert_allclose(current-start,[k/np.sqrt(2),k/np.sqrt(2),0],atol=1e-10)
            previous=current;field=np.roll(m.full(field),(1,1,0),axis=(0,1,2))[m.mask]
        self.assertFalse(centroid_chart(m,np.ones_like(field))['valid'])
        antipodal=self.f+np.roll(m.full(self.f),(6,0,0),axis=(0,1,2))[m.mask]
        self.assertFalse(centroid_chart(m,antipodal)['valid'])

    def test_lowest_band_projection_and_qzero_hessian(self):
        m=BulkExcitation(16,coefficients=replace(BulkCoefficients(),focusing=0,saturation=0))
        field,leak=prepare_linear_packet(m,1,2)
        self.assertLess(leak,1e-12);self.assertAlmostEqual(m.norm(field),1,places=12)
        offsets=np.array(OFFSETS)/np.sqrt(2)
        def eig(q):
            symbol=np.sum(1-np.cos(offsets@q))
            return np.linalg.eigvalsh(symbol*m.C/12+m.c.phase_lock*m.R)[0]
        errors=[]
        for h in [.02,.01,.005]:
            curvature=(eig([h,0,0])+eig([-h,0,0])-2*eig([0,0,0]))/h**2
            errors.append(abs(curvature-.3))
        self.assertLess(errors[2],1e-6);self.assertLess(errors[1],errors[0]/3.8)
        self.assertLess(errors[2],errors[1]/3.8)

    def test_invalid_force_and_event_budget(self):
        d=DrivenBulk(self.m,self.f)
        for f in ([.03,0,0],[float('nan'),0,0],[0,0],[False,0,0],['0.01',0,0]):
            with self.assertRaises(ValueError):d.set_force(self.f,f)
        for _ in range(64):d.set_force(self.f,[0,0,0])
        with self.assertRaises(ValueError):d.set_force(self.f,[0,0,0])

if __name__=='__main__':unittest.main()
