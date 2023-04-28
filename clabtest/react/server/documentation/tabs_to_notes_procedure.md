1. get all file contents
2. now you have a list of lines
	[
		"e|-0-1-2-3",
		"B|-0-1-2-3",
		"G|-0-1-2-3",
		"D|-0-1-2-3",
		"A|-0-1-2-3",
		"E|-0-1-2-3",
	]
3. split these by the | character -- this will give you the open notes on the left side and the fretting positions on the right side (`separate_open_notes_from_fret_positions()` method)
4. now you have a list of lists
	[
		["e", "-0-1-2-3"],
		["B", "-0-1-2-3"],
		["G", "-0-1-2-3"],
		["D", "-0-1-2-3"],
		["A", "-0-1-2-3"],
		["E", "-0-1-2-3"]
	]
5. to put the proper contents into the tab dictionary, iterate through the list above (use `get_unprocessed_tab_dictionary()` method)

6. your dictionary will look like this
{
	'e': '---------------\n', 
	'B': '---------------\n', 
	'G': '---------------\n', 
	'D': '---------------\n', 
	'A': '---------------\n', 
	'E': '-0-3-5-6-5-0-0-\n'
}

7. use a representation to determine where that note falls in the sequence to be played
