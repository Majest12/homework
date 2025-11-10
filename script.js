// Start of IIFE
(function() {

// 1. UPDATED Mock Backend Data
// ... all your mediaDatabase content ...

// 2. DOM Element References
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const resultsContainer = document.getElementById('results-container');
const searchResults = document.getElementById("search-results"); 

// 3. Search Logic Function
function performSearch() {
    // ... all the search logic and HTML rendering code ...
}

// 6. Event Listeners
searchButton.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault(); 
        performSearch();
    }
});

})(); // End of IIFE