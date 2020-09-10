class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        import random
        fn = ['Jim','Bob','Janet','Mary','Sheela','Yin','Ahmed','Raj']
        ln = ['Patel','Robinson','Smith','Shaikh','Wong','Fernandez','Singh','DeMello']
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(num_users):
            self.add_user(random.choice(fn)+' '+random.choice(ln)) 

        for i in self.users:
            for j in range(random.randrange(0,4)):
                choose_friends = [i for i in set(self.users) - {i}]
                self.add_friendship(i, random.choice(choose_friends))
                # self.add_friendship(i,random.choice()
       

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        visited = {i:False for i in self.users}
        
        # breakpoint()

        connections = {}
        # for i in 

        for i in self.users:
            if i != user_id:
                connections[i] = self.get_path_to_friend(user_id,i)
        
        return connections

    # helper function that returns shortest path from a friend to another friend in a network
    # this will implement an iterative BFS algorithm
    def get_path_to_friend(self, vertex, target): 

        from util import Queue
        visited = {i:False for i in self.users}
        to_visit = Queue()
        to_visit.enqueue([vertex])
        
        while to_visit.size() != 0:
            current_path = to_visit.dequeue() #path-to-current
            current_value = current_path[-1]
            if visited[current_value] == False:
                visited[current_value] = True
                if current_value == target:
                    return current_path
                else:
                    for i in self.friendships[current_value]:
                        to_visit.enqueue(current_path + [i])

            



        
    


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
