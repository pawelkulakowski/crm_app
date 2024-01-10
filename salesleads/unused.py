# class SalesLeadDetailView(View):
#     def get(self, request, saleslead_id):
#         saleslead = SalesLead.objects.get(pk=saleslead_id)
#         comments = saleslead.comment.all()
#         form = SalesLeadAddForm(initial=model_to_dict(saleslead))
#         comment_form = CommentAddForm(initial={'saleslead': saleslead})
#         ctx = {
#             'saleslead': saleslead,
#             'comments': comments,
#             'form': form,
#             'comment_form': comment_form
#         }
#         return render(request, 'salesleads/saleslead_detail.html', ctx)
#
#
# class CommentAddView(View):
#     def get(self, request, saleslead_id):
#         saleslead = SalesLead.objects.get(pk=saleslead_id)
#         form = CommentAddForm()
#         return render(request, 'salesleads/comment_add.html', {'form': form, 'saleslead': saleslead})
#
#     def post(self, request, saleslead_id):
#         form = CommentAddForm(request.POST)
#         if form.is_valid():
#             saleslead = SalesLead.objects.get(pk=saleslead_id)
#             comment = form.cleaned_data['comment']
#             new_comment = Comment.objects.create(saleslead=saleslead, comment=comment)
#             return redirect('/')
#
#
# class TwoFormsView(View):
#     def get(self, request, saleslead_id):
#         saleslead = SalesLead.objects.get(pk=saleslead_id)
#         sale = model_to_dict(saleslead)
#         formOne = SalesLeadAddForm(initial=sale)
#         formTwo = CommentAddForm()
#         comments = saleslead.comment.all()
#         ctx = {
#             'formOne': formOne,
#             'formTwo': formTwo,
#             'saleslead': saleslead,
#             'comments': comments,
#         }
#         return render(request, 'salesleads/saleslead_detail3.html', ctx)

# class SalesLeadUpdateView(UpdateView):
#     template_name = 'salesleads/saleslead_d.html'
#     model = SalesLead
#     fields = ['company_name', 'type', 'status']
#     success_url = '/'
#
#     def get_updatelead_initial(self):
#         saleslead_id = self.kwargs['saleslead_id']
#         saleslead = SalesLead.objects.get(pk=saleslead_id)
#         ctx = model_to_dict(saleslead)
#         return ctx
