# coding=utf-8
#
# Copied from small_program folder, containing the match() function to
# match items in two lists.

from ft_converter.utility import logger



class MatchedItemNotFound(Exception):
	pass



def match(list_a, list_b, matching_function):
	"""
	Match items in list_a to items in list_b. If all items in list_a find a 
	matched item in list_b, then a list of tuples are returned, as:

	(item_a1, item_b1), (item_a2, item_b2), ... (item_aN, item_bN)

	where item_a1 and item_b1 are matched items, etc. Two items in list_a
	cannot match to the same item in list_b.

	matching_function is a user supplied function to determine whether
	an item from list_a is matched to another item in list_b.

	If any item in list_a doesn't find a matched item in list_b, then 
	an exception is thrown.
	"""
	matched_position = []
	for i in range(len(list_a)):
		if i < len(matched_position):
			continue

		matched = False
		for j in range(len(list_b)):
			if not j in matched_position and matching_function(list_a[i], list_b[j]):
				matched_position.append(j)
				matched = True
				break

		if not matched:
			logger.error('item {0} in list_a: {1} does not find a matched item in list_b'.
						format(i, list_a[i]))
			raise MatchedItemNotFound()

	# print(matched_position)
	return create_matched_list(list_a, list_b, matched_position)



def match_repeat(list_a, list_b, matching_function):
	"""
	Match items in list_a to items in list_b. If all items in list_a find a 
	matched item in list_b, then a list of tuples are returned, as:

	(item_a1, item_b1), (item_a2, item_b2), ... (item_aN, item_bN)

	The difference between this function and the match() function is that
	an item in list_b can be matched repeatedly, i.e., two items in list_a
	can match to the same item in list_b.

	For those items in list_a that don't find a matched item in list_b, they
	are returned as a separate list.
	"""
	matched_position = []
	unmatched_position = []
	for i in range(len(list_a)):
		if i < len(matched_position):
			continue

		matched = False
		for j in range(len(list_b)):
			if matching_function(list_a[i], list_b[j]):
				matched_position.append(j)
				matched = True
				break

		if not matched:
			logger.error('item {0} in list_a: {1} does not find a matched item in list_b'.
						format(i, list_a[i]))
			unmatched_position.append(i)

	# print(matched_position)
	return create_matched_list(list_a, list_b, matched_position, unmatched_position), \
			[list_a[i] for i in unmatched_position]



def create_matched_list(list_a, list_b, matched_position, unmatched_position=[]):
	"""
	create a list of tuples for matches items in list_a and list_b.

	matched_position: positions in list_b that matched to list_a
	unmatched_position: positions in list_a that does not match to any item
						in list_b
	"""
	matched_list = []
	j = 0
	for i in range(len(list_a)):
		if i in unmatched_position:
			continue

		matched_list.append((list_a[i], list_b[matched_position[j]]))
		j = j + 1

	return matched_list

