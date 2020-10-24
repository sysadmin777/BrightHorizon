from django.db import models

# Create your models here.
#Graduation, Certification, Get a Job

#12 credits, 24 credits, 36 credits, done (GPA 3.7+ = bonus points)
#take practice exam and pass, pass exam (bonus task take online class)
#Meet career counsoler, build portfolio, get interview, get hired
#Each full objective = 100 points

class goal(models.Model):
    goal_title = models.TextField()
    def __str__(self):
        return self.goal_title

class task(models.Model):
    task_title = models.TextField()
    goal = models.ForeignKey(goal, on_delete=models.CASCADE)
    is_bonus = models.BooleanField(default=False)
    def __str__(self):
        return self.task_title

class UserGoal(models.Model):
    goal = models.ForeignKey(goal, on_delete=models.CASCADE)
    goal_complete = models.BooleanField(default=False)
    suggested_complete_date = models.DateField()
    owner = models.TextField()
    def __str__(self):
        return self.goal

class UserCompletedTasks(models.Model):
    goal = models.ForeignKey(UserGoal, on_delete=models.CASCADE)
    task_completed = models.ForeignKey(task, on_delete=models.CASCADE)
    points = models.IntegerField()
    owner = models.TextField()
    def __str__(self):
        return self.goal