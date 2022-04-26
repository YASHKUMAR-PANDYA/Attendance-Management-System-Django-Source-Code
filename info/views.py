from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Dept, Class, Student,  Teacher,  User, time_slots, PunchAttendancelog, Punchstatus


# Create your views here.


@login_required
def index(request):
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    return render(request, 'info/logout.html')


# @login_required()
# def attendance(request, stud_id):
#     stud = Student.objects.get(USN=stud_id)
#     ass_list = Assign.objects.filter(class_id_id=stud.class_id)
#     att_list = []
#     for ass in ass_list:
#         try:
#             a = AttendanceTotal.objects.get(student=stud, course=ass.course)
#         except AttendanceTotal.DoesNotExist:
#             a = AttendanceTotal(student=stud, course=ass.course)
#             a.save()
#         att_list.append(a)
#     return render(request, 'info/attendance.html', {'att_list': att_list})


# @login_required()
# def attendance_detail(request, stud_id, course_id):
#     stud = get_object_or_404(Student, USN=stud_id)
#     cr = get_object_or_404(Course, id=course_id)
#     att_list = Attendance.objects.filter(
#         course=cr, student=stud).order_by('date')
#     return render(request, 'info/att_detail.html', {'att_list': att_list, 'cr': cr})


# Teacher Views

# @login_required
# def t_clas(request, teacher_id, choice):
#     teacher1 = get_object_or_404(Teacher, id=teacher_id)
#     return render(request, 'info/t_clas.html', {'teacher1': teacher1, 'choice': choice})


# @login_required()
# def t_student(request, assign_id):
#     ass = Assign.objects.get(id=assign_id)
#     att_list = []
#     for stud in ass.class_id.student_set.all():
#         try:
#             a = AttendanceTotal.objects.get(student=stud, course=ass.course)
#         except AttendanceTotal.DoesNotExist:
#             a = AttendanceTotal(student=stud, course=ass.course)
#             a.save()
#         att_list.append(a)
#     return render(request, 'info/t_students.html', {'att_list': att_list})


# @login_required()
# def t_class_date(request, assign_id):
#     now = timezone.now()
#     ass = get_object_or_404(Assign, id=assign_id)
#     curr = AttendanceClass.objects.filter(date=datetime.date(datetime.now()))
#     if curr:
#         pass
#     else:
#         att_create = AttendanceClass.objects.create(
#             assign=ass, date=datetime.date(datetime.now()))
#     att_create.save()
#     att_list = ass.attendanceclass_set.filter(
#         date=datetime.date(datetime.now()))
#     return render(request, 'info/t_class_date.html', {'att_list': att_list})


# @login_required()
# def cancel_class(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     assc.status = 2
#     assc.save()
#     return HttpResponseRedirect(reverse('t_class_date', args=(assc.assign_id,)))


# @login_required()
# def t_attendance(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     ass = assc.assign
#     c = ass.class_id
#     context = {
#         'ass': ass,
#         'c': c,
#         'assc': assc,
#     }
#     return render(request, 'info/t_attendance.html', context)

# My view--> starts


@login_required()
def p_attendance(request, u_id):
    context = {}
    obj = get_object_or_404(Punchstatus, user=u_id)
    # pobj = get_object_or_404(PunchAttendancelog, user=u_id)

    error = ""
    error1 = ""

    user = request.user
    dt = datetime.now()
    if request.method == "POST":
        pval = request.POST["punch"]
        if pval == "punchin":
            PunchAttendancelog.objects.create(
                user=user, PINstatus=True, PunchIn=dt, PunchValue=pval)
            if user:
                Punchstatus.objects.filter(user=user).update(status=True)
                error = "no"
            else:
                # else:
                #     Punchstatus.objects.create(user=user, status=True)
                error = "yes"
        elif pval == "punchout":
            rev = request.POST.get("review", False)
            if rev == "":
                error1 = "yes"
            else:
                PunchAttendancelog.objects.create(
                    user=user, PINstatus=False, PunchOut=dt, PunchValue=pval, PunchOutReview=rev)
                Punchstatus.objects.filter(user=user).update(status=False)
                error1 = "no"
            # if rev:
            #     PunchAttendancelog.objects.create(user=user, PINstatus=False, PunchOut=dt, Punchvalue=pval)
            #     Punchstatus.objects.filter(user=user).update(status=False)
            #     error="no"
            # else:
            #     error="yes"
    # context["pobj"] = pobj
    context["error"] = error
    context["obj"] = obj
    context["error1"] = error1

    return render(request, "info/P_Attendance_UI.html", context)


