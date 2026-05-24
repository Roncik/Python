from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Word, Definition, Vote, Comment
from .forms import WordForm, DefinitionForm, CommentForm, WordEditForm

def home(request):
    return render(request, 'records/home.html')

def word_list(request):
    words = Word.objects.all().order_by('-created_at')
    return render(request, 'records/word_list.html', {'words': words})

def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    comments = word.comments.all().order_by('-created_at') # Fetch all comments for this word
    
    if request.method == 'POST':
        # Safety check: ensure user is logged in before processing comment
        if not request.user.is_authenticated:
            return redirect('login')
            
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.word = word
            comment.author = request.user
            comment.save()
            return redirect('word_detail', pk=word.pk) # Refresh the page
    else:
        comment_form = CommentForm()

    return render(request, 'records/word_detail.html', {
        'word': word,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def add_word(request):
    if request.method == 'POST':
        word_form = WordForm(request.POST)
        def_form = DefinitionForm(request.POST)
        
        if word_form.is_valid() and def_form.is_valid():
            word = word_form.save()
            definition = def_form.save(commit=False)
            definition.word = word
            definition.author = request.user
            definition.save()
            return redirect('word_detail', pk=word.pk)
    else:
        word_form = WordForm()
        def_form = DefinitionForm()
        
    return render(request, 'records/add_word.html', {
        'word_form': word_form, 
        'def_form': def_form
    })

@login_required
def edit_word(request, pk):
    word = get_object_or_404(Word, pk=pk)
    # Grab the first definition associated with this word
    definition = word.definitions.first()
    
    if request.method == 'POST':
        # Pass the instances so Django knows we are updating, not creating
        word_form = WordEditForm(request.POST, instance=word)
        def_form = DefinitionForm(request.POST, instance=definition)
        
        if word_form.is_valid() and def_form.is_valid():
            word_form.save()
            
            # Save the definition safely
            updated_def = def_form.save(commit=False)
            if not definition:
                updated_def.word = word
                updated_def.author = request.user
            updated_def.save()
            
            return redirect('word_detail', pk=word.pk)
    else:
        word_form = WordEditForm(instance=word)
        def_form = DefinitionForm(instance=definition)
        
    # Pass both forms to the template
    return render(request, 'records/edit_word.html', {
        'word_form': word_form, 
        'def_form': def_form, 
        'word': word
    })

@login_required
def delete_word(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word_list')
    return render(request, 'records/delete_word.html', {'word': word})

@login_required
def vote_definition(request, pk):
    if request.method == 'POST':
        definition = get_object_or_404(Definition, pk=pk)
        action = request.POST.get('action') # This will be 'up' or 'down'
        
        if action in ['up', 'down']:
            is_upvote = (action == 'up')
                        
            existing_vote = Vote.objects.filter(definition=definition, user=request.user).first()
            
            if existing_vote:
                if existing_vote.is_upvote == is_upvote:
                    # Clicking the same button again removes the vote
                    existing_vote.delete()
                else:
                    # Clicking the opposite button switches the vote
                    existing_vote.is_upvote = is_upvote
                    existing_vote.save()
            else:            
                Vote.objects.create(definition=definition, user=request.user, is_upvote=is_upvote)
                        
        return redirect('word_detail', pk=definition.word.pk)
    
@login_required
def words_by_me(request):
    words = Word.objects.filter(definitions__author=request.user).distinct().order_by('-created_at')
    return render(request, 'records/my_word_list.html', {'words': words})

@login_required
def my_comments(request):
    comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'records/my_comment_list.html', {'comments': comments})