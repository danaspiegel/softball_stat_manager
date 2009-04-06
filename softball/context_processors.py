from softball.models import *

def game_record(request):
    games = Game.objects.all()
    wins = sum(map(lambda game: int(game.score > game.opponent_score), games))
    losses = sum(map(lambda game: int(game.score < game.opponent_score), games))
    ties = sum(map(lambda game: int(game.score == game.opponent_score), games))
    return {"wins": wins, "losses": losses, "ties": ties, }