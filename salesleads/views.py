from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from simple_history.utils import update_change_reason
from django.utils import timezone
from django import template

from salesleads.multiform import MultiFormsView

from salesleads.forms import (
    ChangeUserForm,
    ContactPersonForm,
    CommentForm,
    CountryForm,
    LoginForm,
    MyGeoForm,
    PlannedActivitiesAddForm,
    PlannedActivitiesUpdateForm,
    SalesLeadAddForm,
    SalesLeadAddressAddForm,
    ReportForm
)
from salesleads.models import Comment, ExportUser, SalesLead, PlannedActivities, ContactPerson, Country, STATUS


def get_saleslead(id):
    return SalesLead.objects.get(pk=id)


def get_user(id):
    return ExportUser.objects.get(pk=id)


def get_user_id(username):
    return ExportUser.objects.get(username=username).id


def is_valid_query(param):
    return param != '' and param is not None and param != 'None'


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(request, 'salesleads/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            export_user = authenticate(**form.cleaned_data)
            if export_user is not None:
                login(request, export_user)
                return redirect('dashboard')
        return render(request, 'salesleads/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')


class UserListView(ListView):
    model = ExportUser
    template_name = 'salesleads/users.html'


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        salesleads = SalesLead.objects.filter(user=user)
        activities = PlannedActivities.objects.filter(user=user).filter(
            Q(activity_done=False) | Q(activity_done=None)).filter(date__gte=timezone.now()).order_by('date')
        status_one = 0
        status_two = 0
        status_three = 0
        status_four = 0
        status_five = 0

        page_number = request.GET.get('page')

        # Time filters for 1st sector
        this_week = request.GET.get('this_week')
        this_month = request.GET.get('this_month')
        this_quarter = request.GET.get('this_quarter')
        this_year = request.GET.get('this_year')
        last_year = request.GET.get('last_year')

        # Actions filters for 2nd sector
        to_do = request.GET.get('todo')
        done = request.GET.get('done')
        overdue = request.GET.get('overdue')

        if this_week == 'True':
            salesleads = salesleads.filter(created__week_day=timezone.now().weekday())
        if this_month == 'True':
            salesleads = salesleads.filter(created__month=timezone.now().month)
        if this_quarter == 'True':
            pass
        if this_year == 'True':
            salesleads = salesleads.filter(created__year=timezone.now().year)
        if last_year == 'True':
            pass

        if to_do == 'True':
            activities = PlannedActivities.objects.filter(user=user).filter(
                Q(activity_done=False) | Q(activity_done=None)).filter(date__gte=timezone.now()).order_by('date')
        if done == 'True':
            activities = PlannedActivities.objects.filter(user=user).filter(activity_done=True).order_by('date')
        if overdue == 'True':
            activities = PlannedActivities.objects.filter(user=user).filter(date__lt=timezone.now()).exclude(activity_done=True).order_by('date')

        paginator = Paginator(activities, 5)
        page_obj = paginator.get_page(page_number)

        for lead in salesleads:
            if lead.status == 1:
                status_one += 1
            if lead.status == 2:
                status_two += 1
            if lead.status == 3:
                status_three += 1
            if lead.status == 4:
                status_four += 1
            if lead.status == 5:
                status_five += 1

        saleslead_history = SalesLead.history.filter(history_user=user)
        comment_history = Comment.history.filter(history_user=user)
        contactperson_history = ContactPerson.history.filter(history_user=user)
        plannedactivity_history = PlannedActivities.history.filter(history_user=user)

        together = []

        for item in comment_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display,
                             item.history_change_reason, get_user(item.history_user_id), item.id, 'comment'])
        for item in contactperson_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display, item.history_change_reason,
                             get_user(item.history_user_id), item.id, 'contactperson'])
        for item in plannedactivity_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display,
                             item.history_change_reason, get_user(item.history_user_id), item.id, 'plannedactivity'])
        for item in saleslead_history:
            try:
                saleslead = item.company_name
            except:
                saleslead = None
            together.append(
                [item.history_date, saleslead, item.get_history_type_display, item.history_change_reason,
                 get_user(item.history_user_id), item.id, 'saleslead'])

        together = sorted(together, key=lambda x: x[0], reverse=True)

        ctx = {
            'status_one': status_one,
            'status_two': status_two,
            'status_three': status_three,
            'status_four': status_four,
            'status_five': status_five,
            'page_obj': page_obj,
            'user': user,
            'together': together,
            'todo': to_do,
            'done': done,
            'overdue': overdue,
        }
        return render(request, 'salesleads/dashboard.html', ctx)


