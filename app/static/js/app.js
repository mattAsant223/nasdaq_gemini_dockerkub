document.addEventListener('DOMContentLoaded', () => {
    const austinBtn = document.getElementById('btn-austin');
    const dallasBtn = document.getElementById('btn-dallas');
    const resultsContainer = document.getElementById('results');
    const loader = document.getElementById('loader');
    const top10List = document.getElementById('top-10-list');

    // Function to format large numbers into Trillions, Billions
    const formatMarketCap = (num) => {
        if (num === null) return 'N/A';
        if (num >= 1e12) {
            return (num / 1e12).toFixed(2) + 'T';
        }
        if (num >= 1e9) {
            return (num / 1e9).toFixed(2) + 'B';
        }
        return num.toLocaleString();
    };

    // Fetch and populate top 10 list on startup
    const loadTopCompanies = async () => {
        // This is a static list now to avoid hitting the API rate limit on page load.
        const topNasdaqCompanies = [
            "MSFT", "AAPL", "NVDA", "GOOGL", "AMZN", 
            "META", "AVGO", "TSLA", "COST", "ADBE"
        ];

        top10List.innerHTML = ''; // Clear list
        topNasdaqCompanies.forEach(ticker => {
            const li = document.createElement('li');
            const strong = document.createElement('strong');
            strong.textContent = ticker;
            li.appendChild(strong);
            top10List.appendChild(li);
        });
    };

    const analyzeCity = async (city) => {
        resultsContainer.innerHTML = '';
        loader.classList.remove('hidden');

        try {
            const response = await fetch(`/api/analyze/${city}`);
            const data = await response.json();

            if (response.ok) {
                resultsContainer.innerHTML = `<pre>${data.analysis}</pre>`;
            } else {
                resultsContainer.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            resultsContainer.textContent = 'An error occurred while fetching data.';
        } finally {
            loader.classList.add('hidden');
        }
    };

    // Initial setup
    loadTopCompanies();
    austinBtn.addEventListener('click', () => analyzeCity('austin'));
    dallasBtn.addEventListener('click', () => analyzeCity('dallas'));
});