# CS50 Web - Capstone Project - School Web App

# Overview (Write-Up) #

This project is a school-based web application that allows users to register either as a **teacher** or **student** by clicking the **Register** link in the navigation bar of the index page (`http://127.0.0.1:8000/`) or by accessing it directly through `http://127.0.0.1:8000/register`.

If a user registers successfully, they will be automatically logged in (with the navigation bar updated accordingly using django template conditions for `user.is_authenticated`) and redirected to their home page (`http://127.0.0.1:8000/home`) where they can see courses they manage (if user is a teacher) or courses they are enrolled in (if user is a student).

On the other hand, unsuccesful registrants will be presented with helpful error messages.

### Teachers

**Teachers** who are logged in are able to **create**/**manage**/**delete** courses. They may also **add**/**edit** grades for students who enroll in their courses.

Teachers may create a course by clicking the **Add Course** button in their own home page, entering the course title and course code, and submitting the form. If the addition is successful, they will then be redirected to their home page with the new course added, otherwise they will be presented with help messages.

By clicking the course on their home page (or any page that lists courses), teachers will be taken to the **course's detail page** which includes **two tables** for enrolled students (if the authenticated teacher created the course): one for *graded students* and another for *ungraded students*. This page also includes an option to **delete** the course (only available to the teacher who created the course).

If there is/are enrolled student(s) in the course, the teacher is able to add grades by clicking the **Submit Grades** button which then triggers the event listener in the javascript file `course_detail_teacher.js` in order to change the empty grade fields into input fields where the teacher can enter the grades, and to make the submit button visible. If the grade inputs are valid, the page is updated accordingly to display the inputted grades and the graded students placed from the ungraded students table to the graded students table.

Teachers also have the option to edit the grades for graded students (if any) by clicking **Edit Grades** which uses a similar implementation as for submitting grades, the only difference is that the input boxes for the grades are pre-populated with their original grade(s).

### Students

On the other hand, **Students** who are logged in are able to **enroll**/**unenroll** from classes and **view their grade** in classes they are enrolled in.

Students who log in will be taken to their home page (similar to teachers) where they can see courses they are enrolled in. Students may then add a course by clicking **Add Course** button which takes them to a page that lists all available courses and includes a search feature which allows students to be able to query for a course's title or code. Clicking on any of the listed courses takes them to the course's detail page where they can toggle their enrollment status by clicking the **Enroll** button (if not yet enrolled) or **Unenroll** button (if already enrolled). 

The enroll/unenroll buttons are dynamically displayed using django template conditions depending on the user's enrollment status. Clicking this button triggers an event listener in the javascript file `course_detail_student.js` which sends a `PUT` request to a function view named `course_student_api` in the Django app `school` in order to reflect this change in the database by adding or removing the student from the course's list of students and creating or deleting the student's gradebook, respectively.

If a student is enrolled, they will be able to see their grades provided that the course teacher has graded them already, otherwise their grade for that course will be marked as **Ungraded**.

### Others

Additionally, anyone (even unauthenticated users) may be able to look up courses using a **search feature**, but only users who are logged in can see the course in detail and perform **special actions** (as those stated above for teachers and students).

Finally, when a user logs out, they are redirected to the login page (`http://127.0.0.1:8000/login`).

More details about these pages can be found in the sections below.

# Distinctiveness and Complexity #

1. This project is relatively **distinct** because **there is no school-based web app project for the course**.

    - Project 0 - Search

    - Project 1 - Wiki

    - Project 2 - (E-)Commerce

    - Project 3 - (E-)Mail

    - Project 4 - (Social) Network

    - **Capstone** - **School-Based Web Application**

2. This project is relatively **complex** because:

    - It uses a **combination of the concepts** used throughout the course (but no testing yet though, sorry).
    
    - It makes use of some tools beyond the scope of the course like **Django's Class-Based Views and Mix-ins**, and **integrating `django-env`** to be able to use **environment variables** (also, Bootstrap Modals which are pretty cool).

        - using class-based views for the visible web pages.

        - using function-based views for the API.

        - environment variables allow the user to dynamically input their secret key (preventing it from getting exposed in commits), and some other additional options (e.g. debug, database url, etc.).
    
    - It also implements some **basic error-handling** which were not required in previous projects (such as input error-handling for user registration) and **restricting access** on views and functions when necessary (e.g. restricting functionalities which are exclusive to certain user roles or model instance owners) by using Django's powerful decorator functions and mix-ins.


# Files (What’s contained in each file) #