class SalesLeadAddFormView(LoginRequiredMixin, View):
    def get(self, request):
        form = SalesLeadAddForm()
        ctx = {
            'form': form
        }
        return render(request, 'salesleads/saleslead_add.html', ctx)

    def post(self, request):
        form = SalesLeadAddForm(request.POST)
        if form.is_valid():
            new_saleslead = SalesLead.objects.create(user=self.request.user, **form.cleaned_data)
            update_change_reason(new_saleslead, f'{new_saleslead.company_name}')
            return redirect('salesleads')
        return render(request, 'salesleads/saleslead_add.html', {'form': form})


class SalesLeadListView(LoginRequiredMixin, View):
    def get(self, request):
        salesleads = SalesLead.objects.filter(user=self.request.user)
        ctx = {
            'salesleads': salesleads,
        }
        return render(request, 'salesleads/saleslead_list.html', ctx)


class SalesLeadDelete(LoginRequiredMixin, DeleteView):
    model = SalesLead
    pk_url_kwarg = 'saleslead_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.company_name
        self.object.delete()
        update_change_reason(self.object, f'{name}')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('salesleads')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class SalesLeadModalDelete(LoginRequiredMixin, View):
    def get(self, request, saleslead_id):
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        ctx = {
            'saleslead':saleslead
        }
        return render(request, 'salesleads/saleslead_delete_modal.html', ctx)
    def post(self, request, saleslead_id):
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        saleslead.delete()
        update_change_reason(saleslead, f'{saleslead.company_name}')
        return redirect('salesleads')




class SalesLeadDetailView(LoginRequiredMixin, MultiFormsView):
    template_name = 'salesleads/saleslead_detail.html'
    form_classes = {'updatelead': SalesLeadAddForm,
                    'commentadd': CommentForm,
                    'contactpersonform': ContactPersonForm,
                    'updateaddress': SalesLeadAddressAddForm,
                    'plannedactivitiesaddform': PlannedActivitiesAddForm,
                    'plannedactivitiesupdateform': PlannedActivitiesUpdateForm,
                    'mygeoform': MyGeoForm,
                    'countryaddform': CountryForm}
    success_url = '/'

    def get_updatelead_initial(self):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        ctx = model_to_dict(saleslead)
        return ctx

    def get_updateaddress_initial(self):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        ctx = model_to_dict(saleslead)
        return ctx

    def get_context_data(self, **kwargs):
        context = super(SalesLeadDetailView, self).get_context_data(**kwargs)
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        comments = saleslead.comment.all()
        contactpeople = saleslead.contacts.all().order_by('default', 'first_name')
        activities = saleslead.plannedactivities.all()
        context.update(
            {
                'saleslead': saleslead,
                'comments': comments,
                'activities': activities,
                'contactpeople': contactpeople,
            }
        )
        return context

    def updatelead_form_valid(self, form):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead_update = SalesLead.objects.get(pk=saleslead_id)
        saleslead_update.company_name = form.cleaned_data['company_name']
        saleslead_update.type = form.cleaned_data['type']
        saleslead_update.status = form.cleaned_data['status']
        saleslead_update.company_website = form.cleaned_data['company_website']
        saleslead_update.source = form.cleaned_data['source']
        saleslead_update.brands = form.cleaned_data['brands']
        saleslead_update.potential = form.cleaned_data['potential']
        saleslead_update.score = form.cleaned_data['score']
        saleslead_update.save()
        update_change_reason(saleslead_update, f'{saleslead_update.company_name}')
        return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': saleslead_id}))

    def commentadd_form_valid(self, form):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        new_comment = Comment.objects.create(saleslead=saleslead, comment=form.cleaned_data['comment'])
        print(new_comment)
        update_change_reason(new_comment, 'dane komentarza')
        return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': saleslead_id}))

    def updateaddress_form_valid(self, form):
        saleslead_id = self.kwargs['saleslead_id']
        address_update = SalesLead.objects.get(pk=saleslead_id)
        address_update.street = form.cleaned_data['street']
        address_update.city = form.cleaned_data['city']
        address_update.postcode = form.cleaned_data['postcode']
        address_update.country = form.cleaned_data['country']
        address_update.longtitude = form.cleaned_data['longtitude']
        address_update.latitude = form.cleaned_data['latitude']
        address_update.save()
        update_change_reason(address_update, f'dane adresowe {address_update.company_name}')
        return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': saleslead_id}))

    def plannedactivitiesaddform_form_valid(self, form):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        new_activity = PlannedActivities.objects.create(
            user=self.request.user,
            saleslead=saleslead,
            date=form.cleaned_data['date'],
            activity_type=form.cleaned_data['activity_type'],
            activity_comment=form.cleaned_data['activity_comment']
        )
        update_change_reason(new_activity, 'planowane działanie')
        return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': saleslead_id}))

    def contactpersonform_form_valid(self, form):
        saleslead_id = self.kwargs['saleslead_id']
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        new_contactperson = ContactPerson.objects.create(saleslead=saleslead, **form.cleaned_data)
        update_change_reason(new_contactperson, 'dane osoby kontaktowej')
        return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': saleslead_id}))


