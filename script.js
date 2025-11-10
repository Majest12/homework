// 1. UPDATED Mock Backend Data
const mediaDatabase = [
    // Film / TV Series
    {
        type: "Film / TV Series",
        title: "You",
        author: "Greg Berlanti & Sera Gamble",
        date: "2018",
        category: "TV Series",
        backend_id: "TVS-2018-005"
    },
    {
        type: "Film / TV Series",
        title: "Reign",
        author: "Laurie McCarthy & Stephanie SenGupta",
        date: "2013",
        category: "TV Series",
        backend_id: "TVS-2013-006"
    },
    {
        type: "Film / TV Series",
        title: "Dynasty",
        author: "Richard & Esther Shapiro (original); Reboot by Sallie Patrick, Josh Schwartz & Stephanie Savage",
        date: "1981 / 2017",
        category: "TV Series",
        backend_id: "TVS-2017-007"
    },
    {
        type: "Film / TV Series",
        title: "The Blacklist",
        author: "Jon Bokenkamp",
        date: "2013",
        category: "TV Series",
        backend_id: "TVS-2013-008"
    },
    {
        type: "Film / TV Series",
        title: "Designated Survivor",
        author: "David Guggenheim",
        date: "2016",
        category: "TV Series",
        backend_id: "TVS-2016-009"
    },
    // Books
    {
        type: "Book",
        title: "To Kill a Mockingbird",
        author: "Harper Lee",
        date: "1960",
        category: "Book",
        backend_id: "B-1960-010"
    },
    {
        type: "Book",
        title: "Pride and Prejudice",
        author: "Jane Austen",
        date: "1813",
        category: "Book",
        backend_id: "B-1813-011"
    },
    {
        type: "Book",
        title: "Fahrenheit 451",
        author: "Ray Bradbury",
        date: "1953",
        category: "Book",
        backend_id: "B-1953-012"
    },
    {
        type: "Book",
        title: "Dune",
        author: "Frank Herbert",
        date: "1965",
        category: "Book",
        backend_id: "B-1965-013"
    },
    {
        type: "Book",
        title: "The Martian",
        author: "Andy Weir",
        date: "2011",
        category: "Book",
        backend_id: "B-2011-014"
    },
    // Journal / Magazine
    {
        type: "Journal / Magazine",
        title: "Time Magazine",
        author: "Briton Hadden & Henry Luce",
        date: "1923 (Founding Year)",
        category: "Journal",
        backend_id: "J-1923-015"
    }
];

// 2. DOM Element References
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const resultsContainer = document.getElementById('results-container');

// 3. Search Logic Function
function performSearch() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    resultsContainer.innerHTML = ''; 

    if (searchTerm === "") {
        resultsContainer.innerHTML = '<p style="color: #1a73e8; font-style: italic;">Please enter a title, author, or keyword to search.</p>';
        document.getElementById('search-results-section').scrollIntoView({ behavior: 'smooth' });
        return;
    }

    // Filter the database: Search by title OR author
    const foundMedia = mediaDatabase.filter(media =>
        media.title.toLowerCase().includes(searchTerm) ||
        media.author.toLowerCase().includes(searchTerm)
    );

    // 4. Render Results - THIS IS THE CRITICAL SECTION
    if (foundMedia.length > 0) {
        let htmlContent = `<h3 style="color: #343a40;">✅ Found ${foundMedia.length} Item(s) matching "${searchInput.value}"</h3>`;

        foundMedia.forEach(media => {
            // Check that media.author, media.date, media.type, etc. are correctly used here.
            htmlContent += `
                <div class="media-detail-block" style="display: block; border: 1px solid #1a73e8; padding: 20px; margin-bottom: 25px; border-radius: 8px; background: #e6f0ff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <h4 style="color: #1a73e8; margin-top: 0; border-bottom: 1px dashed #a0c3ff; padding-bottom: 5px;">${media.title}</h4>
                    <p><strong>Author / Creator / Producer:</strong> ${media.author}</p>
                    <p><strong>Publication / Release Date:</strong> ${media.date}</p>
                    <p><strong>Type:</strong> ${media.type}</p>
                    <p><strong>Category:</strong> ${media.category}</p>
                    <p style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #cceeff;">
                        <strong>Backend Detail (ID):</strong> <code style="background: #f0f8ff; padding: 4px 8px; border-radius: 4px; color: #c0392b;">${media.backend_id}</code>
                    </p>
                </div>
            `;
        });

        resultsContainer.innerHTML = htmlContent;
    } else {
        // 5. Not Found Message
        resultsContainer.innerHTML = `
            <div style="padding: 30px; border: 2px dashed #e74c3c; border-radius: 8px; background: #fdf2f2; color: #c0392b; text-align: center;">
                <h3>❌ Media Not Found / Item Not Available</h3>
                <p>No item matching **"${searchInput.value}"** was found in the library database.</p>
                <p style="font-size: 0.9em; margin-top: 15px;">Please check your spelling or try a different keyword.</p>
            </div>
        `;
    }

    document.getElementById('search-results-section').scrollIntoView({ behavior: 'smooth' });
}

// 6. Event Listeners
searchButton.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});