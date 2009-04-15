from decimal import Decimal

from django.db import models

def average(at_bats, hits):
    """
    Avg = H / AB
    
    >>> average(0, 0)
    Decimal("0")
    >>> average(4, 2)
    Decimal("0.5")
    >>> average(1, 1)
    Decimal("1")
    >>> average(2, 1)
    Decimal("0.5")
    >>> average(1, 0)
    Decimal("0")
    """
    if at_bats == 0:
        return Decimal("0")
    if at_bats < hits:
        return Decimal("0")
    return Decimal(hits) / Decimal(at_bats)

def on_base_percentage(at_bats, walks, hits):
    """
    OBP = (H + BB) / (AB + BB)
    
    >>> on_base_percentage(0, 0, 0)
    Decimal("0")
    >>> on_base_percentage(1, 0, 0)
    Decimal("0")
    >>> on_base_percentage(1, 0, 1)
    Decimal("1")
    >>> on_base_percentage(2, 1, 1)
    Decimal("0.6666666666666666666666666667")
    >>> on_base_percentage(4, 1, 1)
    Decimal("0.4")
    >>> on_base_percentage(4, 0, 1)
    Decimal("0.25")
    >>> on_base_percentage(4, 1, 0)
    Decimal("0.2")
    """
    if at_bats == 0:
        return Decimal("0")
    return Decimal(hits + walks) / Decimal(at_bats + walks)

def slugging_percentage(at_bats, hits, doubles, triples, home_runs):
    """
    SLG = (H + (2B * 2) + (3B * 2) + (HR * 3)) / AB

    >>> slugging_percentage(0, 0, 0, 0, 0)
    Decimal("0")
    >>> slugging_percentage(3, 0, 0, 0, 0)
    Decimal("0")
    >>> slugging_percentage(3, 1, 1, 1, 0)
    Decimal("2")
    >>> slugging_percentage(4, 1, 1, 1, 1)
    Decimal("2.5")
    >>> slugging_percentage(1, 1, 0, 0, 0)
    Decimal("1")
    >>> slugging_percentage(1, 0, 1, 0, 0)
    Decimal("2")
    >>> slugging_percentage(1, 0, 0, 1, 0)
    Decimal("3")
    >>> slugging_percentage(1, 0, 0, 0, 1)
    Decimal("4")
    >>> slugging_percentage(8, 2, 2, 2, 2)
    Decimal("2.5")
    """
    if at_bats == 0:
        return Decimal("0")
    return Decimal(hits + (2 * doubles) + (3 * triples) + (4 * home_runs)) / Decimal(at_bats)
    