class SearchResults(LoginRequiredMixin, ListView):
    model = SalesLead
    template_name = 'salesleads/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = SalesLead.objects.filter(Q(company_name__icontains=query))
        return object_list


class SalesLeadMap(LoginRequiredMixin, ListView):
    # queryset = SalesLead.objects.filter(latitude__isnull=False)
    template_name = 'salesleads/map.html'

    def get_queryset(self):
        salesleads = SalesLead.objects.filter(latitude__isnull=False)
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')
        statuses = self.request.GET.getlist('status')

        if is_valid_query(date_min):
            salesleads = salesleads.filter(created__gte=date_min)
        if is_valid_query(date_max):
            salesleads = salesleads.filter(created__lt=date_max)
        if statuses:
            salesleads = salesleads.filter(status__in=statuses)
        return salesleads

    def get_context_data(self, *args, **kwargs):
        context = super(SalesLeadMap, self).get_context_data(*args, **kwargs)
        context['date_min'] = self.request.GET.get('date_min')
        context['date_max'] = self.request.GET.get('date_max')
        context['statuses'] = self.request.GET.getlist('status')
        context['types'] = STATUS
        context['logged_user'] = self.request.user.id
        return context


class ContactPersonAll(LoginRequiredMixin, ListView):
    model = ContactPerson
    template_name = 'salesleads/saleslead_detail.html'


