---
name: Student-Project-Feedback
about: Report issues or give feedback on a student project in this repository.
title: Project Feedback
labels: ["feedback", "student-project"]
assignees: Emilio-Vasquez

body:
  - type: markdown
    attributes:
      value: |
        ## Thank you for helping improve our student project archive!
        Please fill in the details below. This will help us keep the repository high-quality and consistent.

  - type: input
    id: semester
    attributes:
      label: Semester
      description: Which semester is this project from? (e.g., Spring2025)
      placeholder: e.g., Spring2025
    validations:
      required: true

  - type: input
    id: group
    attributes:
      label: Group or Student Name
      description: Name of the group or student this feedback is about.
      placeholder: e.g., Group 3 - Camila Escobar
    validations:
      required: true

  - type: input
    id: project
    attributes:
      label: Project Folder Name
      description: Provide the folder or project name you are reporting about.
      placeholder: e.g., CST-Project
    validations:
      required: true

  - type: textarea
    id: feedback
    attributes:
      label: Feedback or Issue
      description: Describe the problem, suggestion, or improvement in detail.
      placeholder: Describe the issue here...
    validations:
      required: true

  - type: dropdown
    id: urgency
    attributes:
      label: Urgency
      description: How urgent is this feedback?
      options:
        - Low
        - Medium
        - High
    validations:
      required: false

---