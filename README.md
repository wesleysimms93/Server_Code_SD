# README

## Project Overview
This project is a web application designed to house the following services:
- **Login**
- **Logout**
- **Task Autometer**
- **Manual Control**
- **Photo Repository**

The application is built on **Raspberry Pi 5** using the **Django** framework. Leveraging Django ensures compatibility with Python and provides useful libraries for security and functionality, such as an admin panel, login/logout capabilities, and HTTPS request handling. The project uses Python's `source` command to restrict library access to the local directory, enhancing system security.

---

## Pages and Services

### 1. Login
The login page ensures secure access and user confidentiality while maintaining a seamless user experience.
- **Access Prevention**: Prevent unauthorized access to the website and log usage for security and research.
- **Hidden Check**: All login information remains confidential to avoid credential theft.
- **Perpetual Login**: Sessions persist across pages to avoid frustration but time out with user inactivity to prevent misuse.

---

### 2. Logout
The logout page removes user access and completes the session securely.
- **Access Restriction**: Redirects users back to the login page upon logout.
- **Website Cookie Removal**: Deletes session cookies to prevent potential attacks and records final user activity data.

---

### 3. Manual Control
This page provides real-time control over system functionalities.
- **Mechanical Control**: Offers a defined interface for system tasks, capturing feedback and task outcomes.
- **Interface with External Software**: Communicates with the main system thread, preventing bottlenecks and conflicts during multiple user interactions.

---

### 4. Task Autometer
A user-friendly automation page enabling configurable and autonomous task execution.
- **Mechanical Control**: Provides task interfaces similar to the manual control page.
- **Interface with External Software**: Ensures stable interactions with the main system thread.
- **Set Up Tasks**: Enables "set it and forget it" automation, configurable for different plant types, locations, and needs.

---

### 5. Photo Repository
A repository for storing and managing photos captured by the system.
- **Database Pathing**: Saves photos in user-designated directories with customizable options (e.g., by date, x-y axis positions).
- **Exporting to the Cloud**: Allows secure and efficient uploads to external servers.
- **Local Download**: Enables photo downloads for review and post-processing, supporting all photo types.

---

## Technical Notes
- **Framework**: Django
- **Platform**: Raspberry Pi 5
- **Key Features**: Optimizations include a fully functioning admin panel, HTTPS request handling, and robust login/logout functionalities.
- **Security**: The use of Python's `source` command ensures restricted access to libraries, mitigating external risks.
