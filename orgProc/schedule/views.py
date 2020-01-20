import json, datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from pip._vendor.distlib.locators import NAME_VERSION_RE
from datetime import datetime, timedelta
from django.db.models.aggregates import Count, Max, Min
from django.http import JsonResponse
import re


from .models import *

#
# почему в стандартной библиотеке такого нет?
# src = https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
#


def index(request): # производит редирект на другие страницы в записимости
    # pass
    if request.user.is_authenticated:
        # проверка - кем является пользователь
        user = request.user

        if (Teacher.objects.filter(user=user).count() == 1):
            # b=Teacher.objects.filter(user==user)
            return redirect('/teacher/', permanent=False)
            # return redirect(studentHome(request))
        elif (Student.objects.filter(user=user).count() == 1):
            return redirect('/student/', permanent=False)
            # return renderStudentPersonal(request)
        else:
            return redirect('/admin/', permanent=False)
    else:
        return redirect('/login/', permanent=False)

########################################################################################################################
########################################################################################################################
def teacherSc(request):
    if request.user.is_authenticated:
        # проверка - кем является пользователь
        user = request.user

        if (Teacher.objects.filter(user=user).count() == 1):
            return teacherHome(Teacher.objects.filter(user=user)[0], request)
        elif (Student.objects.filter(user=user).count() == 1):
            return redirect('/student/', permanent=False)
        else:
            return redirect('/login/', permanent=False)
    else:
        return redirect('/login/', permanent=False)
###
def studentSc(request):
    if request.user.is_authenticated:
        # проверка - кем является пользователь
        user = request.user

        if (Teacher.objects.filter(user=user).count() == 1):
            return redirect('/teacher/', permanent=False)
        elif (Student.objects.filter(user=user).count() == 1):
            return studentHome(Student.objects.filter(user=user)[0], request)
        else:
            return redirect('/login/', permanent=False)
    else:
        return redirect('/login/', permanent=False)

########################################################################################################################
########################################################################################################################
# рендер страниц
def teacherHome(curTeacher, request): # обработка запроса преподавателя
    '''
    структура передаваемых данных:
    - фио преподаватедя
    - список предметов преподавателя
        - ID
        - название предмета
        - наименование учебного плана
        - год
        - семестр
        - номер группы

    ######################################
    {pac.name}
    {pac.subjects}
        -> foreach subject in pac.subjects
            - {subject.id}
            - {subject.name}
            - {subject.planName}
            - {subject.year}
            - {subject.semestr}
            - {subject.group}
    '''
    now = datetime.now()
    planReq = Plan.objects.filter(Year=now.strftime("%Y"))
    thisSemestrPlans = [
        pl.id if Subject.objects.filter(plan_id=pl.id).aggregate(Max('FinishDay'))['FinishDay__max'] >= now.date()
                 and Subject.objects.filter(plan_id=pl.id).aggregate(Min('StartDay'))['StartDay__min'] <= now.date()
        else None for pl in planReq]  # CURSED

    thisSemestrPlansIDs = [x for x in thisSemestrPlans if x]
    subjReq = Subject.objects.filter(teacher=curTeacher, plan_id__in = thisSemestrPlansIDs)

    subjectsList = {}
    iter = 0
    for req in subjReq:
        subjectsList.update({
            iter:{
                'id': req.id,
                'name': req.Name,
                'planName': req.plan.Name,
                'year': req.plan.Year,
                'semestr': req.plan.Semester,
                'group': req.plan.group.Name,
            }

        })
        iter += 1

    pac = {
        'pac': {
            'name': curTeacher.Name,
            'subjects': subjectsList
        }

    }
    return render(request, 'teacher.html', pac)







def studentHome(curStudent, request): # обработка запроса студента
    '''
        структура передаваемых данных:
        - фио студента
        - группа студента
        - список предметов в текущем учебном плане
            - ID
            - название предмета
            - фио преподавателя

        ######################################
        {pac.name}
        {pac.group}
        {pac.subjects}
            -> foreach subject in pac.subjects
                - {subject.id}
                - {subject.name}
                - {subject.teacher}
        '''

    # получение текущего учебного плана
    '''
    1) получить группу студента
    2) получить учебные планы группы
    3) узнать текущий год
    4) отфильтровать учебные планы по тек. году // получили список семестров/триместров/четвертей
    5) узнать дату начала и дату конца учебного плана на семестр/триместр/четверь
    6) получить 1 план в период которого входит текущая дата
    '''
    studGroup = curStudent.group
    now = datetime.now()
    planReq = Plan.objects.filter(group=studGroup, Year=now.strftime("%Y"))

    curPlanIDs = [
        pl.id if Subject.objects.filter(plan_id=pl.id).aggregate(Max('FinishDay'))['FinishDay__max'] >= now.date()
                 and Subject.objects.filter(plan_id=pl.id).aggregate(Min('StartDay'))['StartDay__min'] <= now.date()
        else None  for pl in planReq] # CURSED

    uidList = [x for x in curPlanIDs if x]
    curPlan = Plan.objects.filter(id=uidList[0])[0]
    #
    SubjectsReq = Subject.objects.filter(plan=curPlan)

    subjectList = {}
    iter = 0
    for req in SubjectsReq:
        subjectList.update({
            iter: {
                'id': req.id,
                'name': req.Name,
                'teacher': req.teacher.Name,
            }
        })
        iter += 1

    pac = {
        'pac': {
            'name': curStudent.Name,
            'group': studGroup.Name,
            'subjects': subjectList,
        }
    }
    return render(request, 'student.html', pac)
