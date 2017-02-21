# hashes.org
hashes.org cracked passwords recovery tool.

Pretty simple stuff:
Main thread recover the index of downloadable archives containing cracked passwords.
Parse it, and recover archives ids. And put it in a queue.

A first thread poll this queue, craft download URL for each archive, and download it.
Then it puts the archive name (<id>.7z) in a second queue.

A second thread poll this queue, and extract the previously downloaded archives on the fly,
and insert all the password it contains in a third queue.

Lastly multiple threads poll this last queue and insert the passwords in a local MySQL database.

# TO DO
Dynamically generate the multiple insert threads and DB connection objects.
