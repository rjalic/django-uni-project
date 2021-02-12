def enough_ects_available(student, subject, selected_semester):
  """
  Checks if the student has enough ects available in the selected semester.
  """
  enrollments = student.enrollment_set.all()
  ects_earned = subject.ects

  for enrollment in enrollments:
    if student.status == 'FULL_TIME' and enrollment.subject.semester_full_time == selected_semester:
      ects_earned += enrollment.subject.ects
    elif student.status == 'PART_TIME' and enrollment.subject.semester_part_time == selected_semester:
      ects_earned += enrollment.subject.ects

  if ects_earned > 30:
    return False

  return True

def previous_semester_criteria(student, subject, selected_semester):
  """
  Checks if the student successfully passed the subjects in the previous semester.
  """
  enrollments = student.enrollment_set.all()

  if selected_semester > 2:
    ceiling = selected_semester % 2 == 1 and selected_semester or selected_semester - 1
    for i in range(1, ceiling):
      target = student.status == 'FULL_TIME' and 15 or 6
      ects_earned = 0
      for enrollment in enrollments:
        if student.status == 'FULL_TIME' and enrollment.subject.semester_full_time == i and enrollment.status == 'passed':
          ects_earned += enrollment.subject.ects
        elif student.status == 'PART_TIME' and enrollment.subject.semester_part_time == i and enrollment.status == 'passed':
          ects_earned += enrollment.subject.ects
      if ects_earned < target:
        return False
  return True