class ContactPersonDelete(LoginRequiredMixin, DeleteView):
    model = ContactPerson
    pk_url_kwarg = 'contactperson_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        update_change_reason(self.object, 'dane osoby kontaktowej')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        update_change_reason(self.object, 'dane komentarza')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class PlannedActitivitiesDelete(LoginRequiredMixin, DeleteView):
    model = PlannedActivities
    pk_url_kwarg = 'plannedactivity_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        update_change_reason(self.object, 'planowane działanie')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CommentUpdate(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        form = CommentForm(initial={'comment': comment})
        ctx = {
            'form': form,
            'comment': comment
        }
        return render(request, 'salesleads/comment_update.html', ctx)

    def post(self, request, comment_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_update = Comment.objects.get(pk=comment_id)
            comment_update.comment = form.cleaned_data['comment']
            comment_update.save()
            update_change_reason(comment_update, 'dane komentarze')
            comment = Comment.objects.get(pk=comment_id)
            return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': comment.saleslead.id}))


class ContactPersonUpdate(View):
    def get(self, request, contactperson_id):
        contact_person = get_object_or_404(ContactPerson, pk=contactperson_id)
        form = ContactPersonForm(initial={
            'first_name': contact_person.first_name,
            'last_name': contact_person.last_name,
            'position': contact_person.position,
            'email': contact_person.email,
            'telephone': contact_person.telephone,
            'whatsapp': contact_person.whatsapp,
            'linkedin_added': contact_person.linkedin_added,
            'default':contact_person.default
        })
        ctx = {
            'contactperson': contact_person,
            'form': form
        }
        return render(request, 'salesleads/contactperson_update.html', ctx)

    def post(self, request, contactperson_id):
        form = ContactPersonForm(request.POST)
        if form.is_valid():
            contact_update = ContactPerson.objects.get(pk=contactperson_id)
            contact_update.first_name = form.cleaned_data['first_name']
            contact_update.last_name = form.cleaned_data['last_name']
            contact_update.position = form.cleaned_data['position']
            contact_update.email = form.cleaned_data['email']
            contact_update.telephone = form.cleaned_data['telephone']
            contact_update.whatsapp = form.cleaned_data['whatsapp']
            contact_update.linkedin_added = form.cleaned_data['linkedin_added']
            contact_update.default = form.cleaned_data['default']
            contact_update.save()
            update_change_reason(contact_update, 'dane osoby kontaktowej')
            contact = ContactPerson.objects.get(pk=contactperson_id)
            return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': contact.saleslead.id}))


class PlannedActivitiesUpdate(View):
    def get(self, request, plannedactivities_id):
        planned_activity = get_object_or_404(PlannedActivities, pk=plannedactivities_id)
        form = PlannedActivitiesUpdateForm(initial={
            'date': planned_activity.date,
            'activity_type': planned_activity.activity_type,
            'activity_comment': planned_activity.activity_comment,
            'activity_done': planned_activity.activity_done
        })
        ctx = {
            'form': form,
            'activity': planned_activity
        }
        return render(request, 'salesleads/plannedactivities_update.html', ctx)

    def post(self, request, plannedactivities_id):
        form = PlannedActivitiesUpdateForm(request.POST)
        if form.is_valid():
            planned_activity_update = PlannedActivities.objects.get(pk=plannedactivities_id)
            planned_activity_update.activity_type = form.cleaned_data['activity_type']
            planned_activity_update.activity_comment = form.cleaned_data['activity_comment']
            planned_activity_update.activity_done = form.cleaned_data['activity_done']
            planned_activity_update.save()
            update_change_reason(planned_activity_update, 'planowane działanie')
            planned_activity = PlannedActivities.objects.get(pk=plannedactivities_id)
            return redirect(reverse('saleslead-detail', kwargs={'saleslead_id': planned_activity.saleslead.id}))


def country_create(request):
    data = dict()

    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            countries = Country.objects.all()
            data['html_countries_list'] = render_to_string('salesleads/partial_book_list.html', {
                'countries': countries
            })
        else:
            data['form_is_valid'] = False
    else:
        form = CountryForm()

    context = {'form': form}
    data['html_form'] = render_to_string('salesleads/country_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)


class ReportView(View):
    def get(self, request):
        saleslead_history = SalesLead.history.all()
        comment_history = Comment.history.all()
        contactperson_history = ContactPerson.history.all()
        plannedactivity_history = PlannedActivities.history.all()
        users = ExportUser.objects.all()

        page_number = request.GET.get('page')

        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        user_get = request.GET.get('user')

        if is_valid_query(user_get) and user_get != 'Wybierz...':
            saleslead_history = saleslead_history.filter(history_user_id=get_user_id(user_get))
            comment_history = comment_history.filter(history_user_id=get_user_id(user_get))
            contactperson_history = comment_history.filter(history_user_id=get_user_id(user_get))
            plannedactivity_history = plannedactivity_history.filter(history_user_id=get_user_id(user_get))

        if is_valid_query(date_min):
            saleslead_history = saleslead_history.filter(history_date__gte=date_min)
            comment_history = comment_history.filter(history_date__gte=date_min)
            contactperson_history = comment_history.filter(history_date__gte=date_min)
            plannedactivity_history = plannedactivity_history.filter(history_date__gte=date_min)

        if is_valid_query(date_max):
            saleslead_history = saleslead_history.filter(history_date__lt=date_max)
            comment_history = comment_history.filter(history_date__lt=date_max)
            contactperson_history = comment_history.filter(history_date__lt=date_max)
            plannedactivity_history = plannedactivity_history.filter(history_date__lt=date_max)

        together = []

        for item in comment_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display,
                             item.history_change_reason, get_user(item.history_user_id), item.id, 'comment'])
        for item in contactperson_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display, item.history_change_reason,
                             get_user(item.history_user_id), item.id, 'contactperson'])
        for item in plannedactivity_history:
            try:
                saleslead = get_saleslead(item.saleslead_id)
            except:
                saleslead = None
            together.append([item.history_date, saleslead, item.get_history_type_display,
                             item.history_change_reason, get_user(item.history_user_id), item.id, 'plannedactivity'])

        for item in saleslead_history:
            try:
                saleslead = item.company_name
            except:
                saleslead = None
            together.append(
                [item.history_date, saleslead, item.get_history_type_display, item.history_change_reason,
                 get_user(item.history_user_id), item.id, 'saleslead'])

        together = sorted(together, key=lambda x: x[0], reverse=True)

        paginator = Paginator(together, 15)
        page_obj = paginator.get_page(page_number)

        ctx = {
            'page_obj': page_obj,
            'users': users,
            'date_min': date_min,
            'date_max': date_max,
            'user_get': user_get
        }
        return render(request, 'salesleads/report.html', ctx)


class ChangeUserView(LoginRequiredMixin, View):
    def get(self, request, saleslead_id):
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        users = ExportUser.objects.exclude(username=self.request.user)
        form = ChangeUserForm()
        ctx = {
            'form': form,
            'saleslead': saleslead,
            'users': users
        }
        return render(request, 'salesleads/user_change.html', ctx)

    def post(self, request, saleslead_id):
        user = self.request.POST.get('user')
        saleslead = SalesLead.objects.get(pk=saleslead_id)
        saleslead.user_id = ExportUser.objects.get(username=user).id
        saleslead.save()
        update_change_reason(saleslead, f'{saleslead.company_name} przekazany')
        return redirect('salesleads')
