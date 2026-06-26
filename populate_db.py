import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stu_test.settings')
django.setup()

from quiz.models import CustomUser, Subject, Quiz, Question, Option, QuizAttempt, StudentAnswer


def populate():
    print("Clearing old data...")
    CustomUser.objects.filter(user_type='student', username__startswith='teststudent').delete()

    subjects_to_clear = [
        "Python Programming", "Object Oriented Programming", "Database Management Systems",
        "Data Structures", "UI/UX Design", "Cyber Security", "Artificial Intelligence",
        "Machine Learning", "Computer Networks", "Web Development", "AR/VR Technology",
        "Mathematics", "ICT"
    ]
    for s in subjects_to_clear:
        Subject.objects.filter(name=s).delete()

    print("Creating 5 students...")
    students = []
    for i in range(1, 6):
        student = CustomUser.objects.create_user(
            username=f'teststudent{i}',
            email=f'teststudent{i}@example.com',
            password='password123',
            user_type='student',
            enrollment_no=f'ENR202600{i}',
            attendance=random.choice([85, 90, 95, 100]),
            cgpa=round(random.uniform(7.0, 10.0), 2),
            review=random.randint(3, 5)
        )
        students.append(student)

    all_quizzes_data = [

        # ── PYTHON ──────────────────────────────────────────────────────────────
        {
            "subject": "Python Programming",
            "title": "Python Fundamentals Quiz",
            "description": "Test your core Python knowledge.",
            "time_limit_minutes": 20,
            "questions": [
                ("What is the output of print(2 ** 3)?", [("6", False), ("8", True), ("9", False), ("12", False)]),
                ("Which keyword defines a function in Python?", [("func", False), ("define", False), ("def", True), ("function", False)]),
                ("What data type is [1, 2, 3]?", [("Tuple", False), ("Set", False), ("Dictionary", False), ("List", True)]),
                ("How do you write a comment in Python?", [("// comment", False), ("/* comment */", False), ("# comment", True), ("-- comment", False)]),
                ("What is the conventional indentation in Python?", [("1 space", False), ("2 spaces", False), ("4 spaces", True), ("8 spaces", False)]),
                ("Which of these is a mutable data type?", [("Tuple", False), ("String", False), ("List", True), ("Integer", False)]),
                ("What does len() do?", [("Deletes a list", False), ("Returns length of an object", True), ("Adds elements", False), ("Sorts a list", False)]),
                ("Which keyword is used for loops in Python?", [("loop", False), ("repeat", False), ("for", True), ("iterate", False)]),
                ("What is the correct file extension for Python files?", [(".py", True), (".pt", False), (".pyt", False), (".python", False)]),
                ("How do you create a dictionary in Python?", [("[]", False), ("()", False), ("{}", True), ("<>", False)]),
                ("What does the 'pass' statement do?", [("Exits the function", False), ("Does nothing, acts as placeholder", True), ("Passes a value", False), ("Skips iteration", False)]),
                ("Which function converts a string to integer?", [("str()", False), ("float()", False), ("int()", True), ("chr()", False)]),
                ("What is a lambda function?", [("A named function", False), ("An anonymous function", True), ("A recursive function", False), ("A built-in function", False)]),
                ("What is the output of type(3.14)?", [("<class 'int'>", False), ("<class 'float'>", True), ("<class 'double'>", False), ("<class 'str'>", False)]),
                ("Which method adds an element to the end of a list?", [("add()", False), ("insert()", False), ("append()", True), ("extend()", False)]),
            ]
        },

        # ── OOP ─────────────────────────────────────────────────────────────────
        {
            "subject": "Object Oriented Programming",
            "title": "OOP Concepts Quiz",
            "description": "Test your understanding of OOP principles.",
            "time_limit_minutes": 20,
            "questions": [
                ("What are the four pillars of OOP?", [("Abstraction, Encapsulation, Inheritance, Polymorphism", True), ("Class, Object, Method, Function", False), ("Loop, Array, Pointer, Stack", False), ("Compile, Link, Run, Debug", False)]),
                ("What is a class in OOP?", [("A function", False), ("A blueprint for creating objects", True), ("A variable", False), ("A loop", False)]),
                ("What is encapsulation?", [("Hiding data within a class", True), ("Inheriting from a parent class", False), ("Overloading methods", False), ("Creating objects", False)]),
                ("What is inheritance?", [("Creating new classes from existing ones", True), ("Hiding internal details", False), ("Overriding methods", False), ("Defining multiple constructors", False)]),
                ("What is polymorphism?", [("One interface, many implementations", True), ("Multiple inheritance", False), ("Data hiding", False), ("Method overloading only", False)]),
                ("What is a constructor?", [("A method that destroys objects", False), ("A special method called when an object is created", True), ("A method for sorting", False), ("A static function", False)]),
                ("What is method overriding?", [("Defining multiple methods with same name but different parameters", False), ("Redefining a parent class method in a child class", True), ("Calling a method twice", False), ("Using a method in two classes", False)]),
                ("What is abstraction?", [("Hiding implementation details and showing only functionality", True), ("Copying code from one class to another", False), ("Creating multiple objects", False), ("Using loops inside classes", False)]),
                ("Which keyword is used to inherit a class in Python?", [("extends", False), ("inherits", False), ("class Child(Parent):", True), ("super", False)]),
                ("What is a destructor?", [("A method called when an object is created", False), ("A method called when an object is destroyed", True), ("A static method", False), ("An overloaded method", False)]),
                ("What does 'super()' do in Python?", [("Creates a new object", False), ("Calls the parent class method", True), ("Deletes an object", False), ("Overrides a method", False)]),
                ("What is multiple inheritance?", [("A class inheriting from more than one parent class", True), ("A class with multiple methods", False), ("A method with multiple parameters", False), ("An object of multiple classes", False)]),
                ("What is an abstract class?", [("A class that cannot be instantiated directly", True), ("A class with no methods", False), ("A class with only static methods", False), ("A class that inherits from itself", False)]),
                ("What is an interface?", [("A class with only abstract methods", True), ("A physical device", False), ("A type of variable", False), ("A loop structure", False)]),
            ]
        },

        # ── DBMS ────────────────────────────────────────────────────────────────
        {
            "subject": "Database Management Systems",
            "title": "DBMS Fundamentals Quiz",
            "description": "Test your knowledge of database concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What does DBMS stand for?", [("Data Backup Management System", False), ("Database Management System", True), ("Data Based Monitoring System", False), ("Digital Base Management System", False)]),
                ("Which language is used to query a database?", [("HTML", False), ("Python", False), ("SQL", True), ("CSS", False)]),
                ("What is a primary key?", [("A key used to encrypt data", False), ("A unique identifier for a record in a table", True), ("The first column of a table", False), ("A foreign key reference", False)]),
                ("What is a foreign key?", [("A key from another country", False), ("A key that links two tables together", True), ("A primary key duplicate", False), ("An encrypted key", False)]),
                ("What does SELECT * FROM table do?", [("Deletes all records", False), ("Retrieves all records from the table", True), ("Updates all records", False), ("Creates a new table", False)]),
                ("What is normalization?", [("Making the database faster", False), ("Organizing data to reduce redundancy", True), ("Encrypting the database", False), ("Backing up the database", False)]),
                ("What is a JOIN in SQL?", [("Combining rows from two or more tables", True), ("Deleting duplicate rows", False), ("Creating a new database", False), ("Adding a new column", False)]),
                ("Which normal form removes partial dependencies?", [("1NF", False), ("2NF", True), ("3NF", False), ("BCNF", False)]),
                ("What is a transaction in DBMS?", [("A payment made online", False), ("A unit of work performed against a database", True), ("A backup operation", False), ("A query result", False)]),
                ("What does ACID stand for?", [("Atomicity, Consistency, Isolation, Durability", True), ("Add, Create, Insert, Delete", False), ("Array, Class, Index, Data", False), ("Access, Control, Index, Database", False)]),
                ("What is an ER diagram?", [("A diagram showing employee roles", False), ("A diagram representing entities and their relationships", True), ("An error reporting diagram", False), ("An encryption diagram", False)]),
                ("What is a view in SQL?", [("A virtual table based on a query", True), ("A physical table", False), ("A stored procedure", False), ("An index", False)]),
                ("What is indexing in a database?", [("A technique to speed up data retrieval", True), ("A way to encrypt data", False), ("A backup strategy", False), ("A normalization technique", False)]),
                ("Which command removes a table from the database?", [("DELETE TABLE", False), ("REMOVE TABLE", False), ("DROP TABLE", True), ("TRUNCATE TABLE", False)]),
                ("What is a stored procedure?", [("A saved SQL query that can be reused", True), ("A physical file on disk", False), ("A type of index", False), ("A backup script", False)]),
            ]
        },

        # ── DATA STRUCTURES ─────────────────────────────────────────────────────
        {
            "subject": "Data Structures",
            "title": "Data Structures Quiz",
            "description": "Test your understanding of data structures.",
            "time_limit_minutes": 20,
            "questions": [
                ("What is a data structure?", [("A programming language", False), ("A way to organize and store data", True), ("A type of database", False), ("A hardware component", False)]),
                ("Which data structure uses LIFO?", [("Queue", False), ("Stack", True), ("Array", False), ("Linked List", False)]),
                ("Which data structure uses FIFO?", [("Stack", False), ("Tree", False), ("Queue", True), ("Graph", False)]),
                ("What is the time complexity of binary search?", [("O(n)", False), ("O(n²)", False), ("O(log n)", True), ("O(1)", False)]),
                ("What is a linked list?", [("A list stored in a file", False), ("A linear data structure where elements are linked using pointers", True), ("A sorted array", False), ("A type of queue", False)]),
                ("What is a binary tree?", [("A tree with exactly 2 nodes", False), ("A tree where each node has at most 2 children", True), ("A tree with binary data", False), ("A tree with 2 levels", False)]),
                ("What is the worst case time complexity of bubble sort?", [("O(n log n)", False), ("O(n)", False), ("O(n²)", True), ("O(log n)", False)]),
                ("What is a hash table?", [("A table with encrypted data", False), ("A data structure that maps keys to values using a hash function", True), ("A sorted table", False), ("A type of linked list", False)]),
                ("What is a graph?", [("A chart showing data trends", False), ("A non-linear data structure with nodes and edges", True), ("A type of array", False), ("A binary tree variant", False)]),
                ("What is recursion?", [("A loop that runs forever", False), ("A function that calls itself", True), ("A sorting algorithm", False), ("A data structure", False)]),
                ("What is the best case time complexity of quicksort?", [("O(n²)", False), ("O(n)", False), ("O(n log n)", True), ("O(log n)", False)]),
                ("What is a deque?", [("A double-ended queue", True), ("A type of stack", False), ("A priority queue", False), ("A circular array", False)]),
                ("What is the height of a balanced binary tree with n nodes?", [("O(n)", False), ("O(log n)", True), ("O(n²)", False), ("O(1)", False)]),
                ("Which traversal visits root first?", [("Inorder", False), ("Postorder", False), ("Preorder", True), ("Level order", False)]),
                ("What is a priority queue?", [("A queue where elements are served based on priority", True), ("A queue with fixed size", False), ("A stack with priorities", False), ("A sorted linked list", False)]),
            ]
        },

        # ── UI/UX ───────────────────────────────────────────────────────────────
        {
            "subject": "UI/UX Design",
            "title": "UI/UX Design Principles Quiz",
            "description": "Test your knowledge of UI/UX design.",
            "time_limit_minutes": 15,
            "questions": [
                ("What does UI stand for?", [("User Interface", True), ("Universal Integration", False), ("Unified Interaction", False), ("User Input", False)]),
                ("What does UX stand for?", [("User Experience", True), ("Universal Exchange", False), ("User Execution", False), ("Unified Expression", False)]),
                ("What is a wireframe?", [("A finished design", False), ("A low-fidelity blueprint of a design", True), ("A type of font", False), ("A color palette", False)]),
                ("What is a prototype?", [("A working model of a product for testing", True), ("A final product", False), ("A type of wireframe", False), ("A design color scheme", False)]),
                ("What is the 80/20 rule in UX?", [("80% of users use 20% of features", True), ("80% of design is color", False), ("20% of budget covers 80% of features", False), ("80% of clicks are on images", False)]),
                ("What is a user persona?", [("A fictional character representing a user type", True), ("A real user's profile", False), ("A type of wireframe", False), ("A design element", False)]),
                ("What does 'affordance' mean in UI design?", [("The cost of a design tool", False), ("The visual cue that tells users how to interact with an element", True), ("The loading speed of a UI", False), ("The number of colors used", False)]),
                ("What is a mood board?", [("A project timeline", False), ("A visual collection of design inspiration", True), ("A type of wireframe", False), ("A user journey map", False)]),
                ("What is Fitts's Law?", [("The time to acquire a target depends on distance and size", True), ("Users read left to right", False), ("Colors affect mood", False), ("Simpler is always better", False)]),
                ("What is accessibility in UI/UX?", [("Making designs usable by people with disabilities", True), ("Making apps load faster", False), ("Adding more features", False), ("Reducing design cost", False)]),
                ("What is a call-to-action (CTA)?", [("A button or link that prompts users to take an action", True), ("A type of animation", False), ("A navigation menu", False), ("A color scheme", False)]),
                ("What is whitespace in design?", [("White colored backgrounds", False), ("Empty space between design elements", True), ("A design mistake", False), ("A type of font", False)]),
                ("What is A/B testing in UX?", [("Testing two versions of a design to see which performs better", True), ("Testing on Android and Browser", False), ("Alpha and Beta testing", False), ("Testing accessibility features", False)]),
            ]
        },

        # ── CYBER SECURITY ──────────────────────────────────────────────────────
        {
            "subject": "Cyber Security",
            "title": "Cyber Security Fundamentals Quiz",
            "description": "Test your knowledge of cyber security concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What is phishing?", [("A fishing technique", False), ("A cyber attack using fake emails to steal information", True), ("A type of virus", False), ("A network protocol", False)]),
                ("What does VPN stand for?", [("Virtual Private Network", True), ("Very Protected Node", False), ("Verified Public Network", False), ("Virtual Protocol Network", False)]),
                ("What is malware?", [("Malicious software designed to harm a system", True), ("A type of hardware", False), ("A network protocol", False), ("A programming language", False)]),
                ("What is encryption?", [("Converting data into a coded format to prevent unauthorized access", True), ("Deleting sensitive data", False), ("Compressing files", False), ("Backing up data", False)]),
                ("What is a firewall?", [("A physical wall in a data center", False), ("A security system that monitors and controls network traffic", True), ("A type of virus", False), ("A backup system", False)]),
                ("What is two-factor authentication?", [("Using two passwords", False), ("A security process requiring two forms of verification", True), ("Two firewalls", False), ("Two encryption layers", False)]),
                ("What is ransomware?", [("Software that demands payment to restore access to data", True), ("Free antivirus software", False), ("A network monitoring tool", False), ("A type of firewall", False)]),
                ("What is SQL injection?", [("Adding SQL to a database", False), ("An attack that inserts malicious SQL code into a query", True), ("A database backup technique", False), ("A SQL optimization method", False)]),
                ("What is a DDoS attack?", [("Distributed Denial of Service attack that overwhelms a server", True), ("A data deletion attack", False), ("A password cracking attack", False), ("A phishing technique", False)]),
                ("What is social engineering in cyber security?", [("Building social media apps", False), ("Manipulating people into revealing confidential information", True), ("Engineering social networks", False), ("A type of firewall", False)]),
                ("What does HTTPS stand for?", [("HyperText Transfer Protocol Secure", True), ("High Transfer Text Protocol System", False), ("HyperText Transmission Protocol Standard", False), ("High Tech Transfer Protocol Security", False)]),
                ("What is a zero-day vulnerability?", [("A vulnerability fixed in zero days", False), ("An unknown software vulnerability that hackers exploit before it's patched", True), ("A vulnerability in day-zero of software release", False), ("A vulnerability with no risk", False)]),
                ("What is a brute force attack?", [("Physically breaking into a server", False), ("Trying all possible combinations to crack a password", True), ("A DDoS attack variant", False), ("A social engineering attack", False)]),
                ("What is the CIA triad in security?", [("Confidentiality, Integrity, Availability", True), ("Code, Interface, Access", False), ("Control, Identify, Authenticate", False), ("Cyber, Internet, Access", False)]),
            ]
        },

        # ── AI ──────────────────────────────────────────────────────────────────
        {
            "subject": "Artificial Intelligence",
            "title": "Artificial Intelligence Quiz",
            "description": "Test your knowledge of AI concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What does AI stand for?", [("Automated Integration", False), ("Artificial Intelligence", True), ("Advanced Internet", False), ("Automated Input", False)]),
                ("What is machine learning?", [("Programming computers with explicit rules", False), ("A subset of AI that allows systems to learn from data", True), ("A type of hardware", False), ("A programming language", False)]),
                ("What is a neural network?", [("A computer network", False), ("A system inspired by the human brain used to recognize patterns", True), ("A type of database", False), ("A security system", False)]),
                ("What is natural language processing (NLP)?", [("A programming language", False), ("AI's ability to understand and process human language", True), ("A type of encryption", False), ("A hardware component", False)]),
                ("What is the Turing Test?", [("A speed test for computers", False), ("A test to determine if a machine can exhibit human-like intelligence", True), ("A programming test", False), ("A hardware benchmark", False)]),
                ("What is deep learning?", [("Learning from deep web", False), ("A subset of machine learning using multi-layered neural networks", True), ("Programming at a low level", False), ("A type of database", False)]),
                ("What is computer vision?", [("A monitor specification", False), ("AI's ability to interpret and understand visual information", True), ("A type of camera", False), ("A graphics card feature", False)]),
                ("What is reinforcement learning?", [("Learning from textbooks", False), ("Learning through rewards and penalties from interactions", True), ("A type of supervised learning", False), ("Learning from labeled data", False)]),
                ("What is an expert system?", [("A system used by experts only", False), ("An AI system that mimics the decision-making of a human expert", True), ("A high-performance computer", False), ("A type of neural network", False)]),
                ("What is overfitting in ML?", [("Training a model too slowly", False), ("When a model performs well on training data but poorly on new data", True), ("Using too much training data", False), ("A type of neural network error", False)]),
                ("What is a chatbot?", [("A robot that chats physically", False), ("An AI program that simulates conversation with users", True), ("A type of email", False), ("A social media bot", False)]),
                ("What is supervised learning?", [("Learning with a teacher present", False), ("Training a model using labeled data", True), ("Learning without any data", False), ("A type of reinforcement learning", False)]),
                ("What is unsupervised learning?", [("Training without a computer", False), ("Finding patterns in data without labeled examples", True), ("A type of supervised learning", False), ("Learning from rewards", False)]),
                ("What is a recommendation system?", [("A system that recommends hardware upgrades", False), ("An AI system that suggests items based on user preferences", True), ("A type of search engine", False), ("A chatbot variant", False)]),
            ]
        },

        # ── ML ──────────────────────────────────────────────────────────────────
        {
            "subject": "Machine Learning",
            "title": "Machine Learning Quiz",
            "description": "Test your knowledge of ML algorithms and concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What is a training dataset?", [("Data used to evaluate a model", False), ("Data used to train a machine learning model", True), ("Random data", False), ("Encrypted data", False)]),
                ("What is a test dataset?", [("Data used to train the model", False), ("Data used to evaluate model performance", True), ("Data used for validation", False), ("A backup dataset", False)]),
                ("What is linear regression used for?", [("Classification problems", False), ("Predicting a continuous output value", True), ("Clustering data", False), ("Image recognition", False)]),
                ("What is logistic regression used for?", [("Predicting continuous values", False), ("Binary classification problems", True), ("Clustering", False), ("Dimensionality reduction", False)]),
                ("What is a decision tree?", [("A tree diagram for project planning", False), ("A model that splits data based on feature values to make predictions", True), ("A type of neural network", False), ("A sorting algorithm", False)]),
                ("What is cross-validation?", [("Testing on multiple computers", False), ("A technique to assess model performance using multiple data splits", True), ("A type of overfitting", False), ("A data cleaning method", False)]),
                ("What is the k in k-nearest neighbors?", [("The number of layers in a neural network", False), ("The number of nearest data points considered for classification", True), ("The learning rate", False), ("The number of features", False)]),
                ("What is clustering?", [("Grouping similar data points together without labels", True), ("A type of supervised learning", False), ("Training a neural network", False), ("A data cleaning technique", False)]),
                ("What is gradient descent?", [("Going downhill physically", False), ("An optimization algorithm used to minimize the loss function", True), ("A type of decision tree", False), ("A clustering algorithm", False)]),
                ("What is a confusion matrix?", [("A matrix that confuses the model", False), ("A table showing model prediction results vs actual results", True), ("A type of neural network layer", False), ("A data preprocessing tool", False)]),
                ("What is feature engineering?", [("Building physical features", False), ("Creating or selecting relevant input variables for a model", True), ("Training a model", False), ("Testing a model", False)]),
                ("What does precision measure?", [("How fast a model runs", False), ("The proportion of true positives among all positive predictions", True), ("The total accuracy", False), ("The recall score", False)]),
                ("What is the purpose of a validation set?", [("To train the model", False), ("To tune hyperparameters and prevent overfitting", True), ("To test the final model", False), ("To clean data", False)]),
                ("What is a hyperparameter?", [("A parameter learned during training", False), ("A parameter set before training that controls the learning process", True), ("A type of feature", False), ("An output variable", False)]),
                ("What is ensemble learning?", [("Learning from a single model", False), ("Combining multiple models to improve performance", True), ("A type of clustering", False), ("A neural network technique", False)]),
            ]
        },

        # ── COMPUTER NETWORKS ───────────────────────────────────────────────────
        {
            "subject": "Computer Networks",
            "title": "Computer Networks Quiz",
            "description": "Test your knowledge of networking concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What does IP stand for?", [("Internet Protocol", True), ("Internal Process", False), ("Integrated Program", False), ("Input Port", False)]),
                ("What does HTTP stand for?", [("HyperText Transfer Protocol", True), ("High Tech Transfer Protocol", False), ("HyperText Transmission Program", False), ("Host Transfer Protocol", False)]),
                ("What is a router?", [("A device that connects networks and routes data packets", True), ("A type of cable", False), ("A wireless device only", False), ("A type of server", False)]),
                ("What is DNS?", [("Domain Name System that translates domain names to IP addresses", True), ("Data Network Service", False), ("Digital Network System", False), ("Domain Number Service", False)]),
                ("What is the OSI model?", [("A framework defining how data is transmitted across a network in 7 layers", True), ("An operating system", False), ("A programming model", False), ("A security framework", False)]),
                ("Which layer of OSI handles routing?", [("Transport layer", False), ("Network layer", True), ("Data link layer", False), ("Application layer", False)]),
                ("What is a MAC address?", [("An Apple computer address", False), ("A unique hardware identifier assigned to a network interface", True), ("A type of IP address", False), ("A wireless network address", False)]),
                ("What is bandwidth?", [("The physical width of a cable", False), ("The maximum data transfer rate of a network", True), ("The number of connected devices", False), ("The network security level", False)]),
                ("What is a subnet mask?", [("A mask used to hide network details", False), ("A number that divides an IP address into network and host parts", True), ("A type of firewall", False), ("A wireless security protocol", False)]),
                ("What is TCP?", [("Transmission Control Protocol that ensures reliable data delivery", True), ("Transfer Communication Protocol", False), ("Technical Control Program", False), ("Text Control Protocol", False)]),
                ("What is the difference between TCP and UDP?", [("TCP is faster, UDP is slower", False), ("TCP is reliable and connection-oriented, UDP is faster but unreliable", True), ("They are the same", False), ("UDP is more secure than TCP", False)]),
                ("What is a LAN?", [("Large Area Network", False), ("Local Area Network covering a small geographical area", True), ("Long Access Node", False), ("Linked Area Network", False)]),
                ("What is a WAN?", [("Wireless Area Network", False), ("Wide Area Network covering large geographical areas", True), ("Web Access Node", False), ("Wired Area Network", False)]),
                ("What is latency?", [("The speed of a network", False), ("The delay in data transmission across a network", True), ("The number of packets sent", False), ("The network bandwidth", False)]),
            ]
        },

        # ── WEB DEVELOPMENT ─────────────────────────────────────────────────────
        {
            "subject": "Web Development",
            "title": "Web Development Quiz",
            "description": "Test your knowledge of web development concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What does HTML stand for?", [("HyperText Markup Language", True), ("High Tech Modern Language", False), ("HyperText Machine Language", False), ("Home Tool Markup Language", False)]),
                ("What does CSS stand for?", [("Cascading Style Sheets", True), ("Computer Style System", False), ("Creative Style Sheets", False), ("Coded Style System", False)]),
                ("What is JavaScript used for?", [("Styling web pages", False), ("Adding interactivity and dynamic behavior to web pages", True), ("Structuring web content", False), ("Managing databases", False)]),
                ("What is a responsive design?", [("A design that responds to clicks", False), ("A design that adapts to different screen sizes", True), ("A fast-loading design", False), ("A design with animations", False)]),
                ("What is the DOM?", [("Document Object Model representing the structure of a web page", True), ("Domain Object Management", False), ("Data Object Model", False), ("Document Output Mode", False)]),
                ("What is an API?", [("Application Programming Interface that allows software to communicate", True), ("Advanced Programming Integration", False), ("Automated Program Input", False), ("Application Process Interface", False)]),
                ("What is a REST API?", [("A type of database", False), ("An architectural style for designing networked applications", True), ("A programming language", False), ("A web browser", False)]),
                ("What is a framework in web development?", [("A physical structure", False), ("A pre-built set of tools and libraries to speed up development", True), ("A type of database", False), ("A programming language", False)]),
                ("What does 'frontend' refer to?", [("The server-side of a web application", False), ("The client-side part of a web app that users interact with", True), ("The database layer", False), ("The network layer", False)]),
                ("What does 'backend' refer to?", [("The visual part of a web app", False), ("The server-side logic, database, and APIs", True), ("The CSS styling", False), ("The browser rendering", False)]),
                ("What is a cookie in web development?", [("A snack for developers", False), ("A small piece of data stored on the user's browser", True), ("A type of JavaScript function", False), ("A server-side script", False)]),
                ("What is version control?", [("Controlling the app version number", False), ("A system for tracking changes in code over time (e.g., Git)", True), ("A type of database backup", False), ("A deployment strategy", False)]),
                ("What is Git?", [("A programming language", False), ("A distributed version control system", True), ("A web framework", False), ("A type of database", False)]),
                ("What is npm?", [("Node Package Manager used to manage JavaScript packages", True), ("Network Protocol Manager", False), ("New Programming Module", False), ("Node Programming Mode", False)]),
            ]
        },

        # ── AR/VR ───────────────────────────────────────────────────────────────
        {
            "subject": "AR/VR Technology",
            "title": "AR/VR Technology Quiz",
            "description": "Test your knowledge of Augmented and Virtual Reality.",
            "time_limit_minutes": 15,
            "questions": [
                ("What does AR stand for?", [("Augmented Reality", True), ("Automated Reality", False), ("Advanced Rendering", False), ("Artificial Reality", False)]),
                ("What does VR stand for?", [("Virtual Reality", True), ("Visual Rendering", False), ("Verified Reality", False), ("Video Reality", False)]),
                ("What is the difference between AR and VR?", [("AR adds digital elements to the real world; VR creates a fully virtual environment", True), ("AR is older than VR", False), ("VR uses cameras while AR uses headsets", False), ("They are the same technology", False)]),
                ("What is Mixed Reality (MR)?", [("A combination of AR and VR", True), ("A type of VR only", False), ("A type of AR only", False), ("A standalone technology unrelated to AR/VR", False)]),
                ("What device is commonly used for VR?", [("Smartphone only", False), ("VR headset", True), ("Smart glasses", False), ("A regular monitor", False)]),
                ("What is a 360-degree video?", [("A video that lasts 360 seconds", False), ("A video that captures all directions simultaneously", True), ("A video with 360 frames per second", False), ("A video in 360p resolution", False)]),
                ("What is spatial computing?", [("Computing in space (outer space)", False), ("Technology that integrates digital information into physical spaces", True), ("A type of cloud computing", False), ("A 2D computing paradigm", False)]),
                ("Which company makes the Meta Quest headset?", [("Apple", False), ("Sony", False), ("Meta (formerly Facebook)", True), ("Microsoft", False)]),
                ("What is haptic feedback?", [("Visual feedback in VR", False), ("Tactile sensations simulated in VR/AR experiences", True), ("Audio feedback", False), ("A type of motion tracking", False)]),
                ("What is motion tracking in VR?", [("Tracking internet speed", False), ("Technology that detects and responds to physical movements", True), ("A camera feature", False), ("A type of display technology", False)]),
                ("What is the field of view (FOV) in VR?", [("The video quality", False), ("The extent of the observable world seen at any moment", True), ("The frame rate", False), ("The resolution of the headset", False)]),
                ("What is an AR marker?", [("A physical or digital reference point that triggers AR content", True), ("A type of VR controller", False), ("A camera filter", False), ("A QR code only", False)]),
                ("What is presence in VR?", [("The physical location of the user", False), ("The feeling of actually being inside the virtual environment", True), ("The number of users in VR", False), ("The VR headset's weight", False)]),
            ]
        },

        # ── MATHS ───────────────────────────────────────────────────────────────
        {
            "subject": "Mathematics",
            "title": "Applied Mathematics Quiz",
            "description": "Test your knowledge of mathematics concepts.",
            "time_limit_minutes": 20,
            "questions": [
                ("What is a prime number?", [("A number divisible by all numbers", False), ("A number greater than 1 divisible only by 1 and itself", True), ("An even number", False), ("A number divisible by 2", False)]),
                ("What is the value of π (pi) approximately?", [("2.718", False), ("3.14159", True), ("1.618", False), ("2.302", False)]),
                ("What is a matrix?", [("A movie", False), ("A rectangular array of numbers arranged in rows and columns", True), ("A type of equation", False), ("A single number", False)]),
                ("What is the derivative of x²?", [("x", False), ("2x", True), ("x²", False), ("2", False)]),
                ("What is a logarithm?", [("The inverse operation of exponentiation", True), ("A type of matrix", False), ("A geometric shape", False), ("A probability concept", False)]),
                ("What is the Pythagorean theorem?", [("a² + b² = c² for right triangles", True), ("a + b = c", False), ("a² - b² = c²", False), ("a × b = c²", False)]),
                ("What is a set in mathematics?", [("A collection of distinct objects", True), ("A type of equation", False), ("A matrix operation", False), ("A number sequence", False)]),
                ("What is probability?", [("A measure of certainty", False), ("A measure of how likely an event is to occur", True), ("A type of statistics", False), ("A counting technique", False)]),
                ("What is a permutation?", [("An arrangement where order does not matter", False), ("An arrangement of items where order matters", True), ("A combination of items", False), ("A mathematical set", False)]),
                ("What is a combination?", [("A selection where order matters", False), ("A selection of items where order does not matter", True), ("A type of permutation", False), ("A matrix operation", False)]),
                ("What is the mean of a dataset?", [("The middle value", False), ("The most frequent value", False), ("The sum of all values divided by the count", True), ("The largest value", False)]),
                ("What is variance?", [("The average of the dataset", False), ("A measure of how spread out data is from the mean", True), ("The middle value of data", False), ("The most common value", False)]),
                ("What is a vector?", [("A scalar quantity", False), ("A quantity with both magnitude and direction", True), ("A type of matrix", False), ("A random number", False)]),
                ("What is integration in calculus?", [("Finding the derivative", False), ("Finding the area under a curve", True), ("Solving equations", False), ("Finding the slope of a line", False)]),
                ("What is a Boolean algebra?", [("Algebra using complex numbers", False), ("Algebra dealing with true/false values", True), ("A type of matrix algebra", False), ("Algebra with fractions", False)]),
            ]
        },

        # ── ICT ─────────────────────────────────────────────────────────────────
        {
            "subject": "ICT",
            "title": "ICT Fundamentals Quiz",
            "description": "Test your knowledge of Information and Communication Technology.",
            "time_limit_minutes": 20,
            "questions": [
                ("What does ICT stand for?", [("Information and Communication Technology", True), ("Integrated Computer Technology", False), ("Internet Communication Tools", False), ("Information Control Technology", False)]),
                ("What is the Internet?", [("A single computer network", False), ("A global system of interconnected computer networks", True), ("A type of software", False), ("A hardware component", False)]),
                ("What is cloud computing?", [("Computing using weather data", False), ("Delivering computing services over the internet", True), ("A type of hardware", False), ("A programming language", False)]),
                ("What is an operating system?", [("A type of application software", False), ("System software that manages hardware and software resources", True), ("A programming language", False), ("A network protocol", False)]),
                ("What is a bit?", [("The smallest unit of digital data (0 or 1)", True), ("A type of byte", False), ("8 bytes", False), ("A megabyte", False)]),
                ("How many bits are in a byte?", [("4", False), ("8", True), ("16", False), ("32", False)]),
                ("What is a spreadsheet?", [("A type of word processor", False), ("A software for organizing data in rows and columns for calculations", True), ("A presentation tool", False), ("A database", False)]),
                ("What is a URL?", [("Uniform Resource Locator — the address of a web resource", True), ("Universal Remote Login", False), ("Unified Resource Language", False), ("User Resource Link", False)]),
                ("What is an email?", [("Electronic mail for sending messages over the internet", True), ("A type of website", False), ("A programming language", False), ("A hardware device", False)]),
                ("What is a search engine?", [("A car engine powered by search", False), ("A software system that searches for information on the web", True), ("A type of database", False), ("A browser plugin", False)]),
                ("What is digital literacy?", [("The ability to read digital text only", False), ("The ability to use digital technology effectively and safely", True), ("A programming skill", False), ("A hardware certification", False)]),
                ("What is open-source software?", [("Software that costs nothing", False), ("Software with publicly available source code that anyone can modify", True), ("Software without any features", False), ("Software made by one company only", False)]),
                ("What is a binary number system?", [("A system using digits 0-9", False), ("A number system using only 0 and 1", True), ("A system using hexadecimal digits", False), ("A system with 8 digits", False)]),
                ("What is IoT?", [("Internet of Things — connecting physical devices to the internet", True), ("Internet of Technology", False), ("Integrated Online Tools", False), ("Input Output Technology", False)]),
                ("What is big data?", [("Large files on a computer", False), ("Extremely large datasets that require special tools to process", True), ("A type of database", False), ("A cloud storage service", False)]),
            ]
        },
    ]

    print(f"\nCreating {len(all_quizzes_data)} quizzes across all subjects...\n")

    all_quizzes = []
    for quiz_data in all_quizzes_data:
        subject, created = Subject.objects.get_or_create(name=quiz_data["subject"])
        quiz = Quiz.objects.create(
            title=quiz_data["title"],
            subject=subject,
            description=quiz_data["description"],
            time_limit_minutes=quiz_data["time_limit_minutes"],
            is_active=True,
        )
        questions = []
        for q_text, options_data in quiz_data["questions"]:
            question = Question.objects.create(
                quiz=quiz,
                question_text=q_text,
                marks=2,
                difficulty=random.choice(["Easy", "Medium", "Hard"]),
            )
            questions.append(question)
            for opt_text, is_correct in options_data:
                Option.objects.create(
                    question=question,
                    option_text=opt_text,
                    is_correct=is_correct,
                )
        all_quizzes.append((quiz, questions))
        print(f"  ✅ Created: {quiz.title} ({len(questions)} questions)")

    print("\nCreating quiz attempts for students...")
    for quiz, questions in all_quizzes[:5]:
        for student in students[:3]:
            score = 0
            attempt = QuizAttempt.objects.create(
                student=student,
                quiz=quiz,
                score=0,
                is_completed=True,
                start_time=timezone.now(),
                end_time=timezone.now(),
                time_taken_seconds=random.randint(300, 1200),
            )
            for q in questions:
                correct = random.random() > 0.4
                if correct:
                    opt = Option.objects.get(question=q, is_correct=True)
                    score += q.marks
                else:
                    opt = Option.objects.filter(question=q, is_correct=False).first()
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=q,
                    selected_option=opt,
                    is_correct=correct,
                )
            attempt.score = score
            attempt.save()

    print("\n✅ Database populated successfully!")
    print(f"   Subjects: {Subject.objects.count()}")
    print(f"   Quizzes:  {Quiz.objects.count()}")
    print(f"   Questions:{Question.objects.count()}")
    print(f"   Students: {CustomUser.objects.filter(user_type='student').count()}")


if __name__ == '__main__':
    populate()