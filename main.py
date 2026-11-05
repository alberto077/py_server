
from uuid import UUID, uuid4

# Find out what data structure is better than a list especially when people are joining and leaving lobbys how can we profile performance
# Create a server with fast api allow curl requests to different endpoints in order to make a user and other crud operations 
# Add and endpoint to connect to a lobby 
# Allow lobbies to be their own servers maybe their own processes on a docker conatainer and then have the connections to a lobby be the current capacity
# With the server implementation we probably have to set a connection capacity within the fastapi server something I can look into 
# databse for stats with a player

class Lobby():
    _current_total_active_players: int = 0
    _current_active_lobbys: int = 0
    _lobby_instance: list[Lobby] = []
    def __init__(self, *, max_capacity: int) -> None:
        self.max_capacity: int = max_capacity
        self.current_capacity:int = 0
        self.current_players: list[UUID] = []
        self.index = Lobby._current_active_lobbys
        Lobby._current_active_lobbys += 1
        Lobby._lobby_instance.append(self)

    @staticmethod
    def all_lobby_stats() -> str:
        return f"Total Active Players: {Lobby._current_total_active_players}\nTotal Active Lobbys: {Lobby._current_active_lobbys}\n Players in the lobbys = {[f"{player}" for lobby in Lobby._lobby_instance for player in lobby.current_players]}"

    @classmethod
    def process_player(cls, *, player: Player) -> str:
        lowest_lobby: Lobby = min(cls._lobby_instance, key= lambda lobby: lobby.current_capacity)
        if lowest_lobby.current_capacity == lowest_lobby.max_capacity:
            return "Lobby is full"
        lowest_lobby.current_capacity +=1
        lowest_lobby.current_players.append(player.id)
        Lobby._current_total_active_players += 1
        player.current_lobby_index = lowest_lobby.index
        return f"{player.name} has joined lobby {lowest_lobby.index} successfully"
    @classmethod
    def remove_player(cls, *, player: Player) -> str:

        # Needs validation
        lobby: Lobby = Lobby._lobby_instance[player.current_lobby_index]

        print(lobby.current_players)
        lobby.current_players.remove(player.id)
        lobby.current_capacity -=1
        player.current_lobby_index = -1
        Lobby._current_total_active_players -=1

        return f"{player.name} has left lobby {lobby.index+1}"


class Player:
    total_players_accounts: int = 0
    def __init__(self, *, name: str) -> None:
        self.name: str = name
        self.id: UUID = uuid4()
        self.current_lobby_index: int = -1
        Player.total_players_accounts +=1
        print(f"Player {self.name} Created")

    def join_lobby(self) -> str:
        return Lobby.process_player(player=self)

    def leave_lobby(self) -> str:
        return Lobby.remove_player(player=self)



def main():
    lobby1: Lobby = Lobby(max_capacity=10)
    lobby2: Lobby = Lobby(max_capacity=10)
    lobby3: Lobby = Lobby(max_capacity=10)

    print(Lobby.all_lobby_stats())

    p1: Player = Player(name= "Alberto")
    p2: Player = Player(name= "Tay")

    print(Lobby.all_lobby_stats())
    
    print(p1.join_lobby())

    print(Lobby.all_lobby_stats())


    print(p2.join_lobby())

    print(Lobby.all_lobby_stats())

    print(p2.leave_lobby())
    print(p1.leave_lobby())

    print(Lobby.all_lobby_stats())
if __name__ == '__main__':
    main()
