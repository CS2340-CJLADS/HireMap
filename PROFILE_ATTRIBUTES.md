# Profile Page Attributes Reference

## Currently Displayed Attributes

### Applicant Basic Information
- **first_name** (CharField, max_length=30) - Currently displayed
- **last_name** (CharField, max_length=30) - Currently displayed
- **user.username** (from User model) - Displayed as "Email" - Currently displayed
- **phone** (CharField, max_length=20, nullable) - Currently displayed
- **location** (CharField, max_length=100, nullable) - Legacy field - Currently displayed

### Professional Information
- **skills** (TextField, nullable) - Currently displayed
- **education** (TextField, nullable) - Currently displayed
- **experience** (TextField, nullable) - Currently displayed
- **availability** (CharField with choices) - Currently displayed as "Job Search Status"
  - Choices: 'available' (Available Now), 'open-to-work' (Open to Work), 'not-looking' (Not Looking)

### Projects Section
- **projects** (Related Project objects) - Currently displayed
  - Each project has:
    - **title** (CharField, max_length=200)
    - **description** (TextField)
    - **technologies** (CharField, max_length=500, nullable)
    - **url** (URLField, nullable)
    - **created_at** (DateTimeField, auto_now_add)

---

## Available But NOT Currently Displayed

### Address Fields (Detailed Location)
- **street_address** (CharField, max_length=200, nullable)
- **post_code** (CharField, max_length=20, nullable) - ZIP/Postal code
- **city** (CharField, max_length=100, nullable)
- **state** (CharField, max_length=100, nullable)
- **country** (CharField, max_length=100, default='USA')

### Additional Information
- **links** (TextField, nullable) - External links (portfolio, LinkedIn, etc.)
- **user.email** (from User model) - Separate email field (may differ from username)

---

## Data Structure Summary

### Applicant Model Fields
```python
# Basic Info
- first_name
- last_name
- phone
- location (legacy)

# Professional
- skills
- education
- experience
- links
- availability

# Address (Detailed)
- street_address
- post_code
- city
- state
- country

# Relations
- user (OneToOne to User)
- project_set (reverse ForeignKey to Project)
```

### User Model Fields (via applicant.user)
```python
- username (used as email in current display)
- email (separate field, not currently displayed)
- first_name (Django default, separate from Applicant.first_name)
- last_name (Django default, separate from Applicant.last_name)
```

### Project Model Fields
```python
- title
- description
- technologies
- url
- created_at
- applicant (ForeignKey)
```

---

## Template Context Variables

From `seeker/views.py` profile view:
```python
template_data = {
    'title': 'My Profile',
    'applicant': applicant,  # Full Applicant object
    'projects': projects,     # QuerySet of Project objects
}
```

---

## Notes for Design

1. **Location Fields**: There are two location systems:
   - Legacy: `location` (single string field)
   - New: `street_address`, `post_code`, `city`, `state`, `country` (structured address)

2. **Name Fields**: Both User and Applicant have first_name/last_name. Currently only Applicant fields are displayed.

3. **Email**: Currently shows `user.username` as email. `user.email` is also available.

4. **Links Field**: Available but not displayed - could be used for portfolio, LinkedIn, GitHub, etc.

5. **Availability**: Has three states with display labels via `get_availability_display()` method.

6. **Projects**: Displayed in a grid with cards showing title, description, technologies, URL, and creation date.

