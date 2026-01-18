from datetime import date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import String, Column, Integer, create_engine, Date
from sqlalchemy import ForeignKey


Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	email = Column(String, unique=True, nullable=False)

	bookings = relationship("Booking", back_populates="user")

class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	aftor = Column(String, nullable=False)

	dostupn_copies = Column(Integer)
	bookings = relationship("Booking", back_populates="book")


class Booking(Base):
	__tablename__ = "bookings"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	book_id = Column(Integer, ForeignKey("books.id"))
	booking_date = Column(Date, default=date.today())

	user = relationship("User", back_populates="bookings")
	book = relationship("Book", back_populates="bookings")
class Biblioteka:
	def f(self, db_url = "sqlite:///library.db"):
		self.engine = create_engine(db_url)
		Base.metadate.creata_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def add_user(self, name, email):
		try:
			user = User(name = name, email = email)
			self.session.add(user)
			self.session.commit()
			return user
		except Exception as z:
			self.session.rollback()
			raise z

	def add_book(self, title, aftor, dostupn_copies):
		try:
			book = Book(title=title, aftor=aftor, dostupn_copies=dostupn_copies)
			self.session.add(book)
			self.session.commit()
			return book
		except Exception as z:
			self.session.rollback()
			raise z

	def create_booking(self, user_id, book_id):
		try:
			book = self.session.query(Book).get(book_id)
			if not book or book.dostupn_copies <=0:
				raise ValueError("Книга недоступна для бронирования")
			booking = Booking(user_id = user_id, book_id = book_id)
			book.dostupn_copies -= 1

			self.session.add(booking)
			self.session.commit()
			return booking
		except Exception as z:
			self.session.rollback()
			raise z
	def del_booking(self, booking_id):
		try:
			booking = self.session.query(Booking).get(booking_id)
			if not booking:
				raise ValueError("Бронирование не найдено")

			book = booking.book
			book.dostupn_copies += 1

			self.session.delete((booking))
			self.session.commit()
		except Exception as z:
			self.session.rollback()
			raise z

	def get_book_dostupn(self, book_id):
		book = self.session.query(Book).get(book_id)
		return book.dostupn_copies if book else 0
	def get_user_book(self, user_id):
		return self.session.query(Booking).filter_by(user_id = user_id).all()

	def close(self):
		self.session.close()