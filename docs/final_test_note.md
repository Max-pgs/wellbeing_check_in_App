# Testing Notes

Testing was carried out in two stages. The initial backend test was carried out during the period when the front end was still under development (during_design_testing_note), and then another round of test was conducted after the final improvements to the front end were completed. This document represents the final test, focusing on the final verification status of the application, including authentication, route protection, add, delete, modify and query operations, API behavior, validation, and backend unit tests.


## 1. Authentication
### Test: Register

**Expected Result**
A new user account should be created successfully and the system should redirect to the login page.

**Actual Result**
The account with username "12345" was successfully created, and after completing the registration, it automatically redirected to the login page successfully.

**Result**
Pass

**Evidence**
![Register page](testing_images/deploy_dev_images/register_page.png)
![Register success](testing_images/deploy_dev_images/register_success.png)



### Test: Login

**Expected Result**
The user should log in successfully and gain access to protected pages.

**Actual Result**
The user successfully logs in and is able to use it. Then they are redirected to the dashboard page.

**Result**
Pass

**Evidence**

![Login success](testing_images/deploy_dev_images/login_success.png)



### Test: Logout

**Expected Result**
The user should be logged out and protected pages should require authentication again.

**Actual Result**
The user was logged out successfully and protected pages redirected to the login page.

**Result**
Pass

**Evidence**
![Logout success](testing_images/deploy_dev_images/logout_success.png)



## 2. Route Protection
### Test: Protected Check-ins Page Requires Login

**Expected Result**
The system should prevent unauthenticated access and redirect the user to the login page.

**Actual Result**
This system prevents unauthorized access and automatically redirects to the login page.

**Result**
Pass

**Evidence**
![Route protection](testing_images/deploy_dev_images/route_protection.png)



### Test: API Requires Authentication

**Expected Result**
The API should not be accessible without authentication.

**Actual Result**
When the user attempts to access the API endpoint, they are automatically redirected to the login page.

**Result**
Pass

**Evidence**
![API requires login](testing_images/deploy_dev_images/api_requires_login.png)



## 3. Check-in CRUD Operations
### Test: Create Check-in

**Expected Result**
A new check-in should be created and displayed in the system.

**Actual Result**
The check-in was created successfully and displayed in the check-in history page.

**Result**
Pass

**Evidence**
![Create check-in](testing_images/deploy_dev_images/checkin_create.png)
![Check-in History](testing_images/deploy_dev_images/checkin_history.png)



### Test: Edit Check-in

**Expected Result**
The check-in should be updated successfully.

**Actual Result**
The check-in was updated successfully and the revised values were displayed.

**Result**
Pass

**Evidence**
![Edit check-in](testing_images/deploy_dev_images/checkin_edit.png)



### Test: Delete Check-in

**Expected Result**
The check-in should be removed from the list/history page.

**Actual Result**
The check-in was deleted successfully and can't see in the history page.

**Result**
Pass

**Evidence**
![Delete check-in](testing_images/deploy_dev_images/checkin_delete.png)



## 4. Ownership Protection
### Test: User Cannot Edit Another User’s Check-in

**Expected Result**
User 123 should not be able to access or modify User 12345’s check-in entry.

**Actual Result**
Access was denied and the record could not be modified by another user.

**Result**
Pass

**Evidence**
![Ownership protection](testing_images/deploy_dev_images/ownership_test.png)



## 5. API Endpoint Testing
### Test: API Check-ins Endpoint

**Expected Result**
The endpoint should return JSON data containing the current user’s check-in records.

**Actual Result**
The endpoint returned valid JSON containing the check-in records of the logged-in user.

**Result**
Pass

**Evidence**
![API check-ins](testing_images/deploy_dev_images/api_checkins.png)



### Test: API Progress Endpoint

**Expected Result**
The endpoint should return aggregated progress data, including count and average values.

**Actual Result**
The endpoint returned valid JSON data with progress statistics.

**Result**
Pass

**Evidence**
![API progress](testing_images/deploy_dev_images/api_progress.png)



