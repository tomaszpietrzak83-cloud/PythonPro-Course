# Lesson24 Task Map

This file lists the places where `TASK` markers were added to make review easier.

Templates use Django template comments in the form `{# TASK ... #}`.

## Tagged locations

- `my_project/my_project/settings.py`
  - `# TASK 01` above `LOGOUT_REDIRECT_URL`
  - `# TASK 01` above `LOGIN_REDIRECT_URL`
  - `# TASK 01` above `LOGIN_URL`
- `my_project/my_project/urls.py`
  - `# TASK 02 03 05 06 10` above the `my_app.urls` include
  - `# TASK 07` above the login route
  - `# TASK 02` above the logout route
  - `# TASK 08` above password-change routes
- `my_project/my_app/urls.py`
  - `# TASK 05` above the home route
  - `# TASK 06 09` above the register route
  - `# TASK 03` above the profile route
  - `# TASK 10` above the user-list route
- `my_project/my_app/forms.py`
  - `# TASK 06` above `RegistryForm`
  - `# TASK 06` above the required email field
  - `# TASK 06` above the form fields tuple
  - `# TASK 06` above the custom `save` method
- `my_project/my_app/views.py`
  - `# TASK 07` above `CustomLoginView`
  - `# TASK 02` above `CustomLogoutView`
  - `# TASK 05` above the protected home view
  - `# TASK 06 09` above the register view
  - `# TASK 06` above `RegistryForm` usage
  - `# TASK 09` above automatic login after registration
  - `# TASK 04` above the registration success message
  - `# TASK 03` above the protected profile view
  - `# TASK 10` above the staff-only user-list view
- `my_project/my_app/templates/base.html`
  - `{# TASK 04 #}` above the messages loop
  - `{# TASK 02 #}` above the authenticated/anonymous navigation branch
  - `{# TASK 08 #}` above the password-change navigation link
- `my_project/my_app/templates/users/profile.html`
  - `{# TASK 03 #}` above the profile content
- `my_project/my_app/templates/users/register.html`
  - `{# TASK 06 #}` above the registration form
- `my_project/my_app/templates/users/password_change_form.html`
  - `{# TASK 08 #}` above the password-change form
- `my_project/my_app/templates/users/password_change_done.html`
  - `{# TASK 08 #}` above the password-change confirmation
- `my_project/my_app/templates/users/user_list.html`
  - `{# TASK 10 #}` above the user list

## Notes

- Task 07 is represented by the custom login view and login URL. Django's `LoginView` already handles the `next` redirect behavior when the `next` query parameter is present.
- Task 10 requires a staff user to view the user list, or just delete decorator.
