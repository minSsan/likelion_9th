var searchButton = document.querySelector('.search_button')

function startSearch(value) {
    location.href = `map/${value}`;
};

searchButton.addEventListener('click', function() {
    var keyword = document.getElementById("searchKeyword").value;
    startSearch(keyword);
});
