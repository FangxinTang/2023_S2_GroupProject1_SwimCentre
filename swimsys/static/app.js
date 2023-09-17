// alert("Hello, this is a test!");


// confirm canceling a group class or lesson
var cancelButtons = document.querySelectorAll('.cancel-btn');

cancelButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        var userChoice = confirm("Are you sure you want to cancel this booking?");
        if (!userChoice) {
            event.preventDefault(); 
        }
    });
});


// confirm booking a group class or lesson
var bookButtons = document.querySelectorAll('.book-btn');

bookButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        var userChoice = confirm("Are you sure you want to book this booking?");
        if (!userChoice) {
            event.preventDefault(); 
        }
    });
});


// confirm paying tuition button
var bookButtons = document.querySelectorAll('.tuition-btn');

bookButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        var userChoice = confirm("Booking a private lesson is non-refundable. Click 'OK' to proceed with this payment");
        if (!userChoice) {
            event.preventDefault(); 
        }
    });
});

// confirm paying subscription button
var bookButtons = document.querySelectorAll('.subscription-btn');

bookButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        var userChoice = confirm("Subscription is non-refundable. Click 'OK' to proceed with this payment");
        if (!userChoice) {
            event.preventDefault(); 
        }
    });
});



// regular back button, (if saving, booking, canceling, paying page, use direct url, not this function)
function goBack() {
    window.history.back();
}

// confirm saving changes of my profile
var saveButtons = document.querySelectorAll('.save-btn');

saveButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        var userChoice = confirm('Are you sure you want to make these changes?');
        if (!userChoice) {
            event.preventDefault();
        }
    }
    )
}
)