########################################################################################################################
# API
'''


преподаватель
- получение информации по выбранному предмету
GET
action = teachSubj
на вход = {crfid, action, subjId}
на выход = {planId, subjName, statistics:{
        subjPass, subjAll
    }, nearLesson:{
        theme, date, time, description, type, events:{files+descr} 
    }, nextLesson:{
        theme, date, time, description, type, events:{files+descr} 
    }}
    
    
- получение плана обучения по предмету
GET
action = teachPlan
на вход = {crfid, action, planId, subjId}
на выход = {subjName, lessonTypes:{id, name}, lessons:['num':{
        id, theme, date, time, description, type, events:{files+descr} 
    ]}
    
    
- сохранение изменения блока
POST
action = teachLesson
на вход = {crfid, action, lessonId, theme, description, NewHw{}, newStuff{} ) 
на выход = {200 или 400)
###
- добавление домашней работы
POST
action = teachAddHw
на вход = {crfid, action, lessonId, name, description, file}
на выход = {200 или 400)

- удалеиние домашней работы
POST
action = teachDelHw
на вход = {crfid, action, hwId}
на выход = {200 или 400)
###
- добавление доп материаллов
POST
action = teachAddStuff
на вход = {crfid, action, lessonId, name, description, file}
на выход = {200 или 400)

- удаление доп материаллов
POST
action = teachDelStuff
на вход = {crfid, action, stuffId}
на выход = {200 или 400)
# ###########################

студент
- получение информации по выбранному предмету
GET
action = studSubj
на вход = {crfid, action, subjId}
на выход = {planId, statistics:{
        subjPass, subjAll
    }, nearLesson:{
        theme, date, time, description, type, events:{files+descr} 
    }}
    
    
- получение плана обучения по предмету
GET
action = studPlan
на вход = {crfid, action, planId, subjId}
на выход = {subjName, lessons:['num':{
        theme, date, time, description, type, events:{files+descr} 
    ]}


'''


