#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>._
# 
#    Author : Jorge Fernandez Gonzalez <jorge.fernandez.gonzalez __at__ gmail.com>
#

from apps.gymkhana.models import *

def create(number, help, challenge, CORRECTION_FACTOR):
    clue = Clue()
    clue.challenge = challenge
    clue.number = number
    clue.help = help
    factor = CORRECTION_FACTOR * (number)
    clue.cost = round(challenge.max_score * factor) # 10%, 20%, 30% del max_score
    clue.save()
    return True, clue

def show(team, challenge):
    acquired_clues = AcquiredClue.objects.filter(team=team)
    acquired_clues.order_by('number')
    success = 0
    for acquired_clue in acquired_clues:
      if acquired_clue.clue.challenge == challenge:
        success = 1
    if success == 1:
      return True, acquired_clues
    else:
      return False, "You Have Not Got A Clue."

def buy(event, team, challenge):
    clue_to_buy = Clue()
    clues_challenge = challenge.clue_set.all().order_by('number')
   
    success = 0
    for i in range(len(clues_challenge)):
      clue_to_buy = clues_challenge[i]
      acquired_clues = AcquiredClue.objects.filter(team=team)
      for j in range(len(acquired_clues)):
        if clues_challenge[i] == acquired_clues[j].clue:
          success = 1

      if success == 0:
        new_acquired_clue = AcquiredClue(team=team,clue=clue_to_buy)
        new_acquired_clue.save()
        scoreboard = Scoreboard.objects.get(event=event,team=team)
        scoreboard.score = scoreboard.score - clue_to_buy.cost
        scoreboard.save()
        team.save()
        return True, clue_to_buy
      success = 0
    return False, "No More Clues For This Team And Challenge."