1. **HTML Templates**:

    - `layout.html`

        - the base of most templates and includes the navbar.

    - `register.html` and `login.html`

        - for the registration and login pages.

    - `course_add.html`
        
        - contains the form for adding courses as a teacher.

    - `course_list`... prefix
        
        - `course_list_base.html` for the index page.
        
        - `course_list_search.html` for the search results page.
        
        - `course_list_user.html` for the user's home page.

    - `course_detail.html`
        
        - for the course detail pages.

2. **Javascript Files**

    - `course_detail_student.js`
        
        - enables the single-page enroll/unenroll and updating of student count.

    - `course_detail_teacher.js`

        - enables the submission and editing of student grades.

    - `search.js`

        - disables search form submission when there search input is empty or only spaces.

3. Files in **Django App** named `school`.

    - `school/models.py`

        - contains the models for the **User**, **Course** and **Gradebook**.
    
    - `school/forms.py`

        - contains the forms for **user registration** and **adding courses**.
    
    - `school/urls.py`

        - contains the **valid url paths** for the project, each corresponding to a view in `school/views.py`.
    
    - `school/views.py`

        - each view has a **docstring** to explain what it does.

        - views are also associated in the following **Features** section below (of **THIS** `README.md`).


# Features #

1. **Index Page**:

    - uses class view `CourseListView` from `school/views.py`.

    - The index page is a page where **all courses** are listed.

    - Pages with lists of courses:
        
        - are in **reverse chronological order**.

        - have each course linking to the course's detail page.

        - are paginated by 7.

2. **Registration Page**:

    - uses class view `SignUpView` from `school/views.py`.
    
    - a user may be able to sign up as either: a **teacher** or a **student**.

    - some **error-handling** using Django form validation.

    - successful registration redirects users to their **home page**.

3. In a **User's Home Page**:

    - uses class view `User_CourseListView` from `school/views.py`.
        
    - **Teachers** will see a list of their **managed courses**.

    - **Students** will see a list of their **enrolled courses**.

4. **Course Detail Pages**:

    - uses class view `CourseDetailView` from `school/views.py`.

    - Are **only accessible** to users who are **logged in** (redirects to login page otherwise).

    - This shows the course's creation date, teacher, and number of students.

    - Additionally,
        
        - **Teachers** will see tables of their **graded** and **ungraded students** in alphabetical order.
        
        - **Students** who are enrolled will be able to see their **grade**.

5. A **Teacher**:

    - may **create a course**.

    - may **post/edit grades** for enrolled students (in courses they manage).

        - uses function view `course_teacher_api` from `school/views.py` as API.

    - may **delete a course** that they created.

        - uses function view `course_delete` from `school/views.py`.

        - warns the user to **confirm deletion** using a bootstrap modal (unless view is directly accessed through url).

6. A **Student**:

    - may **enroll** to or **unenroll** from a course.

        - uses function view `course_student_api` from `school/views.py` as API.

        - implemented as a single page feature which also updates the number of students using Javascript `fetch`.

        - confirms enrollment/unenrollment using a bootstrap modal.

    - may **view their grade** in a course they enrolled in.

7. **Search feature** to look up courses.

    - uses class view `Search_CourseListView` from `school/views.py`.

    - Using javascript, disable form submission when the search input is either empty or only spaces.

    - Otherwise, displays a list of courses with that match the query in either the course's code or title.

8. **Aesthetic and User Interface Improvements** using Bootstrap and CSS styling.

    - `bootstrap5` 

        - buttons, navbar, input, modals, etc.
        
        - enables application to be mobile-responsive

    - `crispy-forms` 

        - automatic form-styling and nice input-error helpers.


# How to Run the Application (Setting Up) #

1. Install requirements.txt using `pip install -r requirements.txt`

2. Please create a `.env` file in the **project's root directory** (same directory as `manage.py`) then copy & paste the following:

    ```
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///db.sqlite3
    ```

    - You may edit `SECRET_KEY` if desired.

    - (This is to allow `django-environ` to use environment variables).

3. **(Optional, commit already has migrations)** 

    - Make migrations to school: `python manage.py makemigrations school`

    - Migrate: `python manage.py migrate`

4. **(Optional)** Create a superuser: `python manage.py createsuperuser`

5. You may now run the server: `python manage.py runserver`

6. You may then **register** as a *teacher/student* or **sign-in** as the *superuser* (if you created one).


# Additional Info #

- Please **DO NOT SKIP** any of the **non-optional steps** (especially creating the `.env` file) in the *Setting Up* section above, otherwise the project may not work.