### Test: API Progress with Invalid Date Input

**Expected Result**
The endpoint should safely handle invalid input and redirect or reject the request according to the implemented backend logic.

**Actual Result**
This endpoint was redirected in the manner specified by the final version of the backend, and no invalid data was exposed.

**Result**
Pass

**Evidence**
Backend behaviour confirmed through unit testing.



## 6. Validation Testing
### Test: Registration Validation

**Expected Result**
Passwords that are too weak will result in the failure of account creation and an error message will be displayed.

**Actual Result**
The form displayed validation errors and the account was not created.

**Result**
Pass

**Evidence**
![Register validation](testing_images/deploy_dev_images/register_validation.png)



### Test: Check-in Validation

**Expected Result**
The system should reject invalid input and display form validation errors.

**Actual Result**
The system prevent invalid submission operations and display the corresponding verification feedback information.

**Result**
Pass

**Evidence**
![Check-in validation](testing_images/deploy_dev_images/checkin_validation.png)



### Test: Goal Validation

**Expected Result**
The system should reject the form and display an error message.

**Actual Result**
The form displayed a validation error and the goal was not created.

**Result**
Pass

**Evidence**
![Goal validation](testing_images/deploy_dev_images/goal_validation.png)



## 7. Goal CRUD Operations
### Test: Create Goal

**Expected Result**
A new goal should be created and displayed in the goal list.

**Actual Result**
The goal was successfully created and displayed in the goal list.

**Result**
Pass

**Evidence**
![Goal create](testing_images/deploy_dev_images/goal_create.png)



### Test: Edit Goal

**Expected Result**
The goal should be updated successfully.

**Actual Result**
The goal was updated successfully and the new values were displayed.

**Result**
Pass

**Evidence**
![Goal edit](testing_images/deploy_dev_images/goal_edit.png)



### Test: Delete Goal

**Expected Result**
The goal should be removed from the goal list.

**Actual Result**
The goal was successfully deleted and no longer appeared in the goal list.

**Result**
Pass

**Evidence**
![Goal delete](testing_images/deploy_dev_images/goal_delete.png)



## 8. Habit CRUD Operations
### Test: Create Habit

**Expected Result**
A new habit should be created and displayed in the habit list.

**Actual Result**
The habit was successfully created and displayed in the habit list.

**Result**
Pass

**Evidence**
![Habit create](testing_images/deploy_dev_images/habit_create.png)



### Test: Edit Habit

**Expected Result**
The habit should be updated successfully.

**Actual Result**
The habit was updated successfully and the revised values were displayed.

**Result**
Pass

**Evidence**
![Habit edit](testing_images/deploy_dev_images/habit_edit.png)



### Test: Delete Habit

**Expected Result**
The habit should be removed from the habit list.

**Actual Result**
The habit was successfully deleted and no longer appeared in the habit list.

**Result**
Pass

**Evidence**
![Habit delete](testing_images/deploy_dev_images/habit_delete.png)



## 9. Unit Test Execution

**Command**
python manage.py test checkins -v 2

**Expected Result**
All backend unit tests should execute successfully without failures.

**Actual Result**
The final backend test suite executed successfully, covering authentication, CRUD operations, ownership protection, validation, API behaviour, and basic frontend rendering checks.

**Result**
Pass

**Evidence**
![Unit tests execution](testing_images/deploy_dev_images/unit_tests_success.png)



## 10. Lighthouse / Sustainability Evidence

**Pages Tested**
- `/checkins/`
- `/checkins/progress/`

**Tool**
Chrome DevTools Lighthouse

**Expected Result**
Representative pages of the final application should show strong scores for performance, accessibility, best practices, and SEO.

**Actual Result**
The final frontend implementation achieved strong Lighthouse scores on representative pages, indicating good overall quality and usability.

**Result**
Pass

**Evidence**
![Lighthouse Check-ins](testing_images/deploy_dev_images/lighthouse_checkins.png)
![Lighthouse Progress](testing_images/deploy_dev_images/lighthouse_progress.png)