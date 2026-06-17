from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SpellForm, RegisterForm, FeedbackForm, CommentForm
from .models import Spell, Tag


# ── Home (ListView) ─────────────────────────────────────────────────────────

class Home(ListView):
    model = Spell
    template_name = 'pages/index.html'
    context_object_name = 'spells'
    ordering = ['-add_date']  # newest first, per task spec

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Arcane Compendium'
        context['welcome_text'] = 'A tome of spells for adventurers of every discipline.'
        return context


# ── Spell Detail (DetailView) ────────────────────────────────────────────────

class SpellDetail(DetailView):
    model = Spell
    template_name = 'pages/detail.html'
    context_object_name = 'spell'   # self.object is now available in template as {{ spell }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['comment_form'] = CommentForm()
        return context


# ── Tag filter (kept as a function view — no model form/CBV needed here) ────

def spells_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    spells = tag.spells.all().order_by('-add_date')
    return render(request, 'pages/index.html', {
        'title': f'Tagged: {tag.name}',
        'welcome_text': f'Spells marked with the "{tag.name}" tag.',
        'spells': spells,
        'active_tag': tag,
    })


# ── About ─────────────────────────────────────────────────────────────────────

def about(request):
    return render(request, 'pages/about.html', {
        'title': 'About',
        'text': 'Your guide to the arcane arts.',
    })


# ── Auth ──────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'title': 'Sign Up', 'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'title': 'Login', 'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ── Spells: Create / Update / Delete (CBVs) ──────────────────────────────────

class AddSpell(LoginRequiredMixin, CreateView):
    """LoginRequiredMixin must come FIRST (left) in the inheritance list,
    otherwise the login check never runs."""
    model = Spell
    form_class = SpellForm
    template_name = 'pages/add_spell.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a Spell'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.name}" has been added to the compendium.')
        return response


class EditSpell(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Spell
    form_class = SpellForm
    template_name = 'pages/edit_spell.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def test_func(self):
        spell = self.get_object()
        # Author OR staff/admin may edit — matches the original function-based view
        return self.request.user.is_staff or spell.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit spells you have added yourself.')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit: {self.object.name}'
        context['spell'] = self.object
        return context

    def form_valid(self, form):
        # Author is NOT reassigned on edit — only set once, at creation.
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.name}" has been updated.')
        return response


class DeleteSpell(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Spell
    template_name = 'pages/spell_confirm_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def test_func(self):
        spell = self.get_object()
        return self.request.user.is_staff or spell.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete spells you have added yourself.')
        return redirect('home')

    def form_valid(self, form):
        messages.success(self.request, f'"{self.object.name}" has been removed from the compendium.')
        return super().form_valid(form)


# ── Feedback ──────────────────────────────────────────────────────────────────

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print("New Message", form.cleaned_data)
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'pages/feedback.html', {'form': form})


# ── Comments ──────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def add_comment(request, pk):
    spell = get_object_or_404(Spell, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.spell = spell
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш комментарий успешно добавлен!')
        else:
            messages.error(request, 'Ошибка при добавлении комментария.')

    return redirect('spell_detail', pk=pk)
