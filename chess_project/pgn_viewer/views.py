import os
import chess.pgn
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .forms import PgnUploadForm
from django.views.decorators.http import require_GET

def home(request):
    pgn_dir = os.path.join(settings.MEDIA_ROOT, "pgn_files")
    os.makedirs(pgn_dir, exist_ok=True)
    pgn_files = [f for f in os.listdir(pgn_dir) if f.endswith(".pgn")]

    if request.method == "POST" and "pgn_file" in request.FILES:
        form = PgnUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['pgn_file']
            save_path = os.path.join(pgn_dir, uploaded_file.name)
            with open(save_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)
            return JsonResponse({"status": "success", "filename": uploaded_file.name})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form"}, status=400)

    if request.method == "POST" and request.POST.get("selected_pgn"):
        file_name = request.POST.get("selected_pgn")
        file_path = os.path.join(pgn_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return JsonResponse({"status": "success", "pgn": f.read()})

    form = PgnUploadForm()
    return render(request, "home.html", {
        "form": form,
        "pgn_files": pgn_files,
    })


@require_GET
def load_pgn(request):
    filename = request.GET.get('filename')
    if not filename:
        return JsonResponse({'error': 'Filename required'}, status=400)
    
    try:
        pgn_dir = os.path.join(settings.MEDIA_ROOT, "pgn_files")
        file_path = os.path.join(pgn_dir, filename)
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'File not found'}, status=404)
        
        games = []
        with open(file_path, "r", encoding="utf-8") as f:
            while True:
                offset = f.tell()
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                
                # Get headers and moves
                headers = dict(game.headers)
                game_moves = []
                node = game
                while node.variations:
                    next_node = node.variation(0)
                    game_moves.append(node.board().san(next_node.move))
                    node = next_node
                
                games.append({
                    'headers': headers,
                    'moves': game_moves,
                    'pgn': str(game),
                    'offset': offset
                })
        
        if not games:
            return JsonResponse({'error': 'No games found in PGN file'}, status=404)
            
        return JsonResponse({
            'games': games,
            'count': len(games)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


def upload_pgn(request):
    if request.method == 'POST':
        form = PgnUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pgn_file = request.FILES['pgn_file']
            
            # Ensure the pgn_files directory exists
            pgn_dir = os.path.join(settings.MEDIA_ROOT, 'pgn_files')
            os.makedirs(pgn_dir, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(pgn_dir, pgn_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in pgn_file.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'success': True,
                'filename': os.path.join(pgn_file.name)
            })
    return JsonResponse({'success': False, 'error': 'Invalid form'})