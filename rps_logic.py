# rps_logic.py
import random

CHOICES = ["rock", "paper", "scissors"]

def cpu_choice():
    """Return a random choice for CPU."""
    return random.choice(CHOICES)

def resolve_rps(player, cpu):
    """
    Resolve result.
    Returns one of: "win", "lose", "tie"
    """
    player = player.lower()
    cpu = cpu.lower()
    if player == cpu:
        return "tie"

    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }
    return "win" if wins[player] == cpu else "lose"

def payout_total_return(bet):
    """
    Option A: total return is 1.96x bet.
    Returns integer amount to add to bankroll on a win (total money returned to player).
    """
    return int(round(bet * 1.96))