@login_required()
def s_report(request, u_id):
    context = {}
    user = request.user
    sc_list = PunchAttendancelog.objects.filter(user=user).order_by('-id')
    context["sc_list"] = sc_list
    return render(request, "info/s_report.html", context)
# MY view--> ends


# @login_required()
# def edit_att(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     cr = assc.assign.course
#     att_list = Attendance.objects.filter(attendanceclass=assc, course=cr)
#     context = {
#         'assc': assc,
#         'att_list': att_list,
#     }
#     return render(request, 'info/t_edit_att.html', context)


# @login_required()
# def confirm(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     ass = assc.assign
#     cr = ass.course
#     cl = ass.class_id
#     for i, s in enumerate(cl.student_set.all()):
#         status = request.POST[s.USN]
#         if status == 'present':
#             status = 'True'
#         else:
#             status = 'False'
#         if assc.status == 1:
#             try:
#                 a = Attendance.objects.get(
#                     course=cr, student=s, date=assc.date, attendanceclass=assc)
#                 a.status = status
#                 a.save()
#             except Attendance.DoesNotExist:
#                 a = Attendance(course=cr, student=s, status=status,
#                                date=assc.date, attendanceclass=assc)
#                 a.save()
#         else:
#             a = Attendance(course=cr, student=s, status=status,
#                            date=assc.date, attendanceclass=assc)
#             a.save()
#             assc.status = 1
#             assc.save()

#     return HttpResponseRedirect(reverse('t_class_date', args=(ass.id,)))


# @login_required()
# def t_attendance_detail(request, stud_id, course_id):
#     stud = get_object_or_404(Student, USN=stud_id)
#     cr = get_object_or_404(Course, id=course_id)
#     att_list = Attendance.objects.filter(
#         course=cr, student=stud).order_by('date')
#     return render(request, 'info/t_att_detail.html', {'att_list': att_list, 'cr': cr})


# @login_required()
# def change_att(request, att_id):
#     a = get_object_or_404(Attendance, id=att_id)
#     a.status = not a.status
#     a.save()
#     return HttpResponseRedirect(reverse('t_attendance_detail', args=(a.student.USN, a.course_id)))


# @login_required()
# def t_extra_class(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     c = ass.class_id
#     context = {
#         'ass': ass,
#         'c': c,
#     }
#     return render(request, 'info/t_extra_class.html', context)


# @login_required()
# def e_confirm(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     cr = ass.course
#     cl = ass.class_id
#     assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
#     assc.save()

#     for i, s in enumerate(cl.student_set.all()):
#         status = request.POST[s.USN]
#         if status == 'present':
#             status = 'True'
#         else:
#             status = 'False'
#         date = request.POST['date']
#         a = Attendance(course=cr, student=s, status=status,
#                        date=date, attendanceclass=assc)
#         a.save()

#     return HttpResponseRedirect(reverse('t_clas', args=(ass.teacher_id, 1)))


# @login_required()
# def t_report(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     sc_list = []
#     for stud in ass.class_id.student_set.all():
#         a = StudentCourse.objects.get(student=stud, course=ass.course)
#         sc_list.append(a)
#     return render(request, 'info/t_report.html', {'sc_list': sc_list})


# @login_required()
# def timetable(request, class_id):
#     asst = AssignTime.objects.filter(assign__class_id=class_id)
#     matrix = [['' for i in range(12)] for j in range(6)]

#     for i, d in enumerate(DAYS_OF_WEEK):
#         t = 0
#         for j in range(12):
#             if j == 0:
#                 matrix[i][0] = d[0]
#                 continue
#             if j == 4 or j == 8:
#                 continue
#             try:
#                 a = asst.get(period=time_slots[t][0], day=d[0])
#                 matrix[i][j] = a.assign.course_id
#             except AssignTime.DoesNotExist:
#                 pass
#             t += 1

#     context = {'matrix': matrix}
#     return render(request, 'info/timetable.html', context)


