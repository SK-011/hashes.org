#!/usr/bin/env python

import sys
import urllib
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
import os
import py7zlib
import MySQLdb
import time



db_user = "hashes"
db_pass = "h@5h35"
db_data = "hashes"
db_table = "passwords"
queue_size = 2131072



def download (q_download, q_extract):
	url = urllib.URLopener ()
	print ("[*]\t[download]: Waiting for URL to download")
	sys.stdout.flush ()

	while True:
		leak_id = q_download.get ()

		# Leak id 560 dump is shitty, don't treat it
		if leak_id == "560":
			continue
			
		link = "https://hashes.org/download.php?type=leak&id=%s&list=found" % leak_id
		print ("[*]\t[download]: Retrieving %s" % link)
		sys.stdout.flush ()
		url.retrieve (link, leak_id + ".7z")
		q_extract.put (leak_id + ".7z")
		q_download.task_done ()
		print ("[*]\t[download]: %s download done, %i to go" % (link, q_download.qsize ()))
		sys.stdout.flush ()


def extract (q_extract, q_insert):
	print ("[*]\t[extract]: Waiting for archive to extract")
	sys.stdout.flush ()

	while True:
		archive_name = q_extract.get ()
		print ("[*]\t[extract]: Extracting %s" % archive_name)
		sys.stdout.flush ()

		fp = open (archive_name, "rb")
		archive = py7zlib.Archive7z (fp)

		# For each file in the archive
		for member in archive.getmembers ():

			# Recover its content
			content = member.read ()
			lines = content.split ('\n')

			# Put each line of the current file in the insertion queue
			for line in lines:
				q_insert.put (line)

		# Close and delete the archive
		fp.close ()
		os.remove (archive_name)
		q_extract.task_done ()
		print ("[*]\t[extract]: %s extraction done, %i to go" % (archive_name, q_extract.qsize ()))
		sys.stdout.flush ()


def insert (q_insert, db_con):
	print ("[*]\t[insert]: Waiting for passwords to insert")
	sys.stdout.flush ()

	db_cur = db_con.cursor ()
	count = 0

	while True:
		password = q_insert.get ()
		sql = "INSERT INTO %s VALUES (%s)" % (db_table, db_con.escape (password))

		try:
			db_cur.execute (sql)

		except MySQLdb.Error as error:
			pass

		q_insert.task_done ()

		# Every 4096 insertions
		if count % 65536 == 0:

			try:
				db_cur.execute ("commit")

			except MySQLdb.Error as error:
				print ("Commit exception")
				sys.stdout.flush ()

			print ("[*]\t[insert]: %i insertions done, %i still in queue" % (count, q_insert.qsize ()))
			sys.stdout.flush ()

		count = count + 1



def main (args):
	index = "index.html"
	url = urllib.URLopener ()
	print ("[*]\tRetrieving the index")
	sys.stdout.flush ()
	url.retrieve ("https://hashes.org/public.php", index)

	print ("[*]\tParsing the index")
	sys.stdout.flush ()
	soup = BeautifulSoup (open (index), "lxml")

	# Create the queues
	q_download = Queue (maxsize = queue_size)
	q_extract = Queue (maxsize = queue_size)
	q_insert = Queue (maxsize = queue_size)

	# Start the threads
	t_download = Thread (target = download, args = (q_download, q_extract))
	t_download.setDaemon (True)
	t_download.start ()

	t_extract = Thread (target = extract, args = (q_extract, q_insert))
	t_extract.setDaemon (True)
	t_extract.start ()

	db_con_0 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	db_con_1 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	db_con_2 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	db_con_3 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	db_con_4 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	db_con_5 = MySQLdb.connect (user = db_user, passwd = db_pass, db = db_data)
	
	t_insert_0 = Thread (target = insert, args = (q_insert, db_con_0))
	t_insert_0.setDaemon (True)
	t_insert_0.start ()

	t_insert_1 = Thread (target = insert, args = (q_insert, db_con_1))
	t_insert_1.setDaemon (True)
	t_insert_1.start ()

	t_insert_2 = Thread (target = insert, args = (q_insert, db_con_2))
	t_insert_2.setDaemon (True)
	t_insert_2.start ()

	t_insert_3 = Thread (target = insert, args = (q_insert, db_con_3))
	t_insert_3.setDaemon (True)
	t_insert_3.start ()

	t_insert_4 = Thread (target = insert, args = (q_insert, db_con_4))
	t_insert_4.setDaemon (True)
	t_insert_4.start ()

	t_insert_5 = Thread (target = insert, args = (q_insert, db_con_5))
	t_insert_5.setDaemon (True)
	t_insert_5.start ()


	# Parse the index
	# Foreach table rows (<tr>) in the index
	for row in soup.find_all ("tr"):

		# Get the found hashes for the corresponding leak
		if row.td is not None:
			q_download.put (row.td.string)

	# While a least one of the queues ain't empty, wait
	while q_download.qsize () > 0 or q_extract.qsize () > 0 or q_insert.qsize () > 0:
		time.sleep (4)


	try:
		db_con_0.commit ()
		db_con_0.close ()
		print ("0 Done")

	except MySQLdb.Error as error:
		print (error)

	try:
		db_con_1.commit ()
		db_con_1.close ()
		print ("1 Done")

	except MySQLdb.Error as error:
		print (error)

	try:
		db_con_2.commit ()
		db_con_2.close ()
		print ("2 Done")

	except MySQLdb.Error as error:
		print (error)

	try:
		db_con_3.commit ()
		db_con_3.close ()
		print ("3 Done")

	except MySQLdb.Error as error:
		print (error)

	try:
		db_con_4.commit ()
		db_con_4.close ()
		print ("4 Done")

	except MySQLdb.Error as error:
		print (error)

	try:
		db_con_5.commit ()
		db_con_5.close ()
		print ("5 Done")

	except MySQLdb.Error as error:
		print (error)


if __name__ == '__main__':

	try:
		main (sys.argv)

	except KeyboardInterrupt:
		print ("[!]\tCaught a SIGINT, exiting...")
		sys.exit (0)
