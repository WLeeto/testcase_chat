import asyncio
from app.db import AsyncSessionLocal
from app.models.models import User, Chat


async def main():
    async with AsyncSessionLocal() as session:
        # Создать пользователя
        user = User(name="testuser", email="test@example.com", password="testpass")
        session.add(user)
        await session.flush()  # Получить user.id

        # Создать чат
        chat = Chat(name="Test Chat", type="private")
        session.add(chat)
        await session.commit()
        print(f"User ID: {user.id}, Chat ID: {chat.id}")


if __name__ == "__main__":
    asyncio.run(main())
