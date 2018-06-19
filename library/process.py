# Zane Rossi
# June 2018
# library project debugging

#######################################
import json

#######################################

data_f    = open("ex_data.txt", "r")
raw_json  = data_f.read()
isbn_f    = open("isbn_data.txt", "r")
isbn_data  = isbn_f.read().split()

json_data_full     = json.loads(raw_json)
json_data_scrubbed = []
fields     = ["title", "authors", "publishedDate", "description","industryIdentifiers"]

data_f.close()
isbn_f.close()

for i in range(len(json_data_full)):

	json_data    = json_data_full[i]
	current_isbn = isbn_data[i]

	try:
		volume = json_data["items"][0]["volumeInfo"]
	except KeyError:
		print "The key you were looking for wasn't found for isbn: %s"%(current_isbn)
		volume = None

	# only add books to registry that are found to have volume info
	if not volume == None:
		scrub_data = {}
		total_info = True
		for elem in fields:
			try:
				if elem == "authors":
					# takes only the first author
					scrub_data[elem] = volume[elem][0]
				elif elem == "industryIdentifiers":
					# take care of ISBNs
					scrub_data[elem] = volume[elem]

				else:
					scrub_data[elem] = volume[elem]
			except KeyError:
				print "No field found: %s."%(elem)
				# if not everything is valid, abort
				total_info = False

		if total_info:
			json_data_scrubbed.append(scrub_data)
		else:
			continue
	else:
		continue

# sort according to last name
json_data_scrubbed = sorted(json_data_scrubbed,key=lambda elem: elem["authors"].split()[-1][0])

for elem in json_data_scrubbed:
	print "----------------------------------------"
	for field in fields:
		if field == "title" or field == "authors":
			print "%s : %s\n"%(field, elem[field])
		else:
			continue

# turn back into a nice json
json_return = json.dumps(json_data_scrubbed,indent=4)
return_f    = open("scrubbed_data.json", "w")
return_f.write(json_return)
return_f.close()
