(defun gps-line ()
  "Prints the current line of the cursor in the buffer out of the total lines in the buffer"
  (interactive)
  (let ( (start (point-min))
	 (n (line-number-at-pos))
	 (counter (how-many "\n" (point-min))) )
    (if (= start 1)
	(message "Line %d/%d" n counter)
      (save-excursion
	(save-restriction
	  (widen)
	  (message "line %d/%d (narrowed line %d"
		   (+ n (line-number-at-pos start) -1) counter n))))))
