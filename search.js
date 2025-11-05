// Local images in the same directory
const mediaImages = [
    { name: "The Martian", src: "martian.jpg", link: "#detail-martian" },
    { name: "Dune", src: "dune.jpg", link: "#detail-dune" },
    { name: "Time Magazine", src: "time.jpg", link: "#detail-time" },
];

const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");

searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    searchResults.innerHTML = "";

    if (!query) {
        searchResults.style.display = "none";
        return;
    }

    const filtered = mediaImages.filter(item => item.name.toLowerCase().includes(query));

    if (filtered.length === 0) {
        searchResults.style.display = "none";
        return;
    }

    filtered.forEach(item => {
        const img = document.createElement("img");
        img.src = item.src;
        img.alt = item.name;
        img.title = item.name;
        img.onclick = () => window.location.href = item.link;
        searchResults.appendChild(img);
    });

    searchResults.style.display = "flex";
});
