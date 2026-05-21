from sqlmodel import Session, select
from app.core.database import create_tables, engine
from app.core.security import hash_password
from app.models.usuario import Usuario

def seed():
    create_tables()
    with Session(engine) as session:
        if session.exec(select(Usuario)).first():
            print("Database already has users. Skipping seed.")
            return
        session.add(Usuario(username="admin", password_hash=hash_password("admin123"), role="admin"))
        session.add(Usuario(username="user", password_hash=hash_password("user123"), role="user"))
        session.commit()
        print("Initial users created: admin/admin123, user/user123")

if __name__ == "__main__":
    seed()