class Player(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        unique_together = ("first_name", "last_name")
        ordering = ["last_name", "first_name", ]
    
    def __unicode__(self):
        """
        >>> p = Player(first_name="First", last_name="Last")
        >>> str(p)
        "First Last"
        >>> p = Player(first_name="First", last_name="Last", number="123")
        >>> str(p)
        "First Last (#123)"
        """
        if self.number:
            return "%s %s (#%s)" % (self.first_name, self.last_name, self.number, )
        else:
            return "%s %s" % (self.first_name, self.last_name, )
    
    def _hits_get(self):
        """
        Returns the total hits, doubles, triples, and home_runs
        
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=2, opponent_score=3, opponent="Test Opponent 5")
        >>> g6, created = Game.objects.get_or_create(game_date=date(2009, 06, 01), score=2, opponent_score=3, opponent="Test Opponent 6")
        >>> g7, created = Game.objects.get_or_create(game_date=date(2009, 07, 01), score=2, opponent_score=3, opponent="Test Opponent 7")
        >>> g8, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=2, opponent_score=3, opponent="Test Opponent 8")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.hits
        0
        >>> Statistic(player=p, game=g1, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        2
        
        Test the accumulation of stats
        >>> Statistic(player=p, game=g3, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        2
        >>> Statistic(player=p, game=g4, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        3
        >>> Statistic(player=p, game=g5, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.hits
        4
        >>> Statistic(player=p, game=g6, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.hits
        5
        >>> Statistic(player=p, game=g7, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.hits
        6
        >>> Statistic(player=p, game=g8, singles=1, doubles=2, triples=3, home_runs=4).save()
        >>> p.hits
        16
        
        Clear out the Statistics, and test a single statistic
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g1, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        0
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        1
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g3, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.hits
        1
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g4, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.hits
        1
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g5, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.hits
        1
        >>> p.stats.all().delete()
        >>> Statistic(player=p, game=g6, singles=1, doubles=2, triples=3, home_runs=4).save()
        >>> p.hits
        10
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.hits, self.stats.all(), 0)
    hits = property(_hits_get)
    
    def _walks_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.walks
        0
        >>> Statistic(player=p, game=g1, hits=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, hits=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        0
        >>> Statistic(player=p, game=g3, walks=1, hits=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        1
        >>> Statistic(player=p, game=g4, walks=2, hits=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        3
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.walks, self.stats.all(), 0)
    walks = property(_walks_get)
    
    def _runs_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.runs
        0
        >>> Statistic(player=p, game=g1, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        2
        >>> Statistic(player=p, game=g3, walks=1, runs=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        2
        >>> Statistic(player=p, game=g4, walks=2, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        3
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.runs, self.stats.all(), 0)
    runs = property(_runs_get)
    
    def _singles_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.singles
        0
        >>> Statistic(player=p, game=g1, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        2
        >>> Statistic(player=p, game=g3, walks=1, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        2
        >>> Statistic(player=p, game=g4, walks=2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        3
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.singles, self.stats.all(), 0)
    singles = property(_singles_get)

    def _at_bats_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.at_bats
        0
        >>> Statistic(player=p, game=g1, at_bats=1).save()
        >>> Statistic(player=p, game=g2, at_bats=1).save()
        >>> p.at_bats
        2
        >>> Statistic(player=p, game=g3, at_bats=3).save()
        >>> p.at_bats
        5
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.at_bats, self.stats.all(), 0)
    at_bats = property(_at_bats_get)
    
    def _doubles_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.doubles
        0
        >>> Statistic(player=p, game=g1, doubles=1).save()
        >>> Statistic(player=p, game=g2, doubles=1).save()
        >>> p.doubles
        2
        >>> Statistic(player=p, game=g3, doubles=3).save()
        >>> p.doubles
        5
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.doubles, self.stats.all(), 0)
    doubles = property(_doubles_get)

    def _triples_get(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.triples
        0
        >>> Statistic(player=p, game=g1, triples=1).save()
        >>> Statistic(player=p, game=g2, triples=1).save()
        >>> p.triples
        2
        >>> Statistic(player=p, game=g3, triples=3).save()
        >>> p.triples
        5
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.triples, self.stats.all(), 0)
    triples = property(_triples_get)

    def _home_runs_get(self):
        """
        Returns the total number of home runs for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.home_runs
        0
        >>> Statistic(player=p, game=g1, home_runs=1).save()
        >>> Statistic(player=p, game=g2, home_runs=1).save()
        >>> p.home_runs
        2
        >>> Statistic(player=p, game=g3, home_runs=3).save()
        >>> p.home_runs
        5
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.home_runs, self.stats.all(), 0)
    home_runs = property(_home_runs_get)
    
    def _rbis_get(self):
        """
        Returns the total number of rbis for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.rbis
        0
        >>> Statistic(player=p, game=g1, rbis=1).save()
        >>> Statistic(player=p, game=g2, rbis=1).save()
        >>> p.rbis
        2
        >>> Statistic(player=p, game=g3, rbis=0).save()
        >>> p.rbis
        2
        >>> Statistic(player=p, game=g4, rbis=1).save()
        >>> p.rbis
        3
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.rbis, self.stats.all(), 0)
    rbis = property(_rbis_get)
    
    def _average_get(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=2, opponent_score=3, opponent="Test Opponent 5")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.average
        Decimal("0")
        
        >>> Statistic(player=p, game=g1, at_bats=4, walks=2, singles=1).save()
        >>> p.average
        Decimal("0.25")
        >>> Statistic(player=p, game=g2, at_bats=0, walks=0, doubles=0).save()
        >>> p.average
        Decimal("0.25")
        >>> Statistic(player=p, game=g3, at_bats=4, walks=1, triples=2, home_runs=1).save()
        >>> p.average
        Decimal("0.5")
        >>> Statistic(player=p, game=g4, at_bats=2, walks=1, home_runs=0).save()
        >>> p.average
        Decimal("0.4")
        >>> Statistic(player=p, game=g5, at_bats=1, walks=0, home_runs=1).save()
        >>> p.average
        Decimal("0.4545454545454545454545454545")
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if len(self.stats.all()) == 0:
            return Decimal("0")
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats") 
        return average(self.at_bats, self.hits)
    average = property(_average_get)
    
    def _on_base_percentage_get(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.on_base_percentage
        Decimal("0")
        >>> Statistic(player=p, game=g1, at_bats=0, walks=0, singles=0).save()
        >>> p.on_base_percentage
        Decimal("0")
        >>> Statistic(player=p, game=g2, at_bats=3, walks=1, doubles=2).save()
        >>> p.on_base_percentage
        Decimal("0.75")
        >>> Statistic(player=p, game=g3, at_bats=3, walks=1, home_runs=0).save()
        >>> p.on_base_percentage
        Decimal("0.5")
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return on_base_percentage(self.at_bats, self.walks, self.hits)
    on_base_percentage = property(_on_base_percentage_get)

    def _slugging_percentage_get(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=5, opponent_score=1, opponent="Test Opponent 5")
        >>> g6, created = Game.objects.get_or_create(game_date=date(2009, 06, 01), score=2, opponent_score=3, opponent="Test Opponent 6")
        >>> g7, created = Game.objects.get_or_create(game_date=date(2009, 07, 01), score=2, opponent_score=3, opponent="Test Opponent 7")
        >>> g8, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=2, opponent_score=3, opponent="Test Opponent 8")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.slugging_percentage
        Decimal("0")
        
        >>> Statistic(player=p, game=g1, at_bats=3, walks=3, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("0")
        
        >>> Statistic(player=p, game=g2, at_bats=3, walks=0, singles=1, doubles=1, triples=1, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1")
        
        >>> Statistic(player=p, game=g3, at_bats=4, walks=0, singles=1, doubles=1, triples=1, home_runs=1).save()
        >>> p.slugging_percentage
        Decimal("1.6")
        
        >>> Statistic(player=p, game=g4, at_bats=1, walks=0, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.545454545454545454545454545")
        
        >>> Statistic(player=p, game=g5, at_bats=1, walks=0, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.583333333333333333333333333")
        
        >>> Statistic(player=p, game=g6, at_bats=1, walks=0, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.692307692307692307692307692")
        
        >>> Statistic(player=p, game=g7, at_bats=1, walks=0, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.slugging_percentage
        Decimal("1.857142857142857142857142857")
        
        >>> Statistic(player=p, game=g8, at_bats=8, walks=0, singles=2, doubles=2, triples=2, home_runs=2).save()
        >>> p.slugging_percentage
        Decimal("2.090909090909090909090909091")
        
        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return slugging_percentage(self.at_bats, self.singles, self.doubles, self.triples, self.home_runs)
    slugging_percentage = property(_slugging_percentage_get)

class Game(models.Model):
    """
    >>> from datetime import date
    
    Test the null fields
    >>> g = Game.objects.create()
    Traceback (most recent call last):
        ...
    IntegrityError: (1048, "Column 'game_date' cannot be null")
    >>> g = Game.objects.create(game_date=date(2009, 01, 01))
    Traceback (most recent call last):
        ...
    IntegrityError: (1048, "Column 'score' cannot be null")
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0)
    Traceback (most recent call last):
        ...
    IntegrityError: (1048, "Column 'opponent_score' cannot be null")
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=-1, opponent_score=0)
    Traceback (most recent call last):
        ...
    Warning: Out of range value adjusted for column 'score' at row 1
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=-1)
    Traceback (most recent call last):
        ...
    Warning: Out of range value adjusted for column 'opponent_score' at row 1
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=0)
    >>> g.score = -1
    >>> g.save()
    Traceback (most recent call last):
        ...
    Warning: Out of range value adjusted for column 'score' at row 1
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=0)
    >>> g.opponent_score = -1
    >>> g.save()
    Traceback (most recent call last):
        ...
    Warning: Out of range value adjusted for column 'opponent_score' at row 1
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=0)
    >>> g.notes = "Test notes"
    >>> g.save()
    >>> str(g.notes)
    "Test notes"
    >>> g = Game.objects.get(pk=g.id)
    >>> str(g.notes)
    "Test notes"
    >>> str(g.opponent)
    "Unknown"
    >>> g = Game.objects.create(game_date=date(2009, 01, 01), score=0, opponent_score=0, opponent="Test Opponent")
    >>> g = Game.objects.get(pk=g.id)
    >>> str(g.opponent)
    "Test Opponent"
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    game_date = models.DateField()
    opponent = models.CharField(max_length=150, default="Unknown")
    players = models.ManyToManyField(Player, related_name="games", through="Statistic", null=True, blank=True)
    score = models.PositiveIntegerField()
    opponent_score = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ["game_date",]
    
    def _winner_get(self):
        """
        >>> g = Game(score=5, opponent_score=1, opponent="Test Opponent")
        >>> g.winner
        "Special Interests"
        >>> g = Game(score=1, opponent_score=5, opponent="Test Opponent")
        >>> g.winner
        "Test Opponent"
        >>> g = Game(score=5, opponent_score=5, opponent="Test Opponent")
        >>> g.winner
        "Tie"
        >>> g = Game(score=5, opponent_score=0, opponent="Test Opponent")
        >>> g.winner
        "Special Interests"
        >>> g = Game(score=0, opponent_score=5, opponent="Test Opponent")
        >>> g.winner
        "Test Opponent"
        >>> g = Game(score=0, opponent_score=0, opponent="Test Opponent")
        >>> g.winner
        "Tie"
        """
        if self.is_tie: return "Tie"
        elif self.is_loss: return self.opponent
        else: return "Special Interests"
    winner = property(_winner_get)
    
    def _is_win_get(self):
        """
        >>> g = Game(score=0, opponent_score=0)
        >>> g.is_win
        False
        >>> g = Game(score=1, opponent_score=1)
        >>> g.is_win
        False
        >>> g = Game(score=0, opponent_score=1)
        >>> g.is_win
        False
        >>> g = Game(score=2, opponent_score=3)
        >>> g.is_win
        False
        >>> g = Game(score=1, opponent_score=0)
        >>> g.is_win
        True
        >>> g = Game(score=3, opponent_score=2)
        >>> g.is_win
        True
        """
        return self.score > self.opponent_score
    is_win = property(_is_win_get)
    
    def _is_loss_get(self):
        """
        >>> g = Game(score=0, opponent_score=0)
        >>> g.is_loss
        False
        >>> g = Game(score=1, opponent_score=1)
        >>> g.is_loss
        False
        >>> g = Game(score=0, opponent_score=1)
        >>> g.is_loss
        True
        >>> g = Game(score=2, opponent_score=3)
        >>> g.is_loss
        True
        >>> g = Game(score=1, opponent_score=0)
        >>> g.is_loss
        False
        >>> g = Game(score=3, opponent_score=2)
        >>> g.is_loss
        False
        """
        return self.score < self.opponent_score
    is_loss = property(_is_loss_get)
    
    def _is_tie_get(self):
        """
        >>> g = Game(score=0, opponent_score=0)
        >>> g.is_tie
        True
        >>> g = Game(score=1, opponent_score=1)
        >>> g.is_tie
        True
        >>> g = Game(score=0, opponent_score=1)
        >>> g.is_tie
        False
        >>> g = Game(score=2, opponent_score=3)
        >>> g.is_tie
        False
        >>> g = Game(score=1, opponent_score=0)
        >>> g.is_tie
        False
        >>> g = Game(score=3, opponent_score=2)
        >>> g.is_tie
        False
        """
        return self.score == self.opponent_score
    is_tie = property(_is_tie_get)
    
    def __unicode__(self):
        """
        >>> from datetime import date
        >>> g = Game(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent")
        >>> str(g)
        "v. Test Opponent on Jan 01 (5 to 1)"
        """
        return "v. %s on %s (%s to %s)" % (self.opponent, self.game_date.strftime("%b %d"), self.score, self.opponent_score, )

