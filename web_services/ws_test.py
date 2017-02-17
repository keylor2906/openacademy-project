import functools
import xmlrpclib
HOST = 'localhost'
PORT = 8069
DB = 'odoo_curso'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
model = 'openacademy.session'
domain = []
method_name = 'search_read'
sessions = call(model, method_name, domain, ['name','seats','taken_seats'])
for session in sessions:
    print "Session %s (%s seats), taken seats %d" % (session['name'], session['seats'], session['taken_seats'])

# Read course
method_name='search'
domain = [('name','=','Curso Odoo 1')]
course_ids = call('openacademy.course', method_name,domain)
course_id = course_ids[0]

# 3.create a new session
responsible_id = call('res.partner', 'search', [('name', '=', 'Vauxoo')])[0]
print "responsible_id", responsible_id

method_name = 'create'
new_session_id = call(model, method_name, {
    'name' : 'Session from ws',
    'instructor_id': responsible_id,
    'course_id' : course_id,
    # 'attendee_ids': [(4, responsible_id)],
    'attendee_ids': [(4, 7), (4, 3)],
})
