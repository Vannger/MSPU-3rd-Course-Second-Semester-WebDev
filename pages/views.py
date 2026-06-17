from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SpellForm, RegisterForm
from .models import Spell


# ── Home ──────────────────────────────────────────────────────────────────────

def home(request):
    spells = Spell.objects.all().order_by('spell_lvl', 'name')
    return render(request, 'pages/index.html', {
        'title': 'Arcane Compendium',
        'welcome_text': 'A tome of spells for adventurers of every discipline.',
        'spells': spells,
    })


def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    return render(request, 'pages/detail.html', {
        'title': spell.name,
        'spell': spell,
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


# ── Spells ────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def add_spell(request):
    if request.method == 'POST':
        form = SpellForm(request.POST, request.FILES)
        if form.is_valid():
            spell = form.save(commit=False)
            spell.author = request.user
            spell.save()
            messages.success(request, f'"{spell.name}" has been added to the compendium.')
            return redirect('home')
    else:
        form = SpellForm()
    return render(request, 'pages/add_spell.html', {'title': 'Add a Spell', 'form': form})


@login_required(login_url='login')
def edit_spell(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)

    # Only the author or an admin may edit
    if not request.user.is_staff and spell.author != request.user:
        messages.error(request, 'You can only edit spells you have added yourself.')
        return redirect('home')

    if request.method == 'POST':
        form = SpellForm(request.POST, request.FILES, instance=spell)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{spell.name}" has been updated.')
            return redirect('home')
    else:
        form = SpellForm(instance=spell)

    return render(request, 'pages/edit_spell.html', {
        'title': f'Edit: {spell.name}',
        'form': form,
        'spell': spell,
    })
