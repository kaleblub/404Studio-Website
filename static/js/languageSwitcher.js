function switchLanguage(languageCode) {
    console.log('Switching language to:', languageCode); // Test if function is called
    fetch("{% url 'set_language' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: 'language=' + languageCode
    }).then(response => {
        console.log('Response status:', response.status); // Test server response
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Language switch failed:', response.statusText);
        }
    }).catch(error => console.error('Fetch error:', error));
}