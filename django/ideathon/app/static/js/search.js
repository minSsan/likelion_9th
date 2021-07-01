const searchGrid = document.querySelector('.search-grid')
const searchButton = searchGrid.querySelectorAll('.search-button')

function startSearch(value) {
    location.href = `map/${value}`;
};

[].forEach.call(searchButton,function(searchButton){ searchButton.addEventListener("click", function() {
    const keyword = this.value;
    startSearch(keyword);
    },false); });
