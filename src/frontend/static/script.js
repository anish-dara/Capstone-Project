// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('playerSearch');
    const searchButton = document.getElementById('searchButton');
    
    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/players?search=${encodeURIComponent(query)}`;
        } else {
            window.location.href = '/players';
        }
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }
});

// Add loading states for buttons
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function() {
        if (this.type === 'submit' || this.classList.contains('btn-primary')) {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            this.disabled = true;
        }
    });
});