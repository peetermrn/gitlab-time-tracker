import re
import requests

# YOUR INFO HERE
project_id = "28093"
access_token = "TOKEN"  # a private token with read_api access:
base_url = "https://gitlab.cs.ttu.ee/api/v4"

# headers and parameters
headers = {'Private-Token': access_token}
parameters = {'include_time_stats': True}

# urls and templates
issues_url_template = "{base_url}/projects/{project_id}/issues?per_page=200"
issue_notes_url = issues_url_template.format(base_url=base_url, project_id=project_id)
issue_notes_url_template = "{base_url}/projects/{project_id}/issues/{issue_iid}/notes?per_page=200"
line_template = "title: {title}    time: {time_s}    url: {url}"

# data dictionaries
issue_dict = {}
times_spent_dict = {}

# call API for all issues
issues = requests.get(issue_notes_url, headers=headers)

# loop through all issues in chronological order
for issue in issues.json()[::-1]:
    issue_notes_url = issue_notes_url_template.format(base_url=base_url, project_id=project_id, issue_iid=issue['iid'])
    # call API for all notes under issue
    issue_notes_response = requests.get(issue_notes_url, headers=headers, params=parameters)

    notes = issue_notes_response.json()

    # holds the amount of time each user has contributed to current issue
    issue_time = {}

    # holds all users who have contributed to current issue
    issue_usernames = set()

    # loop through all notes under issue in chronological order
    for note in notes[::-1]:

        note_body = note['body']
        username = note['author']['username']
        if re.search(r"added ((\d+mo)?\s*(\d+w)?\s*(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*)of time spent", note_body):
            note_added_time = 0

            time_months = re.search(r"\d+mo", note_body)
            time_weeks = re.search(r"\d+w", note_body)
            time_days = re.search(r"\d+d", note_body)
            time_hours = re.search(r"\d+h", note_body)
            time_minutes = re.search(r"\d+m", note_body)

            note_added_time += float(time_months.group()[:-2]) * 160 if time_months else 0
            note_added_time += float(time_weeks.group()[:-1]) * 40 if time_weeks else 0
            note_added_time += float(time_days.group()[:-1]) * 8 if time_days else 0
            note_added_time += float(time_hours.group()[:-1]) if time_hours else 0
            note_added_time += float(time_minutes.group()[:-1]) / 60 if time_minutes else 0

            times_spent_dict[username] = times_spent_dict.get(username, 0) + note_added_time
            issue_time[username] = issue_time.get(username, 0) + note_added_time
        if note_body == "removed time spent":
            for user in issue_time:
                times_spent_dict[username] = times_spent_dict.get(username, 0) - issue_time[username]
            issue_time = {}
        if username in issue_time:
            issue_usernames.add(username)

    for user in issue_usernames:
        if issue_time[user]:
            line = line_template.format(
                title=issue['title'],
                time_s=round(issue_time[user], 3),
                url=issue['web_url']
            )
            issue_dict.setdefault(user, []).append(line)

print("time in hours:")
print(times_spent_dict, "\n\n")

print("individual issues:")
[print(key, value, "\n") for key, value in issue_dict.items()]
