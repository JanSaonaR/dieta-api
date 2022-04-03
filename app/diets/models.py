class Child:
    def __init__(self, age, weight, height, activity):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity

    def serialize(self):
        return {
                'age': self.age,
                'weight': self.weight,
                'height': self.height,
                'activity': self.activity
                }
