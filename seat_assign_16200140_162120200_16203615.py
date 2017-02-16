import sqlite3
import csv



class readCSV(object):

	def __init__(self,fileName):
		self.fileName=fileName
		self.bookingData=[]

	#reads csv file into bookingData variable
	def readFile(self):
		with open(self.fileName,'rb') as f:
			reader=csv.reader(f)
			for row in reader:
				self.bookingData.append(row)


class database(object):

	def __init__(self,fileName):
		self.fileName=fileName
		self.seatChars=[]

	#returns number of the rows in the plane from the database
	def getRows(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		c.execute('Select nrows from rows_cols')
		rows = c.fetchone()[0]
		conn.close()
		return rows

	#returns number of columns in the plane and get column codes for seats from the database
	def getColumns(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		c.execute('Select seats from rows_cols')
		cols = c.fetchone()[0]
		count=0
		for char in cols:
			self.seatChars.append(char)
			count=count+1
		conn.close()
		return count



	#returns the remaining seats

	def getRemainingSeats(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select count(seat) from seating where name=""'
		c.execute(cmd)
		totalEmptySeats=c.fetchone()[0]
		conn.close()
		return totalEmptySeats

	#returns the number of empty seats in a row
	#to do try catch
	def getEmptySeatsInRow(self, rowNumber):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select count(seat) from seating where row=(?) and name=""'
		c.execute(cmd,(rowNumber,))
		emptySeats=c.fetchone()[0]
		conn.close()
		return emptySeats
 
	#return the list of rows having empty seats more than required sets
	def getEmptyRowBySeats(self,requiredSeats):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select row,count(seat) as numOfSeats from seating  where name="" group by row  having numOfSeats>=(?)'
		rowsCount=c.execute(cmd,(requiredSeats,))
		if rowsCount>0:
			rowNumber=c.fetchone()[0]
			print(emptySeats)
		else:
			rowNumber=-1
		conn.close()
		return rowNumber

	#return the array of seats available by row
	def getEmptySeatsArray(self,row):
		seats=[]
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select seat from seating where row=(?) and name=""'
		try:
			c.execute(cmd,(row,))
			for row in c:
				seat=row[0]
				seats.append(seat)
				print(seat)
			conn.close()
			return seats
		except:
			print("Unable to connect with database")


	#saves the details of the booked seats in the database
	def addBookedSeatsRecord(self,row,seat,name):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Update seating set name=(?) where row=(?) and seat=(?)'
		try:
			c.execute(cmd,(name,row,seat))
			conn.commit()
			rowsCount=c.rowcount
			if rowsCount>0:

				print("Seat added successfully")
				print(row)
				print(seat)
				print(name)
				conn.close()
				return rowsCount
			else:
				print("error in booking")
				conn.close()
				return -1
		except:
			print("Unable to connect with database")
			conn.close()

class seatAllocator(database):

	def __init__(self,rows,columns,dbName):
		self.maxSeats=rows*columns
		self.rows=rows
		self.columns=columns
		self.seatsAvailable=self.maxSeats
		self.seatsBooked=0
		self.bookingsRefused=0
		self.awayPassengers=0
		self.seatsInRow=self.maxSeats/columns
		self.seatChars=[]
		database.__init__(dbName)


	def printInfo(self):
		print("Maximum number of seats: {}".format(self.maxSeats))
		print("Number of rows: {}".format(self.rows))
		print("Number of columns: {}".format(self.columns))
		print("Number of seats in a row: {}".format(self.seatsInRow))

	def checkSeats(self,requestedSeats):
		if(self.seatsAvailable<requestedSeats):
			print("Seats not available")
			self.bookingsRefused+=requestedSeats
			print("Total bookings refused till now {}".format(self.bookingsRefused))

	def bookSeats(self,numberOfSeats,name):
		
		#get total seats remaining
		remainingSeats=database.getRemainingSeats()
		seats=[]
		#check with remaining seats
		if(numberOfSeats<remainingSeats):
			
			#check if passengers can be accomodated in a single row
			if(numberOfSeats<=self.columns):
				bookedRow=database.getEmptyRowBySeats(numberOfSeats)
				if(bookedRow==-1):
					print("No seats available")
				else:
					print("Seats can be booked in row: {}".format(bookedRow))
					#get the empty seats in the row
					seats=database.getEmptySeatsArray(bookedRow)
					#check for if seats are empty
					if seats:
						count=0
						for seat in seats:
							if count<numberOfSeats:
								bookingResult=database.addBookedSeatsRecord(bookedRow,seat,name)
								if bookingResult==1:
									count+=1
									print("Seat booked successfully")
									print(seat)
									print(bookedRow)
								else:
									print("Error in booking of seats")

			else:
				print("python indentation sucks")
				# do modulus, break down seats according to columns

		else:
			print("Not enough seats available. Remaining seats are {}".format(remainingSeats))
			self.bookingsRefused+=numberOfSeats
			print("booking refused till now {}".format(self.bookingsRefused))

dbName='data.db'
database=database(dbName)
rows=database.getRows()
cols=database.getColumns()


booking=seatAllocator(rows,cols,dbName)
booking.seatChars=database.seatChars
booking.printInfo()

emptySeats=database.getEmptySeatsInRow(1)
print('empty seats in row={}'.format(emptySeats))

totalEmptySeats=database.getRemainingSeats()
print('remaining seats: {}'.format(totalEmptySeats))


booking.bookSeats(4,'Flo')

#database.getEmptyRowBySeats(3)



#readCSV=readCSV('bookings.csv')
#readCSV.readFile()


