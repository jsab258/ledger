# Small tools of the story measure

- extract_reply.py: saves a helper's reply from the session's own transcript folder into a file (helpers cannot write files in this cloud session). Arguments: the helper's id, the output file, a header line, and a marker the reply must contain.
- score_marks.py: adds up the MARKS lines of review files with the ruler's points.

Both only work inside the session that ran the helpers; they are kept so a later run can copy the method.