class Statistic(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(Player, related_name="stats")
    game = models.ForeignKey(Game, related_name="stats")
    at_bats = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    singles = models.PositiveIntegerField(default=0)
    doubles = models.PositiveIntegerField(default=0)
    triples = models.PositiveIntegerField(default=0)
    home_runs = models.PositiveIntegerField(default=0)
    rbis = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ("player", "game")
    
    def __unicode__(self):
        return "%s %s (AB=%s, R=%s, H=%s, 2B=%s, 3B=%s, HR=%s, RBI=%s, BB=%s)" % (self.player, self.game, self.at_bats, self.runs, self.singles, self.doubles, self.triples, self.home_runs, self.rbis, self.walks, )

    def _hits_get(self):
        """
        Returns the total hits, doubles, triples, and home_runs

        >>> s = Statistic(singles=0, doubles=0, triples=0, home_runs=0)
        >>> s.hits
        0
        >>> s = Statistic(singles=1, doubles=0, triples=0, home_runs=0)
        >>> s.hits
        1
        >>> s = Statistic(singles=0, doubles=1, triples=0, home_runs=0)
        >>> s.hits
        1
        >>> s = Statistic(singles=0, doubles=0, triples=1, home_runs=0)
        >>> s.hits
        1
        >>> s = Statistic(singles=0, doubles=0, triples=0, home_runs=1)
        >>> s.hits
        1
        >>> s = Statistic(singles=1, doubles=2, triples=3, home_runs=4)
        >>> s.hits
        10        
        """
        return self.singles + self.doubles + self.triples + self.home_runs
    hits = property(_hits_get)

    def _average_get(self):
        """
        Avg = H / AB

        >>> s = Statistic(at_bats=4, walks=2, singles=1)
        >>> s.average
        Decimal("0.25")
        >>> s = Statistic(at_bats=0, singles=0)
        >>> s.average
        Decimal("0")
        >>> s = Statistic(at_bats=7, doubles=2, triples=3)
        >>> s.average                
        Decimal("0.7142857142857142857142857143")
        >>> s = Statistic(at_bats=2, singles=0)
        >>> s.average                
        Decimal("0")
        >>> s = Statistic(at_bats=1, singles=1)
        >>> s.average
        Decimal("1")
        
        At bats cannot be 0 if hits are not 0
        >>> s = Statistic(at_bats=0, singles=1)
        >>> s.average
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        
        Hits cannot be greater than at bats
        >>> s = Statistic(at_bats=1, singles=2)
        >>> s.average
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats") 
        return average(self.at_bats, self.hits)
    average = property(_average_get)

    def _on_base_percentage_get(self):
        """
        OBP = (H + BB) / (AB + BB)
        
        >>> s = Statistic()
        >>> s.on_base_percentage
        Decimal("0")
        >>> s = Statistic(at_bats=4, walks=2, singles=1)
        >>> s.on_base_percentage
        Decimal("0.5")
        >>> s = Statistic(at_bats=3, walks=1, triples=2)
        >>> s.on_base_percentage
        Decimal("0.75")
        
        At bats cannot be 0 if walks or hits are not 0
        >>> s = Statistic(at_bats=0, walks=1, singles=0)
        >>> s.on_base_percentage
        Decimal("0")
        
        At bats cannot be 0 if walks or hits are not 0
        >>> s = Statistic(at_bats=0, walks=0, singles=1)
        >>> s.on_base_percentage
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        
        Hits cannot be greater than at bats
        >>> s = Statistic(at_bats=1, walks=1, singles=2)
        >>> s.on_base_percentage
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return on_base_percentage(self.at_bats, self.walks, self.hits)
    on_base_percentage = property(_on_base_percentage_get)
    
    def _slugging_percentage_get(self):
        """
        >>> s = Statistic()
        >>> s.slugging_percentage
        Decimal("0")
        
        >>> s = Statistic(at_bats=3, walks=3, singles=0, doubles=0, triples=0, home_runs=0)
        >>> s.slugging_percentage
        Decimal("0")
        
        >>> s = Statistic(at_bats=3, walks=0, singles=1, doubles=1, triples=1, home_runs=0)
        >>> s.slugging_percentage
        Decimal("2")
        
        >>> s = Statistic(at_bats=4, walks=0, singles=1, doubles=1, triples=1, home_runs=1)
        >>> s.slugging_percentage
        Decimal("2.5")
        
        >>> s = Statistic(at_bats=1, walks=0, singles=1, doubles=0, triples=0, home_runs=0)
        >>> s.slugging_percentage
        Decimal("1")
        
        >>> s = Statistic(at_bats=1, walks=0, singles=0, doubles=1, triples=0, home_runs=0)
        >>> s.slugging_percentage
        Decimal("2")
        
        >>> s = Statistic(at_bats=1, walks=0, singles=0, doubles=0, triples=1, home_runs=0)
        >>> s.slugging_percentage
        Decimal("3")
        
        >>> s = Statistic(at_bats=1, walks=0, singles=0, doubles=0, triples=0, home_runs=1)
        >>> s.slugging_percentage
        Decimal("4")
        
        >>> s = Statistic(at_bats=8, walks=0, singles=2, doubles=2, triples=2, home_runs=2)
        >>> s.slugging_percentage
        Decimal("2.5")
        
        >>> s = Statistic(at_bats=0, walks=1, singles=0)
        >>> s.slugging_percentage
        Decimal("0")
        
        At bats cannot be 0 if hits are not 0
        >>> s = Statistic(at_bats=0, walks=0, singles=1)
        >>> s.slugging_percentage
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        
        Hits cannot be greater than at bats
        >>> s = Statistic(at_bats=1, walks=1, singles=2)
        >>> s.slugging_percentage
        Traceback (most recent call last):
            ...
        ValueError: hits must be <= at_bats
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return slugging_percentage(self.at_bats, self.singles, self.doubles, self.triples, self.home_runs)
    slugging_percentage = property(_slugging_percentage_get)
        