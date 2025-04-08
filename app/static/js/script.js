document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let valid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                valid = false;
                input.style.borderColor = 'red';
                input.placeholder = 'دا فیلډ اړین دی!';
            } else {
                input.style.borderColor = '#ddd';
            }
        });

        if (!valid) {
            alert('مهرباني وکړئ ټول اړین فیلډونه ډک کړئ!');
        } else {
            submitForm(form);
        }
    });
});

function submitForm(form) {
    const formData = new FormData(form);
    const action = form.getAttribute('action');

    fetch(action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('معلومات په بریالیتوب سره ثبت شول!');
            form.reset();
            location.reload();
        } else {
            alert('ستونزه رامنځته شوه: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('د سرور سره اړیکه ناکامه شوه!');
    });
}