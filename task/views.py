from django.shortcuts import render, redirect
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from .models import TaskItem
from django.utils.decorators import method_decorator

class ListView(View):
    def get(self, request):
        root_list = TaskItem.objects.filter(parent=None, deleted=False)
        html_content = self.get_child_tasks(root_list, None)
        html_content += ''' 
        <form method="POST" action="/task/add"> 
            <input name="id" value="-1" type="hidden" />
            <input type="text" class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="task" name="item" />
            <input class="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded" type="submit" />
        </form>'''       
        return render(request, 'task/list_view.html', {'html_content': html_content})

    def get_child_tasks(self, items, html_content):
        html_content = ""
        if items is None:
            return html_content
        html_content += "<ol class='list-none ml-12 py-3'>"
        
        for item in items:
            form_content = ''' 
            <form method="POST" action="/task/add" id="'''+str(item.id)+'''" class="inp_form"> 
                <input name="id" value="'''+str(item.id)+'''" type="hidden" />
                <input type="text" class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="add subtask here" name="item" />
                <input class="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded" type="submit" />
            </form>'''
            is_done = ['<strike>', '</strike>'] if item.completed else ['', '']
            done_item = ''' <a href="/task/complete/{0}"> Done </a> |'''.format(str(item.id)) if not item.completed else ''
            html_content += "<li>" + is_done[0] + item.item + '<div class="text-blue-500">' + done_item + " <a href=/task/delete/"+str(item.id)+" >Delete</a> " + '</div>' + is_done[1] + form_content
            html_content += self.get_child_tasks(TaskItem.objects.filter(parent=item, deleted=False), html_content)
            html_content += "</li> "
        html_content += "</ol>"
        
        return html_content

class DeleteItem(View):
    def get(self, request, id):
        TaskItem.objects.filter(id=id).update(deleted=True)
        return redirect('/task')

class CompleteItem(View):
    def get(self, request, id):
        TaskItem.objects.filter(id=id).update(completed=True)
        return redirect('/task')

@method_decorator(csrf_exempt, name='dispatch')
class AddItem(View):
    def post(self, request):
        if request.method=="POST":
            id = request.POST.get("id")
            item = request.POST.get("item")
            if (id!='-1'):
                parent = TaskItem.objects.get(id=id, deleted=False)
            else:
                parent = None
            item = TaskItem.objects.create(item=item, parent=parent)
        return redirect('/task')
    
    def get(self, request):
        return redirect('/task')

class StartOver(View):
    def get(self, request):
        TaskItem.objects.all().delete()
        return redirect('/task')
    
