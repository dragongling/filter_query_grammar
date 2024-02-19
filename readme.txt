Filters:
	Operators
		not
		or
		and
	By data type:
		Common:
			eq =
			in [list]
		String/CharField:
			starts with
			ends with
			contains
		Numeric
			lt <
			lte <=
			gt >
			gte >=
		Date
			lt <
			lte <=
			gt >
			gte >=
		List:
			any([list]) [] in


Terms:
	string
	number
	date
Operators:
	=
	>
	<
	>=
	<=
	in
	|
	&
	~
Parentheses


/me/assigned
	(assignee = my_id or assistants.any(my_id) or position = my_position_id) and not status = completed
	filters=(assignee=1|[1] in assistants|position=1)&~status=3 & sort=date_created & view=table[title,slug,date_created,status,deadline,priority,assignee,position,initiator,spectators,tags]
/me/created
	initiator = my_id
/me/spectator
	my_id in spectators
/me/subordinates
	assignee in my_subs_ids or assistants.any(my_subs_ids) or position = sub_positions
	assignee in [2,3,4] | [2,3,4] in assistants | position=2
/planning/kanban
	(assignee = my_id or my_id in assistants or position = my_position_id) and not (status = completed and create_date <= (current - 30 days))

	(assignee=1|1 in assistants|position=1)&~(status=3&create_date<=2024-01-16)


query string -> AST -> AST with field types -> django db query


assignee=1|[1] in assistants|position=1)&~status=3



/me/assigned
	logical:
		(assignee = my_id or assistants.any(my_id) or position = my_position_id) and not status = completed
	frontend query:
		(assignee=1|[1] in assistants|position=1)&~status=3
	backend query:
		arg1 = 1
		arg2 = [1]
		arg3 = 1
		arg4 = 3

		filter = (Q(assignee=arg1) | Q(assistants__in=arg2) | Q(position=arg3)) & ~Q(status=arg4)


/simpletask/kanban
	hide task with status = completed and date < (current - 30 days)

/me/assigned
	task with position =