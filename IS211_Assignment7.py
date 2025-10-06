import random
import sys

class Die:
    # Represents a single die8
    
    def __init__(self, sides=6):
        self.sides = sides
        random.seed(0)  
    
    def roll(self):
        return random.randint(1, self.sides)

class Player:
    # Represents a player
    
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.turn_score = 0
    
    def reset_turn(self):
        # Reset the player's turn-specific score
        self.turn_score = 0
    
    def add_to_turn(self, points):
        # Add points to the current turn score
        self.turn_score += points
    
    def hold(self):
        # Add turn score to total score and end turn
        self.total_score += self.turn_score
        self.reset_turn()
        return self.total_score
    
    def __str__(self):
        return f"{self.name} (Total: {self.total_score})"

class PigGame:
    # Manages the Pig game state and flow
    
    winning_score = 100
    
    def __init__(self, num_players=2):
        self.players = []
        self.die = Die()
        self.current_player_index = 0
        self.game_over = False
        
        # Create players
        for i in range(num_players):
            player_name = f"Player {i+1}"
            self.players.append(Player(player_name))

    @property
    def current_player(self):
        # Get the current player
        return self.players[self.current_player_index]
    
    def switch_player(self):
        # Switch to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def display_game_state(self):
        # Display current game state
        print("\n" + "="*50)
        print("CURRENT GAME STATE:")
        for player in self.players:
            print(f"  {player}")
        print(f"Current turn: {self.current_player.name}")
        print(f"Turn score: {self.current_player.turn_score}")
        print("="*50)
    
    def process_roll(self):
        # Player rolls
        roll = self.die.roll()
        print(f"\n{self.current_player.name} rolled: {roll}")
        
        if roll == 1:
            print("Oops! Rolled a 1. Turn ends with no points.")
            self.current_player.reset_turn()
            self.switch_player()
            return False  # Turn ends
        else:
            self.current_player.add_to_turn(roll)
            print(f"Added {roll} to turn score. Turn total: {self.current_player.turn_score}")

            # Check if this roll wins the game
            if self.current_player.total_score + self.current_player.turn_score >= self.winning_score:
                self.game_over = True
                print(f"{self.current_player.name} WINS WITH {self.current_player.total_score + self.current_player.turn_score} POINTS!")
                return False
        
            return True  # Turn continues
    
    def process_hold(self):
        # Player holds
        print(f"\n{self.current_player.name} holds!")
        new_score = self.current_player.hold()
        print(f"Added turn score to total. New total: {new_score}")
       
        self.switch_player()
        return True
    
    def get_player_decision(self):
        # Get and validate player decision
        while True:
            decision = input("\nEnter 'r' to roll, 'h' to hold, 'q' to quit: ").strip().lower()
            if decision in ['r', 'h', 'q']:
                return decision
            else:
                print("Invalid input. Please enter 'r' to roll, 'h' to hold, 'q' to quit.")
    
    def play_turn(self):
        # Play a single turn for the current player
        print(f"\n--- {self.current_player.name}'s Turn ---")
        
        while True:
            self.display_game_state()
            
            decision = self.get_player_decision()
            
            if decision == 'r':
                turn_continues = self.process_roll()
                if not turn_continues:
                    break
            elif decision == 'h':
                game_continues = self.process_hold()
                if not game_continues:
                    break
                else:
                    break  # Turn ends after hold but game continues
            elif decision == 'q':
                print("Thanks for playing. Please come again.")
                input("Press Enter to Exit.") 
                sys.exit()
    
    def play_game(self):
        """Main game loop"""
        print("WELCOME TO PIG GAME!")
        print("Rules:")
        print("- Roll the die to accumulate points for your turn.")
        print("- If you roll a 1, you lose all points for that turn!")
        print("- Hold to add your turn points to your total score.")
        print(f"- First player to reach {self.winning_score} points wins!")
        print("- Enter 'r' to roll, 'h' to hold, 'q' to quit\n")
        
        while not self.game_over:
            self.play_turn()
        
        self.display_final_results()
    
    def display_final_results(self):
        """Display final game results"""
        print("\n" + "="*50)
        print("FINAL RESULTS:")
        print("="*50)
        for player in self.players:
            print(f"  {player.name}: {player.total_score + self.current_player.turn_score} points")
        print("="*50)

def config_num_players():
    # Configuring number of players
    num_players = 2  # Default
    
    if '--numPlayers' in sys.argv:
        try:
            index = sys.argv.index('--numPlayers')
            if index + 1 < len(sys.argv):
                num_players = int(sys.argv[index + 1])
                if num_players < 2:
                    print("Warning: Number of players must be at least 2.")
                    sys.exit()
        except (ValueError, IndexError):
            print("Warning: Invalid --numPlayers argument. Defaulting to 2 players.\n")

    return num_players

def main():
    # Check for command line arguments for extra credit
    num_players = config_num_players()
    
    if num_players > 2:
        print(f"Starting game with {num_players} players (Extra Credit Feature!)")
    
    # Create and play the game
    game = PigGame(num_players)
    game.play_game()
    
    # Option to play again
    while True:
        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if play_again == 'y':
            game = PigGame(num_players)
            game.play_game()
        elif play_again == 'n':
            print("Thanks for playing Pig Game! Goodbye!")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()