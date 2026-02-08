from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Note, Chat
from .rag_utils import get_or_create_chunk, get_embedding, prepare_context, generate_response


from .models import Note
from .utils import extract_text_from_pdf, generate_notes


@login_required
def upload_note_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        pdf_file = request.FILES.get("file")
        p1 = request.POST.get('style')
        p2 = request.POST.get('format')

        if title and pdf_file:
            extracted_text = extract_text_from_pdf(pdf_file)

            note = Note.objects.create(user=request.user, title=title, content=extracted_text)
            note.save()
            user = request.user
            key = user.profile.api_key

            generated_notes = generate_notes(extracted_text, p1, p2, key)

            note.generated_notes = generated_notes
            note.save()



            return redirect('note_view', note_id=note.id)

    return render(request, "notes/upload_note.html")

@login_required
def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, "notes/notes_display.html", {"generated_note": note.generated_notes, "note": note})

@login_required
def history_view(request):
    user = request.user
    notes = Note.objects.filter(user=user).order_by('-created_at')
    return render(request, "notes/history.html", {"notes": notes})

from django.http import JsonResponse

@login_required
def ask_doubt_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    key = request.user.profile.api_key

    chunks = get_or_create_chunk(note, key)
    embedding = get_embedding(note)

    # ✅ AJAX POST request
    if request.method == "POST":
        question = request.POST.get("question")

        Chat.objects.create(note=note, role="user", text=question)

        context = prepare_context(note, chunks, embedding, question, key)
        response = generate_response(context, question, key)

        Chat.objects.create(note=note, role="assistant", text=response)

        # 🔥 IMPORTANT: return JSON if AJAX
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "response": response
            })

    chats = Chat.objects.filter(note=note).order_by("created_at")

    return render(
        request,
        "notes/ask_doubt.html",
        {
            "note": note,
            "chats": chats
        }
    )

@login_required
def delete_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    note.delete()
    return redirect('history')








