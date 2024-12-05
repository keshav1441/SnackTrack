from sqlalchemy import Column, Integer, String,Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from database import Base

# Order Status Choices
Order_Status = [
    ('PENDING', 'pending'),
    ('IN-TRANSIT', 'in-transit'),
    ('DELIVERED', 'delivered')
]

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    
    # Relationship to Order
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

# Menu Model
class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationship to Item
    items = relationship("Item", back_populates="menu")
    
    def __repr__(self):
        return f"<Menu(name={self.name})>"

# Item Model
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    
    # Relationship to Menu
    menu = relationship("Menu", back_populates="items")
    
    def __repr__(self):
        return f"<Item(name={self.name}, price={self.price})>"

# Order Model
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(Order_Status), default="PENDING")
    
    # Relationships
    user = relationship("User", back_populates="orders")
    item = relationship("Item")
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, item_id={self.item_id}, quantity={self.quantity}, status={self.order_status})>"