# @login_required()
# def t_timetable(request, teacher_id):
#     asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
#     class_matrix = [[True for i in range(12)] for j in range(6)]
#     for i, d in enumerate(DAYS_OF_WEEK):
#         t = 0
#         for j in range(12):
#             if j == 0:
#                 class_matrix[i][0] = d[0]
#                 continue
#             if j == 4 or j == 8:
#                 continue
#             try:
#                 a = asst.get(period=time_slots[t][0], day=d[0])
#                 class_matrix[i][j] = a
#             except AssignTime.DoesNotExist:
#                 pass
#             t += 1

#     context = {
#         'class_matrix': class_matrix,
#     }
#     return render(request, 'info/t_timetable.html', context)


# @login_required()
# def free_teachers(request, asst_id):
#     asst = get_object_or_404(AssignTime, id=asst_id)
#     ft_list = []
#     t_list = Teacher.objects.filter(
#         assign__class_id__id=asst.assign.class_id_id)
#     for t in t_list:
#         at_list = AssignTime.objects.filter(assign__teacher=t)
#         if not any([True if at.period == asst.period and at.day == asst.day else False for at in at_list]):
#             ft_list.append(t)

#     return render(request, 'info/free_teachers.html', {'ft_list': ft_list})


# # student marks


# @login_required()
# def marks_list(request, stud_id):
#     stud = Student.objects.get(USN=stud_id, )
#     ass_list = Assign.objects.filter(class_id_id=stud.class_id)
#     sc_list = []
#     for ass in ass_list:
#         try:
#             sc = StudentCourse.objects.get(student=stud, course=ass.course)
#         except StudentCourse.DoesNotExist:
#             sc = StudentCourse(student=stud, course=ass.course)
#             sc.save()
#             sc.marks_set.create(type='I', name='Internal test 1')
#             sc.marks_set.create(type='I', name='Internal test 2')
#             sc.marks_set.create(type='I', name='Internal test 3')
#             sc.marks_set.create(type='E', name='Event 1')
#             sc.marks_set.create(type='E', name='Event 2')
#             sc.marks_set.create(type='S', name='Semester End Exam')
#         sc_list.append(sc)

#     return render(request, 'info/marks_list.html', {'sc_list': sc_list})


# # teacher marks


# @login_required()
# def t_marks_list(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     m_list = MarksClass.objects.filter(assign=ass)
#     return render(request, 'info/t_marks_list.html', {'m_list': m_list})


# @login_required()
# def t_marks_entry(request, marks_c_id):
#     mc = get_object_or_404(MarksClass, id=marks_c_id)
#     ass = mc.assign
#     c = ass.class_id
#     context = {
#         'ass': ass,
#         'c': c,
#         'mc': mc,
#     }
#     return render(request, 'info/t_marks_entry.html', context)


# @login_required()
# def marks_confirm(request, marks_c_id):
#     mc = get_object_or_404(MarksClass, id=marks_c_id)
#     ass = mc.assign
#     cr = ass.course
#     cl = ass.class_id
#     for s in cl.student_set.all():
#         mark = request.POST[s.USN]
#         sc = StudentCourse.objects.get(course=cr, student=s)
#         m = sc.marks_set.get(name=mc.name)
#         m.marks1 = mark
#         m.save()
#     mc.status = True
#     mc.save()

#     return HttpResponseRedirect(reverse('t_marks_list', args=(ass.id,)))


# @login_required()
# def edit_marks(request, marks_c_id):
#     mc = get_object_or_404(MarksClass, id=marks_c_id)
#     cr = mc.assign.course
#     stud_list = mc.assign.class_id.student_set.all()
#     m_list = []
#     for stud in stud_list:
#         sc = StudentCourse.objects.get(course=cr, student=stud)
#         m = sc.marks_set.get(name=mc.name)
#         m_list.append(m)
#     context = {
#         'mc': mc,
#         'm_list': m_list,
#     }
#     return render(request, 'info/edit_marks.html', context)


# @login_required()
# def student_marks(request, assign_id):
#     ass = Assign.objects.get(id=assign_id)
#     sc_list = StudentCourse.objects.filter(
#         student__in=ass.class_id.student_set.all(), course=ass.course)
#     return render(request, 'info/t_student_marks.html', {'sc_list': sc_list})
