import random


class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.new_round()
        # Statistics tracking for additional feature
        self.player_wins = 0
        self.dealer_wins = 0
        self.pushes = 0

    # ROUND MANAGEMENT

    def new_round(self):
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        # Instead of removing cards from the deck,
        # we keep an index of the "next card" to deal.
        self.deck_position = 0

        # Hands start empty; cards will be dealt after UI calls deal_initial_cards()
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    def deal_initial_cards(self):
        """
        Deal two cards each to player and dealer.
        """
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    # DECK AND CARD DRAWING

    def create_deck(self):
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        """
        Return the next card in the shuffled deck.
        """
        card = self.deck[self.deck_position]
        self.deck_position += 1
        return card

    # HAND VALUES + ACE HANDLING

    def card_value(self, card):
        """
        Convert a card string into its numeric value.

        Rules:
        - Number cards = their number (2–10)
        - J, Q, K = 10
        - A is normally 11, may later count as 1 if needed
        """
        rank = card[:-1]  # everything except the suit symbol

        if rank in ["J", "Q", "K"]:
            return 10

        if rank == "A":
            return 11  # Initially treat Ace as 11

        # Otherwise it's a number from 2 to 10
        return int(rank)

    def hand_total(self, hand):
        """
        Calculates the best possible total for a hand.
        Aces are counted as 11 unless this would bust the hand,
        in which case they are reduced to 1.

        Suggested Process:
        1. Count all Aces as 11 initially.
        2. If total > 21, subtract 10 for each Ace, so it effectively makes them = 1
        """
        total = 0
        ace_count = 0

        # Calculate initial total and count aces
        for card in hand:
            value = self.card_value(card)
            total += value
            if card[:-1] == "A":
                ace_count += 1

        # Adjust for aces if busting
        # Convert aces from 11 to 1 by subtracting 10
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total

    # PLAYER ACTIONS

    def player_hit(self):
        # Add one card to the player's hand and return it, so the UI can display the card
        new_card = self.draw_card()
        self.player_hand.append(new_card)
        return new_card

    def player_total(self):
        # Return the player's total
        return self.hand_total(self.player_hand)

    # DEALER ACTIONS

    def reveal_dealer_card(self):
        # Called when the player presses Stand. After this, the UI should show both dealer cards
        self.dealer_hidden_revealed = True

    def dealer_total(self):
        # Return the dealer's total
        return self.hand_total(self.dealer_hand)

    def play_dealer_turn(self):
        # Dealer must hit until their total is 17 or more, then stand
        while self.dealer_total() < 17:
            self.dealer_hand.append(self.draw_card())

    # WINNER DETERMINATION

    def decide_winner(self):
        # Decide the outcome of the round
        """
        Example: return the following text messages:
        - "Player busts. Dealer wins!"
        - "Dealer busts. Player wins!"
        - "Player wins!"
        - "Dealer wins!"
        - "Push (tie)."
        """
        player_score = self.player_total()
        dealer_score = self.dealer_total()

        # Check for player bust
        if player_score > 21:
            self.dealer_wins += 1
            return "Player busts. Dealer wins!"

        # Check for dealer bust
        if dealer_score > 21:
            self.player_wins += 1
            return "Dealer busts. Player wins!"

        # Both have valid hands, compare totals
        if player_score > dealer_score:
            self.player_wins += 1
            return "Player wins!"
        elif dealer_score > player_score:
            self.dealer_wins += 1
            return "Dealer wins!"
        else:
            self.pushes += 1
            return "Push (tie)."

    # STATISTICS METHODS (Additional Feature)
    def get_statistics(self):
        """Return game statistics as a dictionary"""
        total_games = self.player_wins + self.dealer_wins + self.pushes
        return {
            'player_wins': self.player_wins,
            'dealer_wins': self.dealer_wins,
            'pushes': self.pushes,
            'total_games': total_games
        }

    def reset_statistics(self):
        """Reset all game statistics to zero"""
        self.player_wins = 0
        self.dealer_wins = 0
        self.pushes = 0