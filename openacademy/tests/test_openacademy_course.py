# -*- encoding: utf-8 -*-

from psycopg2 import IntegrityError

from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    '''
    Global test to openacademy course model.
    Test create course and trigger constraints.
    '''

    # Method pseudo-constructor of test setUp
    def setUp(self):
        #Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'hello world'
        self.course = self.env['openacademy.course']

    # Method of class that isn't test.
    def create_course(self, course_name, course_description, 
                      course_responsible_id):
        # create a course with received parameters
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id,
        })
        return course_id

    # Method of test startswith 'def test_*(self)'

    # Mute the error to avoid it in log
    @mute_logger('openerp.sql_db')
    def test_01_same_name_description(self):
        '''
        Test create a course with same name and description.
        To test constraint of different name and description.
        '''
        # Error raised excpected with message expected
        with self.assertRaisesRegexp(
                IntegrityError,
                'new row for relation "openacademy_course" violates'
                ' check constraint "openacademy_course_name_description_check"'
                ):
            # Create a course with same name and description to raise error
            self.create_course('test', 'test', None)
