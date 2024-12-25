let isLoggedIn = false;

// Function to handle switching between tabs
function openTab(event, tabName) {
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => pane.classList.remove('active'));

    const activeTab = document.getElementById(tabName);
    activeTab.classList.add('active');
}

// Add event listeners for tab buttons
document.addEventListener('DOMContentLoaded', function() {
    // Tab button event listeners
    document.getElementById('howItWorksTab').addEventListener('click', function(event) {
        openTab(event, 'howItWorks');
    });

    document.getElementById('signInTab').addEventListener('click', function(event) {
        openTab(event, 'signIn');
    });

    document.getElementById('inputLabelTab').addEventListener('click', function(event) {
        if (isLoggedIn) {
            openTab(event, 'inputLabel');
        } else {
            alert('Please sign in first!');
        }
    });

    // Sign In form submission
    document.getElementById('signInForm').addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Sign in form submitted');

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Store credentials for later use
        localStorage.setItem('userEmail', email);
        localStorage.setItem('userPassword', password);

        isLoggedIn = true;
        document.getElementById('inputLabelTab').style.display = 'inline-block';
        openTab(null, 'inputLabel');
    });

    // Label form submission
    document.getElementById('labelForm').addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('Label form submitted');

        if (!isLoggedIn) {
            alert('You must sign in first!');
            return;
        }

        const categories = document.getElementById('categories').value.trim();
        const email = localStorage.getItem('userEmail');
        const password = localStorage.getItem('userPassword');

        // Send data to backend
        fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                categories: categories,
                username: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('Processing completed!');
            console.log(data);
        })
        .catch(error => {
            alert('Error processing emails. Please check console for details.');
            console.error('Error:', error);
        });
    });
});