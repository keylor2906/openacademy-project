# -*- encoding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class GlobalTestOpenAcademySession(TransactionCase):
    '''
    Global test to openacademy session model.
    Test create session and trigger constraints.
    '''
    # Pseudo-constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner_vauxoo = self.env.ref('base.res_partner_23').id
        self.course = self.env.ref('openacademy.course1')
        self.partner_attendee = self.env.ref('base.res_partner_5').id

    # Generic methods
    # def create_session(self, name, )

    # Test methods
    def test_10_instructor_is_attendee(self):
        '''
        Check that raise of 'A session's instructor can't be an attendee'
        '''
        with self.assertRaisesRegexp(
                ValidationError,
                "A session's instructor can't be an attendee"
            ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'course_id': 1,
                'instructor_id': self.partner_vauxoo,
                'attendee_ids': [(6, 0, [self.partner_vauxoo])],
            })

    def test_20_wkf_done(self):
        '''
        Checks that the workflow works fine!
        '''
        session_test = self.session.create({
                'name': 'Session test 1',
                'seats': 10,
                'course_id': 1,
                'instructor_id': self.partner_vauxoo,
                'attendee_ids': [(6, 0, [self.partner_attendee])],
            })
        # Check inital state
        self.assertEqual(session_test.state, 'draft', 'Initial state should be on draft')
        session_test.signal_workflow('confirm')

        # Check next tate and check it
        self.assertEqual(session_test.state, 'confirmed', 'State should be on confirmed')
        session_test.signal_workflow('done')

        # Check next tate and check it 
        self.assertEqual(session_test.state, 'done', 'State should be on done')
