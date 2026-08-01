import random
from faker import Faker
from app import create_app, db
from app.models import User, Note

fake = Faker()

def seed_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        users = []
        for i in range(5):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
            )
            user.set_password('password123')
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        categories = ['Personal', 'Work', 'Study', 'Ideas', 'Projects']
        
        for user in users:
            for j in range(10):
                note = Note(
                    title=fake.sentence(nb_words=6),
                    content='\n\n'.join(fake.paragraphs(nb=3)),
                    category=random.choice(categories),
                    is_archived=random.choice([True, False]),
                    user_id=user.id,
                    created_at=fake.date_time_this_year(),
                    updated_at=fake.date_time_this_month()
                )
                db.session.add(note)
        
        db.session.commit()
        
        print(f"Database seeded successfully!")
        print(f"Created {len(users)} users with 10 notes each")
        print("\nTest users:")
        for user in users:
            print(f"- Username: {user.username}, Password: password123")

if __name__ == "__main__":
    seed_database()
