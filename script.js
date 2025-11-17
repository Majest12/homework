// Function to show the selected media detail panel and hide others
function showMediaDetail(clickedElement) {
    // 1. Get the ID of the detail panel to show
    const targetId = clickedElement.getAttribute('data-target');
    
    // 2. Hide all detail blocks (remove 'is-active' class)
    document.querySelectorAll('.media-detail-block').forEach(block => {
        block.classList.remove('is-active');
    });

    // 3. Show the target detail block (add 'is-active' class)
    const targetBlock = document.getElementById(targetId);
    if (targetBlock) {
        targetBlock.classList.add('is-active');
    }
}

// Function to handle the search button click (MOCK IMPLEMENTATION)
document.getElementById('search-button').addEventListener('click', function() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('results-container');
    const mockData = [
        { name: "The Python Primer", author: "A. Developer", category: "Book", id: "detail-book1" },
        { name: "Project Deployment", author: "B. Analyst", category: "Film", id: "detail-film1" },
        { name: "Flask Insights Q3", author: "C. Engineer", category: "Magazine", id: "detail-mag1" }
    ];

    // Find a matching item
    const foundItem = mockData.find(item => 
        item.name.toLowerCase().includes(searchTerm) || 
        item.author.toLowerCase().includes(searchTerm)
    );

    // 1. CLEAR PREVIOUS DETAIL DISPLAY (This is the critical fix)
    document.querySelectorAll('.media-detail-block').forEach(block => {
        block.classList.remove('is-active');
    });
    // Ensure the default message is shown if no item is selected after search
    document.getElementById('detail-default').classList.add('is-active'); 

    // 2. Display the search results
    if (foundItem) {
        resultsContainer.innerHTML = `
            <div class="search-result-item">
                <h4>${foundItem.name}</h4>
                <p>By: ${foundItem.author} (${foundItem.category})</p>
                <button class="search-detail-button" data-target="${foundItem.id}" onclick="showMediaDetail(this)">View Details</button>
            </div>
        `;
    } else {
        resultsContainer.innerHTML = `<p style="font-style: italic; color: #555;">No results found for "${searchTerm}".</p>`;
    }
});

// Initial setup to ensure only the default detail block is active on load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.media-detail-block').forEach(block => {
        if (block.id !== 'detail-default') {
             block.classList.remove('is-active');
        } else {
             block.classList.add('is-active'); // Ensure default is active
        }
    });
});