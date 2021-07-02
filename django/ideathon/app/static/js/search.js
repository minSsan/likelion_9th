const searchGrid = document.querySelector('.search-grid')
const searchButton = searchGrid.querySelectorAll('.search-button')

document.querySelector('.active').setAttribute('class', 'nav-link')
document.getElementById('ho').setAttribute('class', 'nav-link active')

function startSearch(value) {
    location.href = `map/${value}`;
};

[].forEach.call(searchButton,function(searchButton){ searchButton.addEventListener("click", function() {
    const keyword = this.value;
    startSearch(keyword);
    },false); });

const searchKeyword = document.getElementById('searchKeyword')

document.querySelector('.search-button').addEventListener('click', function() {
    startSearch(searchKeyword.value)
})