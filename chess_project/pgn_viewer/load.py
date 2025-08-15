import os
import chess.pgn
import json
from django.http import JsonResponse
from django.conf import settings

def get_pgn_path(filename):
    """Helper function to get consistent file paths"""
    safe_filename = os.path.basename(filename)  # Prevent directory traversal
    pgn_dir = os.path.join(settings.MEDIA_ROOT, 'pgn_files')
    os.makedirs(pgn_dir, exist_ok=True)  # Ensure directory exists
    return os.path.join(pgn_dir, safe_filename)

def get_games_list(request):
    filename = request.GET.get('filename')
    if not filename:
        return JsonResponse({'error': 'Filename parameter missing'}, status=400)
    
    pgn_path = get_pgn_path(filename)
    
    print(f"Looking for PGN file at: {pgn_path}")  # Debugging
    
    if not os.path.exists(pgn_path):
        return JsonResponse({
            'error': 'File not found',
            'debug_info': {
                'requested_file': filename,
                'full_path': pgn_path,
                'media_root': settings.MEDIA_ROOT,
                'files_in_dir': os.listdir(os.path.dirname(pgn_path)) if os.path.exists(os.path.dirname(pgn_path)) else 'Directory not found'
            }
        }, status=404)
    
    games = []
    with open(pgn_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            games.append({
                'headers': dict(game.headers)
            })
    
    return JsonResponse({'games': games})

def load_specific_game(request):
    filename = request.GET.get('filename')
    index = request.GET.get('index')
    
    if not filename or not index:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        index = int(index)
    except ValueError:
        return JsonResponse({'error': 'Invalid index'}, status=400)
    
    pgn_path = get_pgn_path(filename)
    
    if not os.path.exists(pgn_path):
        return JsonResponse({
            'error': 'File not found',
            'debug_info': {
                'requested_file': filename,
                'full_path': pgn_path
            }
        }, status=404)
    
    game_data = None
    current_index = 0
    with open(pgn_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            if current_index == index:
                exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                game_data = {
                    'headers': dict(game.headers),
                    'pgn': game.accept(exporter),
                    'index': index
                }
                break
            current_index += 1
    
    if game_data is None:
        return JsonResponse({'error': 'Game index out of range'}, status=404)
    
    return JsonResponse({'game': game_data})

def get_related_games(request):
    filename = request.GET.get('filename')
    moves_json = request.GET.get('moves')
    current_game = request.GET.get('current_game')
    
    if not filename or not moves_json or not current_game:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        moves = json.loads(moves_json)
        current_game = int(current_game)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({'error': f'Invalid parameters: {str(e)}'}, status=400)
    
    pgn_path = get_pgn_path(filename)
    
    if not os.path.exists(pgn_path):
        return JsonResponse({
            'error': 'File not found',
            'debug_info': {
                'requested_file': filename,
                'full_path': pgn_path
            }
        }, status=404)
    
    related_games = []
    with open(pgn_path) as pgn_file:
        game_index = 0
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            if game_index != current_game:
                node = game
                match_count = 0
                
                for move in moves:
                    if not node.variations:
                        break
                    next_node = node.variation(0)
                    if next_node.move.uci() == chess.Move.from_uci(move).uci():
                        match_count += 1
                        node = next_node
                    else:
                        break
                
                if match_count == len(moves):
                    related_games.append({
                        'game_index': game_index,
                        'move_index': match_count,
                        'headers': dict(game.headers)
                    })
            
            game_index += 1
    
    return JsonResponse({
        'related_games': related_games,
        'debug_info': {
            'search_moves': moves,
            'current_game_skipped': current_game,
            'total_games_searched': game_index
        }
    })