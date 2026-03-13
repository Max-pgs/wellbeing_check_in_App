# Testing Notes
The test is mainly focused on the backend functionality, as the front-end user interface is still under development.


## 1. Authentication
### Test:Register
**Expected result**
The user account was successfully created and redirected to the login page.

**Actual result**
The account with username "12345" was successfully created, and after completing the registration, it automatically redirected to the login page successfully.

**Result**
Pass

**Evidence**
![Register page](testing_image/register_page.png)
![Redirect to login](testing_image/register_success.png)


### Test:Login
**Expected result**
Users who have registered previously can log in and access the check-in page.

**Actual result**
Successfully logged in and can access the check-in page

**Result**
Pass

**Evidence**
![Login success page](testing_image/login_success.png)


### Test:Logout
**Excepted result**
The user has successfully logged out and if user wish to access the check-in (i.e., the protected page), the user need to log in again.

**Actual result**
Successfully logged out and returned to the login page. Click "check-in" to enter, as login is required for access.

**Result**
Pass

**Evidence**
![Logout success page](testing_image/logout_success.png)


## 2. Route protection
### Test:Access protected page without login
**Excepted result**
The system should redirect the user to the login page.

**Actual result**
The system redirected to `/accounts/login/`.

**Result**
Pass

**Evidence**
![Route protection](testing_image/route_protection.png)


## 3. Check-in CRUD operations
### Test:create check-in
**Excepted result**
A new check-in record should be created and added to the list.

**Actual result**
The check-in record was successfully created and displayed in the list.

**Result**
Pass

**Evidence**
![Create checkin](testing_image/checkin_create.png)


### Test:Edit check-in
**Excepted result**
The updated check-in value should have been successfully saved. After logging in again, it will be able to see.

**Actual result**
The check-in was successfully updated. On the "process" page, can see the created check-in.

**Result**
Pass

**Evidence**
![Edit checkin](testing_image/checkin_edit.png)
![Edit checkin](testing_image/checkin_process.png)


### Test:Delete check-in
**Excepted result**
The check-in value should be removed from the list.

**Actual result**
The check-in value was successfully deleted.

**Result**
Pass
**Evidence**



## 4. Ownership protection
### Test:User cannot edit another user's data
**Excepted result**
User 12345 logged in and created a sign-in record. User 12345 logged out, then User 123 logged in. User 123 attempted to access the sign-in editing page of User 12345. User 123 should not be able to edit the data of User 12345.

**Actual result**
The access of user 123 has been denied, and the record of user 12345 cannot be modified.

**Result**
Pass

**Evidence**
![Ownership protection](testing_image/ownership_test.png)


## 5. API endpoint testing
### Test:API check-ins endpoint
**Excepted result**
The endpoint should return JSON data containing the user's check-in records.

**Actual result**
The endpoint returned valid JSON containing the check-in records.

**Result**
Pass

**Evidence**
![API checkins](testing_image/api_checkins.png)


### Test:API progress endpoint
**Excepted result**
The endpoint should return aggregated progress data includ count and averages.

**Actual result**
The endpoint returned JSON data with count and averages field.

**Result**
Pass

**Evidence**
![API progress](testing_image/api_progress.png)


### Test:API Requires Authentication
**Excepted result**
The API should not allow access without authentication and should redirect to the login page.

**Actual result**
The system redirected to the login page when accessing the API endpoint without login in.

**Result**
Pass

**Evidence**
![API requires login](testing_image/api_requires_login.png)


## 6. Validation Testing
### Test:Registration validation
**Excepted result**
The system should prevent submission and show validation error.

**Actual result**
The form display validation errors and the account was not created.

**Result**
Pass

**Evidence**
![Register validation](testing_image/register_validation1.png)
![Register validation](testing_image/register_validation2.png)


### Test:Check-in form validation
**Excepted result**
The system should display validation errors

**Actual result**
The system prevented the invalid submission operation and displayed an error message.

**Result**
Pass

**Evidence**
![Checkin validation](testing_image/checkin_validation1.png)
![Checkin validation](testing_image/checkin_validation2.png)


