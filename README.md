# gitlab-time-tracker

This is a quick python script that calculates all users time spent on project.

Gitlab API does not provide an easy way to see how much time a user has contributed to an **issue with multiple contributors**.
  
  
This information can be gathered from gitlab [notes](https://docs.gitlab.com/ee/api/notes.html) though - the ones under issues that look like `added 2d 4h 20m of time spent`
  
This code looks through given project and based on issue notes calculates the total time each user has spent on project. Prints out the amount of time each user has spent and also each issue the user has spent time on.
  
This code does not take into account time spent on merge requests etc. but it should be relatively easy to add this functionality.