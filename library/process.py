# Zane Rossi
# June 2018
# library project debugging

#######################################
import json

#######################################

error_mode = True

if error_mode == True:
	isbn_f    = open("bad_isbn.txt", "r")
	isbn_data  = isbn_f.read().split()
else:
	isbn_f    = open("isbn_data_proper.txt", "r")
	isbn_data  = isbn_f.read().split()

data_f    = open("ex_data_proper.txt", "r")
raw_json  = data_f.read()

data_f.close()
isbn_f.close()

json_data_full     = json.loads(raw_json)
json_data_scrubbed = []
fields             = ["title", "authors", "publishedDate", "description", "industryIdentifiers", "pageCount", "categories"]

print "\ntotal books: %s\n"%(len(json_data_full))
book_count = 0

# bad_isbn_f = open("bad_isbn.txt", "w")

for i in range(len(json_data_full)):

	json_data    = json_data_full[i]
	current_isbn = isbn_data[i]
	scrub_data   = {}

	# populate from information in volume_info
	# change such that default is storing null, not failure
	# though indicate that a failure has occured
	try:
		volume = json_data["items"][0]["volumeInfo"]
	except KeyError:
		print "The key you were looking for wasn't found for isbn: %s"%(current_isbn)
		# bad_isbn_f.write(str(current_isbn) + "\n")
		volume = None

	# only add books to registry that are found to have volume info
	if not volume == None:
		total_info = True
		for elem in fields:
			try:
				if elem == "authors":
					# takes only the first author
					scrub_data[elem] = volume[elem][0]
				elif elem == "industryIdentifiers":
					# take care of ISBNs (comes in tuple)
					scrub_data[elem] = volume[elem]

				else:
					scrub_data[elem] = volume[elem]
			except KeyError:
				print "\tNo field found: %s. for isbn %s"%(elem, str(current_isbn))
				# bad_isbn_f.write(str(current_isbn) + "\n")
				# if not everything is valid, abort
				scrub_data[elem] = ""

				total_info = True

		if total_info:
			json_data_scrubbed.append(scrub_data)
			book_count = book_count + 1
		else:
			continue
	else:
		continue

# sort according to last name
# json_data_scrubbed = sorted(json_data_scrubbed,key=lambda elem: elem["authors"].split()[-1][0])

for elem in json_data_scrubbed:
	print "----------------------------------------"
	for field in fields:
		if field == "title" or field == "authors":
			print "%s : %s"%(field, elem[field])
		else:
			continue

print "\nsuccessful books: %s\n"%(book_count)

# turn back into a nice json
json_return = json.dumps(json_data_scrubbed, indent=4)
return_f    = open("scrubbed_data_proper.json", "w")
return_f.write(json_return)
return_f.close()
# bad_isbn_f.close()
