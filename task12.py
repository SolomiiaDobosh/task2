import pickle
import shelve
import json

class Weapon:
    def __init__(self, name, hit_percentage):
        self.name = name
        self.hit_percentage = hit_percentage

    def __str__(self):
        return f"{self.name} - {self.hit_percentage}%"

    def __repr__(self):
        return f"Weapon('{self.name}', {self.hit_percentage})"

class Shooting(Weapon):
    def __init__(self, name, hit_percentage, shot_count):
        super().__init__(name, hit_percentage)
        self.shot_count = shot_count

    def hit_probability(self):
        return (self.hit_percentage / 100) * self.shot_count

    def __lt__(self, other):
        return self.shot_count < other.shot_count

    def __repr__(self):
        return f"Shooting('{self.name}', {self.hit_percentage}, {self.shot_count})"

class ShootingList:
    def __init__(self):
        self.shoot_list = []

    def add_shoot(self, shoot):
        self.shoot_list.append(shoot)

    def save_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.shoot_list, f)

    def load_pickle(self, filename):
        with open(filename, 'rb') as f:
            self.shoot_list = pickle.load(f)

    def save_shelve(self, filename):
        with shelve.open(filename) as db:
            db['shoot_list'] = self.shoot_list

    def load_shelve(self, filename):
        with shelve.open(filename) as db:
            self.shoot_list = db.get('shoot_list', [])

    def save_text(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for shoot in self.shoot_list:
                f.write(repr(shoot) + '\n')

    def load_text(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.shoot_list = [eval(line.strip()) for line in f]

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([shoot.__dict__ for shoot in self.shoot_list], f)

    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.shoot_list = [Shooting(**item) for item in data]

if __name__ == "__main__":
    shooting_list = ShootingList()
    shooting_list.add_shoot(Shooting("Pistol", 70, 10))
    shooting_list.add_shoot(Shooting("Sniper Rifle", 90, 5))
    
    shooting_list.save_pickle("shooting.pkl")
    shooting_list.load_pickle("shooting.pkl")
    
    shooting_list.save_shelve("shooting_shelve")
    shooting_list.load_shelve("shooting_shelve")
    
    shooting_list.save_text("shooting.txt")
    shooting_list.load_text("shooting.txt")
    
    shooting_list.save_json("shooting.json")
    shooting_list.load_json("shooting.json")
    
    for shoot in shooting_list.shoot_list:
        print(shoot)
