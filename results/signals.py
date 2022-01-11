#from django.db.models.signals import post_save
#from .models import SemPapers,Result
#from users.models import Profile

"""def create_results(papers,students):

    for paper in papers:
        print(paper)
        for single_student in students:
            print("single student executed")
        """

"""
def sem_papers_listener(sender,instance,created,**kwargs):
    print("created",created)
    print("instance:",instance)
    print("subjects",instance.subjects)
    sem_papers_obj=instance
    new_instance=SemPapers.objects.get(dept_sem_paper=instance)
    papers=new_instance.subjects.all()
    print("first papers:",papers)
    students=Profile.objects.filter(year_of_study=instance.year_of_study,dept=instance.dept)
    for paper in papers:
        print(paper)
        for single_student in students:
            print("single student executed")        
            Result.objects.create(
                student=single_student,
                semester=instance.semester,
                subject=paper)      

post_save.connect(sem_papers_listener,sender=SemPapers)

"""