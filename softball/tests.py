import unittest
from datetime import date
from django.test import TestCase

from softball.models import *
from softball.context_processors import game_record

class ContextProcessorTest(TestCase):
    def test_game_record(self):
        self.assertEqual(game_record(request=None), { "wins": 0, "losses": 0, "ties": 0 })
        
        # Test a single win
        Game.objects.create(game_date=date(2009, 01, 01), score=1, opponent_score=0, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 1, "losses": 0, "ties": 0 })
        Game.objects.all().delete()
        
        # Test a single loss
        Game.objects.create(game_date=date(2009, 01, 01), score=1, opponent_score=1, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 0, "losses": 0, "ties": 1 })
        Game.objects.all().delete()
        
        # Test a single tie
        Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=1, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 0, "losses": 1, "ties": 0 })
        Game.objects.all().delete()
        
        # Test a tie with no score
        Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=0, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 0, "losses": 0, "ties": 1 })
        Game.objects.all().delete()
        
        # Test a accumulated wins, losses, and ties
        Game.objects.create(game_date=date(2009, 01, 01), score=1, opponent_score=0, opponent="Test Opponent 1")
        Game.objects.create(game_date=date(2009, 02, 01), score=1, opponent_score=0, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 2, "losses": 0, "ties": 0 })
        Game.objects.create(game_date=date(2009, 03, 01), score=0, opponent_score=1, opponent="Test Opponent 1")
        Game.objects.create(game_date=date(2009, 04, 01), score=0, opponent_score=1, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 2, "losses": 2, "ties": 0 })
        Game.objects.create(game_date=date(2009, 05, 01), score=1, opponent_score=1, opponent="Test Opponent 1")
        Game.objects.create(game_date=date(2009, 06, 01), score=0, opponent_score=0, opponent="Test Opponent 1")
        self.assertEqual(game_record(request=None), { "wins": 2, "losses": 2, "ties": 2 })
        Game.objects.all().delete()