def api(request):
    if request.is_ajax():

        action = request.POST.get('action', None) or request.GET.get('action', None)
        user = request.user
        if Teacher.objects.filter(user=user).count() == 1:  # определение преподаватея #####################################################################################
            curTeacher = Teacher.objects.filter(user=user)[0]
            for case in switch(action):
                if case('teachSubj'): # получение информации по выбранному предмету
                    subjId = request.GET.get('subjId', None)
                    match = re.search("\D", subjId)
                    if match:
                        return HttpResponse("400")

                    selSubj = Subject.objects.filter(id=subjId, teacher=curTeacher)
                    if selSubj.count() > 0:
                        selSubj = selSubj[0]
                        if Lesson.objects.filter(subject=selSubj).count() == 0:
                            return HttpResponse("500")

                        leftLessons = Lesson.objects.filter(subject=selSubj, Data__gt = datetime.now().date()).order_by('Data')
                        retNearLesson = [pacLesson(leftLessons[0]) if leftLessons.count() > 0 else "-"]
                        retNextLesson = [pacLesson(leftLessons[1]) if leftLessons.count() > 1 else "-"]
                        ret = {
                            'subjName': selSubj.Name,
                            'planId': selSubj.plan.id,
                            'statistics': {
                                'subjPass': Lesson.objects.filter(subject=selSubj, Data__lt = datetime.now().date() ).count(),
                                'subjAll': Lesson.objects.filter(subject=selSubj).count()
                            },
                            'nearLesson': retNearLesson,
                            'nextLesson': retNextLesson

                        }
                        return JsonResponse(ret, json_dumps_params={'ensure_ascii': False}, safe=False)
                    return HttpResponse("400")
                if case('teachPlan'):  # загрузка всех занятий по выбранному предмету
                    planId = request.GET.get('planId', None)
                    match = re.search("\D", planId)
                    if match:
                        return HttpResponse("400")

                    subjId = request.GET.get('subjId', None)
                    match = re.search("\D", subjId)
                    if match:
                        return HttpResponse("400")

                    selSubj = Subject.objects.filter(id=subjId, teacher=curTeacher, plan_id = planId)[0]

                    lessonsPac = {}
                    iter = 1
                    for req in Lesson.objects.filter(subject=selSubj).order_by('Data'):
                        lessonsPac.update({
                            iter: pacLesson(req)
                        })
                        iter+=1


                    ret = {
                        'subjName': selSubj.Name,
                        'lessonTypes': [{req.id: req.Name} for req in LesType.objects.all()],
                        'lessons': lessonsPac

                    }
                    return JsonResponse(ret, json_dumps_params={'ensure_ascii': False}, safe=False)
                if case('teachLesson'):  # сохранение измнения занятия по предмету
                    #  action, lessonId, theme, description, typeId
                    lessonId = request.POST.get('lessonId', None)
                    match = re.search("\D", lessonId)
                    if match:
                        return HttpResponse("400")

                    theme = request.POST.get('theme', None)
                    descr = request.POST.get('description', None)

                    selLesson = Lesson.objects.filter(id=lessonId, subject__teacher=curTeacher)
                    if selLesson.count() > 0 and theme and descr:
                        selLesson = selLesson[0]
                        selLesson.Theme = theme
                        selLesson.Description = descr
                        selLesson.save()
                    else:
                        return HttpResponse("400")

                    return HttpResponse("200")
                if case('teachAddHw'):
                    # action, lessonId, name, description, file
                    lessonId = request.POST.get('lessonId', None)
                    match = re.search("\D", lessonId)
                    if match:
                        return HttpResponse("400")

                    name = request.POST.get('name', None)
                    description = request.POST.get('description', None)
                    myFile = request.FILES.get('file', None)
                    # # #
                    curLesson = Lesson.objects.filter(id=lessonId, subject__teacher=curTeacher)
                    # if (curLesson.count() > 0):
                    #     curLesson = curLesson[0]
                    #     newHW = HW(Name=name, lesson=curLesson, Description=description, Dls=myFile)
                    #     newHW.save()
                    # else:
                    #     return HttpResponse("400")
                    return HttpResponse("200")
                if case('teachDelHw'):

                    return HttpResponse("200")

                if case():
                    return HttpResponse("400")
            return HttpResponse("500")
        elif (Student.objects.filter(user=user).count() == 1):  # определение студента #####################################################################################
            curStudent = Student.objects.filter(user=user)[0]
            for case in switch(action):
                if case('teachSubj'):  # получение информации по выбранному предмету
                    subjId = request.GET.get('subjId', None)
                    match = re.search("\D", subjId)
                    if match:
                        return HttpResponse("400")

                    selSubj = getParticipatedSubj(curStudent, subjId)
                    if selSubj.count() > 0:
                        selSubj = selSubj[0]
                        if Lesson.objects.filter(subject=selSubj).count() == 0:
                            return HttpResponse("500")

                        leftLessons = Lesson.objects.filter(subject=selSubj, Data__gt = datetime.now().date()).order_by('Data')
                        retNearLesson = [pacLesson(leftLessons[0]) if leftLessons.count() > 0 else "-"]
                        ret = {
                            'subjName': selSubj.Name,
                            'planId': selSubj.plan.id,
                            'statistics': {
                                'subjPass': Lesson.objects.filter(subject=selSubj, Data__lt = datetime.now().date() ).count(),
                                'subjAll': Lesson.objects.filter(subject=selSubj).count()
                            },
                            'nearLesson': retNearLesson

                        }
                        return JsonResponse(ret, json_dumps_params={'ensure_ascii': False}, safe=False)
                    return HttpResponse("400")
                    # 
                if case('teachPlan'):  # загрузка всех занятий по выбранному предмету
                    planId = request.GET.get('planId', None)
                    match = re.search("\D", planId)
                    if match:
                        return HttpResponse("400")

                    subjId = request.GET.get('subjId', None)
                    match = re.search("\D", subjId)
                    if match:
                        return HttpResponse("400")

                    selSubj = getParticipatedSubj(curStudent, subjId)[0]

                    lessonsPac = {}
                    iter = 1
                    for req in Lesson.objects.filter(subject=selSubj).order_by('Data'):
                        lessonsPac.update({
                            iter: pacLesson(req)
                        })
                        iter+=1


                    ret = {
                        'subjName': selSubj.Name,
                        'lessonTypes': [{req.id: req.Name} for req in LesType.objects.all()],
                        'lessons': lessonsPac

                    }
                    return JsonResponse(ret, json_dumps_params={'ensure_ascii': False}, safe=False)
                if case():
                    return HttpResponse("400")
            return HttpResponse("500")
        else:
            return HttpResponse("<h1>this is an  ajax API</h1><p>please read the specification link: [REDACTED]")

    else:
        return HttpResponse("<h1>this is an API</h1><p>please read the specification link: [REDACTED]")


def pacLesson(lesson):
    return  {
        'id': lesson.id,
        'theme': lesson.Theme,
        'date': lesson.Data,
        'time': lesson.klass.Start.strftime("%H:%M") + " - " + lesson.klass.Finish.strftime("%H:%M"),
        'description': lesson.Description,
        'type': lesson.subject.LessonType.Name,
        'events': {
            'HW': [
                {'id': stuff.id, 'name': stuff.Name, 'description': stuff.Description, 'dls': stuff.Dls.url}
                for stuff in HW.objects.filter(lesson=lesson)
            ],
            'AddStuff': [
                {'id': stuff.id, 'name': stuff.Name, 'description': stuff.Description, 'dls': stuff.Dls.url}
                for stuff in AddStuff.objects.filter(lesson=lesson)
            ]
        }
    }
def getParticipatedSubj(SelStudent, subjId):
    return Subject.objects.filter(id=subjId, plan__group__id=SelStudent.group.id)
