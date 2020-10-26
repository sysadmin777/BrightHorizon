from django.contrib import admin
from main.models import goal, task, UserGoal, UserCompletedTasks
# Register your models here.
admin.site.register(goal)
admin.site.register(task)
admin.site.register(UserGoal)
admin.site.register(UserCompletedTasks)